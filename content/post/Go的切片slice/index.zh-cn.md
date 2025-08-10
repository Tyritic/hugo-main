---
date : '2025-06-29T09:45:02+08:00'
draft : false
title : 'Go的切片slice'
image : ""
categories : ["Golang"]
tags : ["后端开发"]
description : "Slice的底层原理"
math : true
---
## 切片的定义

Go 语言中切片是对数组的抽象。

Go 数组的长度不可改变，在特定场景中这样的集合就不太适用，Go 中提供了一种灵活，功能强悍的内置类型切片("动态数组")，与数组相比切片的长度是不固定的，可以追加元素，在追加时可能使切片的容量增大。切片可以理解为对底层数组的一个动态视图。Go 切片有三个属性：**指针**（pointer，指向底层数组中切片起始位置）、**长度**（len）和**容量**（cap，表示从起始位置到底层数组末尾的容量）。

特点

- 切片就像数组的引用 切片并不存储任何数据，它只是描述了底层数组中的一段。
- 更改切片的元素会修改其底层数组中对应的元素。
- 和它共享底层数组的切片都会观测到这些修改。

## 切片的声明方法

- 声明切片：**`var identifier []type`** 此时为 nil 切片（还未指向数组）

- 创建切片

  - 截取数组

    - **`arr[startIndex:endIndex]`** ：将 arr 中从下标 startIndex 到 endIndex-1 下的元素创建为一个新的切片
    - 默认 startIndex 时将表示从 arr 的第一个元素开始。
    - 默认 endIndex 时将表示一直到arr的最后一个元素。

    ```go
    arr := [5]int{1, 2, 3, 4, 5}
    s := arr[1:4]  // s = [2 3 4]，len=3，cap=4
    ```

  - 使用make函数

    - **`make([]var_type, length)`**
    - **`make([]var_type, length, capacity)`**

    ```go
    var slice1 []type = make([]type, len)
    // 也可以简写为
    slice1 := make([]type, len)
    ```

  - 字面量初始化：**`s := []string{"Go", "Rust", "Java"}`**

  - 通过切片 s 初始化切片 s1：**`s1 := s[startIndex:endIndex]`** 

{{<notice tip>}}

nil 切片与空切片是不同的：

- nil 切片 ：不会创建底层数组，指针为 nil
- 空切片 ：会创建一个空的底层数组（长度为 0），指针指向一个特殊的内存地址（通常是 runtime.zerobase）

{{</notice>}}

## 基本操作

### 追加元素

```go
func append(s []T, vs ...T) []T
```

- **`s`** 是一个元素类型为 **`T`** 的切片
- 其余类型为 **`T`** 的值将会追加到该切片的末尾。

### 遍历元素

```Go
func main() {
      for i, v := range pow {
           fmt.Printf("2**%d = %d\n", i, v)
      }
}
```

**`for`** 循环的 **`range`** 形式可遍历切片或映射。

当使用 **`for`** 循环遍历切片时，每次迭代都会返回两个值。 

- 第一个值为当前元素的下标
- 第二个值为该下标所对应元素的一份副本。

注意事项

- 可以将下标或值赋予 **`_`** 来忽略它。

```Go
for i := range pow {
                pow[i] = 1 << uint(i) // == 2**i
        }
for _, value := range pow {
                fmt.Printf("%d\n", value)
        }
```

{{<notice tip>}}

在循环中 append 的陷阱（ **`for-range`** 每次迭代都使用同一个变量）

在 Go 的 **`for i, v := range slice`** 循环中：

- **`v`** 是 **每次循环复用的同一个变量**，只是其值在变。
- 所以 **`&v`** 每次取的其实是 **同一个地址**。
- 所以你 **`append(&v)`** 多次，实际上是把 **相同地址的指针**添加了多次。

错误示例

```go
func example5() {
    slice := []int{1, 2, 3}
    newSlice := make([]*int, 0)

    for _, v := range slice {
        newSlice = append(newSlice, &v) // 错误：所有指针都指向同一个变量
    }
}
```

