---
date : '2026-07-01T08:00:00+08:00'
draft : false
title : '为什么加了锁也Panic'
image : ""
categories : ["故障排查经验", "Golang"]
tags : []
description : "记录一次 Go 并发场景下，加锁后仍然 Panic 的排查过程。"
---

## 背景
写 Go 并发代码，绝大多数开发者都踩过一个极其费解的坑：map 写操作明明加了 Mutex 互斥锁，已经保证了写写互斥，程序却依旧随机崩溃，报错：concurrent map iteration and map write。

很多人百思不得其解：锁明明加了，为什么还会触发并发冲突？

## 问题复现

执行逻辑分为三步：先拼接用户缓存 Key 存入 map，标记缓存未命中；再开启多协程并发回源数据库查询数据；最后回填有效数据、剔除非法用户 Key。

```go
package main

import (
	"context"
	"fmt"
	"sync"
)

func cacheKey(userId int64) string {
	return fmt.Sprintf("user:badge:%d", userId)
}

func parseUserId(key string) int64 {
	var id int64
	fmt.Sscanf(key, "user:badge:%d", &id)
	return id
}

func batchQueryFromDB(userIds []int64) (map[int64]string, error) {
	result := make(map[int64]string)
	for _, id := range userIds {
		result[id] = "badge_data_" + fmt.Sprint(id)
	}
	return result, nil
}

func BatchGetUserBadges(ctx context.Context, userIds []int64) (map[int64]string, error) {
	kv := make(map[string]string)
	for _, userId := range userIds {
		kv[cacheKey(userId)] = ""
	}

	var mu sync.Mutex
	var wg sync.WaitGroup
	wg.Add(len(kv))

	// 主协程遍历map
	for key := range kv {
		go func(k string) {
			defer wg.Done()
			userId := parseUserId(k)

			// 非法用户：加锁删除key
			if userId <= 0 {
				mu.Lock()
				delete(kv, k)
				mu.Unlock()
				return
			}

			// 回源DB查询数据
			data, err := batchQueryFromDB([]int64{userId})
			if err != nil {
				return
			}
			if v, ok := data[userId]; ok {
				// 数据回填：加锁写入
				mu.Lock()
				kv[k] = v
				mu.Unlock()
			}
		}(key)
	}

	wg.Wait()
	return kv, nil
}

func main() {
	userIds := []int64{1, 2, 3, -1, 5}
	_, _ = BatchGetUserBadges(context.Background(), userIds)
	fmt.Println("done")
}
```
为规避 map 并发写入问题，开发阶段特意对所有 delete 删除、数据赋值 等写操作添加了 Mutex 锁。自测流程完全正常，但压测和线上运行时，会随机触发 panic，报错固定为迭代与写冲突。

这段代码从常规认知来看，完全没有问题：
-所有 map 写操作全部加锁，杜绝多协程同时写入
- Mutex 保证了同一时间仅有一个协程修改 map

传统写写竞争问题已经彻底解决，既然写写安全了，为什么还会持续触发 panic？

## Go race 定位：冲突不在写写竞争，而是读写冲突
这类隐蔽的并发竞争问题，肉眼很难排查，直接使用 Go 内置的 race 检测工具定位根源：
```bash
go run -race main.go
```
输出日志如下
```bash
==================
WARNING: DATA RACE
Write at 0x00c00012a1e0 by goroutine 8:
  main.BatchGetUserBadges.func1()
      main.go:XX  // delete(kv, k)

Previous read at 0x00c00012a1e0 by goroutine 1:
  main.BatchGetUserBadges()
      main.go:XX  // for key := range kv
==================
```
真相一目了然：崩溃和写写冲突无关，核心是读写冲突！我们的锁，只保护了子协程的并发写操作，却完全忽略了主协程全程无锁的迭代读操作。

## 原因解析

### Mutex 互斥锁的局限性
sync.Mutex 是排他锁，不存在读写区分，一旦加锁，其他协程无论读写都会阻塞。但这段代码只给删除、赋值等写操作加锁，主线程遍历 map 的读逻辑完全无锁保护。于是形成高危并发组合：

