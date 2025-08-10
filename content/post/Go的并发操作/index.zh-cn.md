---
date : '2025-08-10T22:41:59+08:00'
draft : false
title : 'Go的并发操作'
image : ""
categories : ["Golang"]
tags : ["后端开发"]
description : "Go的多线程和并发操作"
math : true
---
## 基本概念

- 进程：程序是指编译过的、可执行的二进制代码。进程指正在运行的程序。进程包括二进制镜像，加载到内存中，还涉及很多其他方面：虚拟内存实例、内核资源如打开的文件、安全上下文如关联的用户，以及一个或多个线程。
- 线程：线程是进程内的活动单元，每个线程包含自己的虚拟存储器，包括栈、进程状态如寄存器，以及指令指针。在单线程进程中，进程即线程，一个进程只有一个虚拟内存实例，一个虚拟处理器。在多线程的进程中，一个进程有多个线程，由于虚拟内存是和进程关联的，所有线程会共享相同的内存地址空间
- 协程：协程可以理解为一种轻量级线程，与线程相比，协程不受操作系统调度。协程调度器完全由用户应用程序提供，协程调度器按照调度策略把协程调度到线程中运行。

## Goroutine

> 传统的线程调度有以下问题：
>
> - 资源消耗大：每个线程需要 2MB-8MB 栈空间、创建和销毁需要大量系统调用
> - 性能开销高：频繁的用户态/内核态切换、上下文切换成本高（寄存器、缓存、TLB）
> - 编程复杂：需要手动管理线程生命周期、同步原语（锁、信号量）使用复杂

goroutine 是由 Go runtime 管理的轻量级线程。

- 轻量级：Go runtime 管理的用户级线程，初始栈空间 2KB（线程 1MB+），支持百万级创建，启动销毁成本低。
- 高效调度机制：Go runtime 负责调度，上下文切换延迟 0.2 微秒（线程 1-2 微秒），仅保存必要寄存器状态。
- 灵活内存管理：动态栈设计（2KB-1GB），按需伸缩，包含程序计数器、栈空间、调度状态等基础功能



## 锁

### 互斥锁sync.Mutex

互斥锁保证同一时间**只有一个 goroutine** 能进入临界区，适合**写多读少**的场景。

```go
var mu sync.Mutex
mu.Lock()
// 临界区
mu.Unlock()
```

注意事项

- 避免重复加锁而不解锁
- 锁未释放前再次访问需要该锁的代码
- 避免对未锁定的互斥锁解锁（会导致panic）
- goroutine被加锁后需要及时解锁否则其他goroutine无法拿到锁

### 读写锁sync.RWMutex

读写锁指读操作和写操作分开,可以分别对读操作和写操作进行加锁,一般用在大量读操作少量写操作的情况

```go
var rw sync.RWMutex
rw.RLock()   // 读锁
rw.RUnlock() // 读操作

rw.Lock()    // 写锁
rw.Unlock()  // 写操作
```

读写锁的使用有以下几个原则

- 同时只有一个 goroutine 能获得写锁,
- 同时可以有多个 goroutine 获得读锁,
- 同时只能存在写锁定和读锁定,

通俗理解就是可以多个goroutine同时读,但是只有一个goroutine能写,共享资源要么在被一个或多个goroutine读
取,要么在被一个goroutine写入,读写不能同时进行。

## 并发操作

### 一次执行sync.Once

保证某个操作**只会执行一次**，并且是并发安全的。无论有多少个 goroutine 同时调用它，都不会重复执行。

常用于单例模式、初始化资源等。

```go
var once sync.Once
once.Do(func() {
    fmt.Println("只执行一次")
})
```

核心方法

```go
func (o *Once) Do(f func())
```

- `f`：要执行的一段函数
- 多个 goroutine 并发调用 `Do` 时，只有 **第一次** 调用会执行 `f`，后面的调用会直接跳过。
- 保证了**并发安全**（内部用了互斥锁和标志位）。

注意事项

- **`Do`** 里传入的函数**必须是幂等的**（即多次调用不会出错），虽然它理论上只执行一次，但业务逻辑最好可重复。
- 不能在 `Do` 的函数里再次调用同一个 **`once.Do`**（会死锁）。
- 不能直接复制 **`sync.Once`**，应始终用指针或包级变量。

###  条件变量sync.Cond

**`sync.Cond`** 是 Go 里的**条件变量**，用来在多个 goroutine 之间进行 **等待** 和 **通知**。
 它本身不控制互斥，而是依赖于一个锁（ **`sync.Mutex`** 或 **`sync.RWMutex`**）来保护共享状态。

简单来说：

> 当某个条件不满足时，goroutine 可以等待；
>  当另一个 goroutine 改变了条件并发出信号，等待的 goroutine 才会继续执行。

创建条件变量

```go
cond := sync.NewCond(&sync.Mutex{})
```

| 方法                   | 作用                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **`cond.Wait()`**      | 等待条件成立，释放锁并阻塞，直到被 `Signal()` 或 `Broadcast()` 唤醒，然后会重新加锁返回。 |
| **`cond.Signal()`**    | 唤醒**一个**正在等待的 goroutine。                           |
| **`cond.Broadcast()`** | 唤醒**所有**正在等待的 goroutine。                           |

生产者-消费者示例

```go
package main

import (
    "fmt"
    "sync"
)

var (
    mu   sync.Mutex
    cond = sync.NewCond(&mu)
    data []int
)

func producer() {
    for i := 1; i <= 5; i++ {
        mu.Lock()
        data = append(data, i)
        fmt.Println("生产:", i)
        cond.Signal() // 通知一个等待的消费者
        mu.Unlock()
    }
}

func consumer(id int) {
    for {
        mu.Lock()
        for len(data) == 0 { // 条件不满足，等待
            cond.Wait()
        }
        x := data[0]
        data = data[1:]
        fmt.Printf("消费者%d 消费: %d\n", id, x)
        mu.Unlock()
    }
}

func main() {
    go consumer(1)
    go consumer(2)

    producer()
}
```

注意事项

- **必须配合锁使用**：`Wait()` 调用前需要加锁，它会在内部自动释放锁并阻塞，唤醒后会重新加锁。
- **要用循环检查条件**：因为即使被唤醒，条件也可能依旧不满足（虚假唤醒）。

### 原子操作sync/atomic

所谓原子操作就是这一系列的操作在cpu上执行是一个不可分割的整体,显然要要么全部执行,要么全部不执行,不会受到其他操作的影响,也就不会存在并发问题。

- 提供无锁的原子操作，比如原子加减、交换、比较并交换（CAS）。
- 适合需要高性能并发计数、标志位控制的场景。

```go
import "sync/atomic"

var counter int64
atomic.AddInt64(&counter, 1)
```

常见方法

```go
func AddT(addr *T,delta T)(new T) // 原子地将 delta 加到 *addr 上，并返回更新后的新值。
func storeT(addr *T, val T) // 原子地将 val 存储到 *addr，替代直接赋值 *addr = val，保证写入在并发下可见。
func LoadT(addr *T)(val T) // 原子地读取 *addr 的值，保证读到的是一致的有效数据（避免竞争条件）。
func swapT(addr *T, new T)(old T) // 原子地将 *addr 设置为 new，并返回原先的旧值。
func compareAndswapT(addr *T,old, new T)(swaapped bool) // 比较 *addr 是否等于 old，如果相等则原子地更新为 new，返回 true；否则返回 false。
```

T的类型是 **`int32`** 、**`int64`** 、**`uint32`** 、**`uint64`** 和 **`uintptr`** 中的任意一种。