正确示例

定义一个局部变量来捕获每个元素

```go
func solution5() {
    slice := []int{1, 2, 3}
    newSlice := make([]*int, 0)
    
    for _, v := range slice {
        value := v // 创建新变量
        newSlice = append(newSlice, &value)
    }
}
```


{{</notice>}}

### 删除元素

Go 没有内置的删除元素语法，需要手动实现

- 删除尾部元素：移动尾部指针

```Go
a = a[:len(a)-1]   // 删除尾部 1 个元素
a = a[:len(a)-N]   // 删除尾部 N 个元素
```

- 删除首部元素：移动首部指针

```Go
a = a[1:] // 删除开头 1 个元素
a = a[N:] // 删除开头 N 个元素
```

- 删除中间元素（第i个元素）

```Go
a = append(a[:i], a[i+1:]...) // 删除中间 1 个元素
a = append(a[:i], a[i+N:]...) // 删除中间 N 个元素
```

### 获取长度和容量

切片是可索引的，并且可以由 **`len()`** 方法获取长度。

切片提供了计算容量的方法 **`cap()`** 可以测量切片最长可以达到多少。

- **`func len(var_name []T)`**
- **`func cap(var_name []T)`**

### 复制切片

```go
func copy(dst, src []T) int
```

- **`dst`** ：目标切片（目标空间）。

- **`src`** ：源切片（被复制的数据源）。

- 返回值：成功复制的元素数量（即 **`min(len(dst), len(src))`**）。

### 切片展开

在 Go 里，**`...`** 主要有 **两个核心用途**，意义完全取决于它出现的位置

#### 可变参数

表示**可变参数**（variadic parameter），也就是这个参数可以接收**任意数量**的值。

```go
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

func main() {
    fmt.Println(sum(1, 2))        // 3
    fmt.Println(sum(1, 2, 3, 4)) // 10
}
```

#### 切片展开

表示**展开切片**（slice expansion），把切片里的元素依次当作独立的参数传入。

```go
func printAll(a ...string) {
    for _, s := range a {
        fmt.Println(s)
    }
}

func main() {
    words := []string{"Go", "is", "cool"}
    printAll(words...) // 展开切片传入
}
```

**`append`** 中表示把一个切片的元素依次追加/传入

```go
a := []int{1, 2}
b := []int{3, 4}
a = append(a, b...) // 把 b 展开后追加到 a
fmt.Println(a) // [1 2 3 4]
```

## slice 和 slice 指针的区别

- 当 slice 作为函数参数时，就是一个普通的结构体。在调用者看来，实参 slice 并不会被函数中的操作改变
- 当 slice 指针作为函数参数，在调用者看来，是会被改变原 slice 的。

值得注意的是，不管传的是 slice 还是 slice 指针，如果改变了 slice 底层数组的数据，会反应到实参 slice 的底层数据。因为底层数据在 slice 结构体里是一个指针，尽管 slice 结构体自身不会被改变，也就是说底层数据地址不会被改变。 但是通过指向底层数据的指针，可以改变切片的底层数据。

- 传 slice 和 slice 指针，如果对 slice 数组里面的数据做修改，都会改变 slice 底层数据
- 传 slice 是拷贝，在函数内部修改，不会修改 slice 的结构， **`len`** 和 **`cap`** 不变 ，传slice 指针是修改，会修改其 slice 结构。

因此要想真的改变外层 slice，只有将返回的新的 slice 赋值到原始 slice，或者向函数传递一个指向 slice 的指针。

## nil 切片，切片为 nil和空切片

- nil切片：底层指向数组为nil，不可以直接进行访问，常见于声明阶段 **`var s []int`**
- 空切片：底层指向数组为空数组（非nil），常见于初始化阶段 **`s := []int{}`**

## 踩坑实录总结

### 误用slice预分配空间

下面代码预期创建**容量**为2的[]int，实际创建了**长度**为2的[]int。