- 主协程：无锁裸奔迭代 map，持续访问底层哈希桶；
- 子协程：锁内执行 delete、键值覆盖等 map 写操作；

map 迭代属于持续读操作，和并发写同时发生，构成数据竞争，运行时检测到直接 panic，这个问题不会因为写操作单独加锁就消失。

### Go Map 不可打破的运行规则
Go 运行时对 map 有一条强制硬性规则，也是绝大多数人的知识盲区：
**只要 map 处于 range 迭代状态，绝对禁止任何删除、赋值等修改操作。** 
这条规则无视手动加锁。即便写操作通过锁实现串行执行，只要迭代未结束，依旧会直接触发 panic。底层原因很简单：map 迭代不会复制完整数据，仅持有底层 bucket 的指针遍历。如果迭代过程中修改数据、删除 Key 或触发扩容，迭代指针会彻底错乱，导致内存数据异常。Go 官方选择「宁可程序崩溃，绝不输出脏数据」，从底层规避数据错乱问题。

### Map 崩溃场景
- 并发读 + 并发写 → 触发 panic
- 多协程并发写写 → 触发 panic
- 迭代遍历期间并发写（本文核心坑）→ 必崩

## 解决方案
### Channel 结果收集（最优方案）
核心思路：彻底规避迭代中修改 map。遍历阶段只做纯读取，所有协程处理结果通过 channel 统一收集，迭代结束后再批量回填写入，从根源消灭数据竞争，无需加锁、零风险、性能最优。
```go
func BatchGetUserBadgesV1(_ context.Context, userIds []int64) (map[string]string, error) {
	kv := make(map[string]string)
	for _, userId := range userIds {
		kv[cacheKey(userId)] = ""
	}

	// 通道统一收集协程结果
	type cacheResult struct {
		key string
		val string
	}
	results := make(chan cacheResult, len(kv))

	var wg sync.WaitGroup
	wg.Add(len(kv))

	// 纯读遍历，不修改原map
	for key := range kv {
		go func(k string) {
			defer wg.Done()
			userId := parseUserId(k)
			if userId <= 0 {
				return
			}
			data, err := batchQueryFromDB([]int64{userId})
			if err != nil {
				return
			}
			if v, ok := data[userId]; ok {
				results <- cacheResult{k, v}
			}
		}(key)
	}

	wg.Wait()
	close(results)

	// 遍历结束，单协程统一写入
	for r := range results {
		kv[r.key] = r.val
	}
	return kv, nil
}
```
### RWLock 读写锁
如果业务逻辑无法规避「边遍历边修改」的场景，普通 Mutex 完全不适用，必须使用 RWMutex 读写锁：遍历全程加读锁，阻塞所有写操作，读写完全互斥，解决裸读+并发写的冲突问题。
```go
func BatchGetUserBadgesV2(ctx context.Context, userIds []int64) (map[string]string, error) {
	kv := make(map[string]string)
	for _, userId := range userIds {
		kv[cacheKey(userId)] = ""
	}

	var mu sync.RWMutex
	var wg sync.WaitGroup
	wg.Add(len(kv))

	// 迭代全程加读锁，禁止一切写操作
	mu.RLock()
	for key := range kv {
		k := key
		go func() {
			defer wg.Done()
			userId := parseUserId(k)

			// 写操作申请写锁，与读锁互斥
			mu.Lock()
			defer mu.Unlock()

			if userId <= 0 {
				delete(kv, k)
				return
			}
			data, err := batchQueryFromDB([]int64{userId})
			if err != nil {
				return
			}
			if v, ok := data[userId]; ok {
				kv[k] = v
			}
		}()
	}
	mu.RUnlock()

	wg.Wait()
	return kv, nil
}
```
缺点：迭代期间写操作会阻塞，大批量高并发场景下性能表现一般，仅适合小数据量兼容改造。
