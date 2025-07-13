---
date : '2025-07-13T23:06:54+08:00'
draft : false
title : 'Go的排序'
image : ""
categories : ["Golang"]
tags : ["后端开发"]
description : "Go中实现排序"
math : true
---

## 标准库sort

Go 语言的标准库 **`sort`** 包提供了强大且易用的排序功能，能够对多种类型的数组进行排序。

## 基本数据类型排序

标准库提供了三种内置排序函数用于排序，只支持正向排序

- **`sort.Ints()`**
- **`sort.Float64s()`**
- **`sort.Strings()`**

```go
import "sort"

// 排序 int 切片
sort.Ints([]int{5, 2, 6, 3})

// 排序 float64 切片
sort.Float64s([]float64{2.3, 1.1, 5.5})

// 排序 string 切片
sort.Strings([]string{"banana", "apple", "cherry"})
```

同时标准库提供函数来判断是否已经排序

- **`sort.IntsAreSorted()`**
- **`sort.StringsAreSorted()`** 

要实现反向排序

- 先将把 **`[]int`** 转换为 **`sort.IntSlice`** 类型，具备 **`Len()`** , **`Less()`** , **`Swap()`** 方法的类型：**`sort.IntSlice(nums)`**
- 再返回一个降序的包装器：**`sort.Reverse(...)`**
- 使用排序算法对这个降序包装器进行排序：**`sort.Sort(...)`**
- 综合可得：**`sort.Sort(sort.Reverse(sort.IntSlice(nums)))`**

## 自定义排序规则

**`sort.Slice`** 是 Go 标准库中一个非常强大且灵活的函数，用于对**任意类型的切片**进行排序，只需提供一个比较函数。

```go
func Slice(slice any, less func(i, j int) bool)
```

| 参数名      | 类型                  | 说明                                   |
| ----------- | --------------------- | -------------------------------------- |
| **`slice`** | **`any`**（接口类型） | 任何切片（`[]T`）都可以                |
| **`less`**  | `func(i, j int) bool` | 比较函数，用来决定排序顺序（基于索引） |

```go
type Person struct {
    Name string
    Age  int
}

people := []Person{
    {"Alice", 30},
    {"Bob", 25},
    {"Charlie", 35},
}

// 按 Age 升序排序
sort.Slice(people, func(i, j int) bool {
    return people[i].Age < people[j].Age
})

```

## 复杂排序结构

在 Go 中，**`sort.Interface`** 是标准库 `sort` 包中定义的一个**接口**，用于支持自定义类型的排序。只要你实现了这个接口的三个方法，就可以用 **`sort.Sort()`** 对你的类型进行排序。

接口定义

```go
type Interface interface {
    Len() int
    Less(i, j int) bool
    Swap(i, j int)
}
```

| 方法            | 作用                                              |
| --------------- | ------------------------------------------------- |
| **`Len()`**     | 返回元素数量                                      |
| **`Less(i,j)`** | 如果元素 `i` < `j`，返回 `true`（即决定排序顺序） |
| **`Swap(i,j)`** | 交换第 `i` 和 `j` 个元素                          |

示例代码

```go
type ByAge []Person

func (a ByAge) Len() int           { return len(a) }
func (a ByAge) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByAge) Less(i, j int) bool { return a[i].Age < a[j].Age }

sort.Sort(sort.Reverse(ByAge(people)))
```

常见函数

- **`func Sort(data sort.Interface)`** ：根据接口实现进行排序
- **`func Reverse(data Interface) Interface`** ：需要配合 **`sort.Sort`** 使用，返回一个降序的包装器
- **`func Stable(data Interface)`** ：根据接口实现进行稳定排序