```Go
package main

import "fmt"

func main() {
    a := make([]int, 2)
    a = append(a, 1)
    a = append(a, 1)
    fmt.Println(a)
}
// 运行结果
[0 0 1 1]

Process finished with the exit code 0
```

**解析：**

make()函数可以创建slice：

- **`make([]T, length, capacity)`** ：创建初始容量为capacity，初始长度为length（用零值填充），类型为[]T的slice
- **`make([]T, length)`** ：创建初始长度为length（用零值填充），类型为[]T的slice

**`length`** 表示初始长度，即slice已经包含数据的个数，默认会用零值填充；

**`capacity`** 表示初始容量，即slice的当前可容量的数据个数，当满足一定条件会自动扩容。

**解决方法：**尽量不用 **`make`** 创建slice

```Go
func main() {
    var a []int // 或者a:=[]int{}
    a = append(a, 1)
    a = append(a, 1)
    fmt.Println(a)
}
```

### 注意slice和底层数组的关系

slice底层数据结构：

- **`array`** ：用于存储数据，指向一块连续的内存空间；
- **`len`** ：大小，表示已存储数据的数量；
- **`cap`** ：容量，表示连续内存空间的大小

对数组进行截取操作后赋值给切片（并没有拷贝），与原数组共用内存空间，所以修改切片也会修改原数组对应的数据。

使用 **`append`** 添加数据后，触发扩容产生新的array，与原数组不是同一个内存空间，所以修改原数组不会对切片产生影响。

## 底层原理

切片的底层结构体如下

```go
type slice struct {
    ptr *T     // 指向底层数组的指针
    len int    // 当前切片长度
    cap int    // 容量（从ptr开始到底层数组的长度）
}
```

### 扩容机制

当容量不足时，Go 会创建一个新的底层数组

#### Go 1.18之前

```go
// src/runtime/slice.go

func growslice(et *_type, old slice, cap int) slice {
    // ...

    newcap := old.cap
    doublecap := newcap + newcap
    if cap > doublecap {
        newcap = cap
    } else {
        if old.cap < 1024 {
            newcap = doublecap
        } else {
            // Check 0 < newcap to detect overflow
            // and prevent an infinite loop.
            for 0 < newcap && newcap < cap {
                newcap += newcap / 4
            }
            // Set newcap to the requested cap when
            // the newcap calculation overflowed.
            if newcap <= 0 {
                newcap = cap
            }
        }
    }

    // ...

    return slice{p, old.len, newcap}
}
```

- 扩容逻辑
  - 请求的容量大于当前容量的两倍则扩容到请求的容量
  - 若请求的容量小于当前容量的两倍
    - 当前容量小于1024 时扩容到原来的两倍
    - 当前容量大于 1024 时扩容到原来的1.25倍

#### Go 1.18之后

```go
// src/runtime/slice.go

func growslice(et *_type, old slice, cap int) slice {
    // ...

    newcap := old.cap
    doublecap := newcap + newcap
    if cap > doublecap {
        newcap = cap
    } else {
        const threshold = 256
        if old.cap < threshold {
            newcap = doublecap
        } else {
            // Check 0 < newcap to detect overflow
            // and prevent an infinite loop.
            for 0 < newcap && newcap < cap {
                // Transition from growing 2x for small slices
                // to growing 1.25x for large slices. This formula
                // gives a smooth-ish transition between the two.
                newcap += (newcap + 3*threshold) / 4
            }
            // Set newcap to the requested cap when
            // the newcap calculation overflowed.
            if newcap <= 0 {
                newcap = cap
            }
        }
    }

    // ...

    return slice{p, old.len, newcap}
}
```

扩容逻辑

- 请求的容量大于当前容量的两倍则扩容到请求的容量

- 当前容量小于 256 时直接扩容到原来的两倍
- 当前容量大于 256 时逐步扩容，**逐步增加约 1.25 倍**。
- 除上述逻辑外，Go 还会根据切片中的元素大小对齐内存，因此扩容不总是精确的 2 倍或 1.25 倍