---
date : '2025-06-22T23:22:47+08:00'
draft : false
title : 'Go的程序运行结构'
image : ""
categories : ["Golang"]
tags : ["后端开发"]
description : "Go的程序运行结构"
math : true
---

## 🔄 循环结构

Go 只有一种循环结构：**`for`** 循环。但 **`for`** 配合 **`range`** 可以灵活地遍历各种集合类型。

---

### 🔁 for 循环

基本的 **`for`** 循环由三部分组成，它们用分号隔开：

- **初始化语句**：在第一次迭代前执行，通常为一句短变量声明（可选）
- **条件表达式**：在每次迭代前求值
- **后置语句**：在每次迭代的结尾执行（可选）

```go
func main() {
    sum := 0
    for i := 0; i < 10; i++ {
        sum += i
    }
    fmt.Println(sum)
}
```

#### 🔄 实现 while 循环

Go 中没有专门的 **`while`** 关键字，只需要去掉初始化语句和后置语句即可实现：

```go
sum := 1
for sum < 1000 {
    sum += sum
}
```

#### ♾️ 无限循环

省略所有条件即可实现无限循环：

```go
for {
    // 无限循环，需要使用 break 退出
}
```

---

### 🔄 for-range 循环

**`for-range`** 是 Go 语言中遍历集合的语法糖，可以简洁高效地遍历数组、切片、字符串、**`map`** 和 **`channel`**。

#### 📝 基本语法

```go
for index, value := range collection {
    // 使用 index 和 value
}
```

- **`index`**：索引或键
- **`value`**：元素的副本（注意是副本，不是引用）
- 可以使用 **`_`** 忽略不需要的变量

---

#### 📊 遍历数组和切片

```go
nums := []int{10, 20, 30}

// 获取索引和值
for i, v := range nums {
    fmt.Printf("索引: %d, 值: %d\n", i, v)
}

// 只获取索引
for i := range nums {
    fmt.Printf("索引: %d\n", i)
}

// 只获取值（使用空白标识符）
for _, v := range nums {
    fmt.Printf("值: %d\n", v)
}
```

---

#### 🗺️ 遍历 map

```go
scores := map[string]int{
    "Alice": 90,
    "Bob":   85,
    "Carol": 92,
}

// 遍历 map（顺序不固定）
for name, score := range scores {
    fmt.Printf("%s: %d\n", name, score)
}

// 只获取键
for name := range scores {
    fmt.Println(name)
}
```

{{<notice tip>}}

**💡 面试要点：为什么 Go map 的遍历顺序是随机的？**

在 Go 中，使用 for range 遍历字典时，遍历顺序是随机的。每次运行程序时，顺序可能不同。

**原因**：
- 避免依赖顺序：防止开发者依赖遍历顺序，提高代码可移植性
- 哈希表的天然特性：哈希表本身就是无序的
- 安全性考虑：避免攻击者利用顺序性进行攻击

**如果需要有序遍历怎么办？**

先将 key 排序，再按顺序遍历：

```go
keys := make([]string, 0, len(scores))
for k := range scores {
    keys = append(keys, k)
}
sort.Strings(keys)

for _, k := range keys {
    fmt.Printf("%s: %d\n", k, scores[k])
}
```

{{</notice>}}

---

#### 🔤 遍历字符串

遍历字符串时，**`index`** 是字节索引，**`value`** 是 **`rune`** 类型（Unicode 码点）：

```go
str := "Hello, 世界"

for i, r := range str {
    fmt.Printf("索引: %d, 字符: %c, Unicode: %U\n", i, r, r)
}

// 输出：
// 索引: 0, 字符: H, Unicode: U+0048
// 索引: 1, 字符: e, Unicode: U+0065
// ...
// 索引: 7, 字符: 世, Unicode: U+4E16
// 索引: 10, 字符: 界, Unicode: U+754C
```

---

#### 📡 遍历 channel

**`for-range`** 可以持续从 **`channel`** 接收数据，直到 **`channel`** 被关闭：

```go
ch := make(chan int)

go func() {
    for i := 0; i < 5; i++ {
        ch <- i
    }
    close(ch)
}()

// 遍历 channel，直到 channel 被关闭
for v := range ch {
    fmt.Println(v)
}
```

---

#### ⚠️ 使用注意事项

##### 1️⃣ 值拷贝问题

**`for-range`** 中的 **`value`** 是元素的**副本**，修改它不会影响原集合：

```go
nums := []int{1, 2, 3}

for _, v := range nums {
    v = v * 10  // 修改的是副本，原数组不变
}
fmt.Println(nums)  // 输出: [1 2 3]

// 正确做法：通过索引修改
for i := range nums {
    nums[i] = nums[i] * 10
}
fmt.Println(nums)  // 输出: [10 20 30]
```

##### 2️⃣ 指针陷阱（面试重点）

在循环中创建指针时要注意：

```go
// ❌ 错误：所有指针都指向同一个变量
var ptrs []*int
for _, v := range []int{1, 2, 3} {
    ptrs = append(ptrs, &v)  // v 是同一个变量的副本
}

// ✅ 正确：创建局部变量
var ptrs []*int
for _, v := range []int{1, 2, 3} {
    val := v  // 创建新的局部变量
    ptrs = append(ptrs, &val)
}
```

{{<notice tip>}}

**面试题：使用 for-range 的时候，它的地址会发生变化吗？**

**答案：不会**。for-range 中的循环变量（包括 index 和 value）在整个循环过程中是**同一个变量**，只是值被不断更新。

这意味着：
1. 每次迭代时，value 变量的地址是相同的
2. 如果在循环中创建指针或闭包，所有指针都会指向同一个地址
3. 循环结束后，value 保存的是最后一次迭代的值

{{</notice>}}

##### 3️⃣ 遍历中修改集合

- **数组/切片**：可以安全修改，但不会影响遍历次数
- **map**：可以删除已遍历的键，但不能添加新键（会导致不确定行为）

---

## 🔀 分支结构

### ❓ if 条件语句

类似于 Java 的 if 结构，表达式外**无需小括号** **`( )`** ，而大括号 **`{ }`** 则是必须的。

#### 📝 基本结构

```go
if 布尔表达式 {
    // 在布尔表达式为 true 时执行
}

if 布尔表达式 {
    // 在布尔表达式为 true 时执行
} else {
    // 在布尔表达式为 false 时执行
}
```

#### 💡 示例代码

```go
func sqrt(x float64) string {
    if x < 0 {
        return sqrt(-x) + "i"
    }
    return fmt.Sprint(math.Sqrt(x))
}
```

#### 🎯 短变量声明

**`if`** 语句可以在条件表达式前执行一个短变量声明语句：

```go
func pow(x, n, lim float64) float64 {
    if v := math.Pow(x, n); v < lim {
        return v
    }
    return lim
}
```

{{<notice tip>}}

在 Go 语言中，**`ok`** 是一种**惯用写法**，它出现在多值赋值中，表示一个操作是否成功，通常是一个 **布尔值（bool）**。

通常在 if 语句的条件表达式之前使用

{{</notice>}}

#### 🔀 多条件判断（if-else if-else）

当需要判断多个条件时，可以使用 if-else if-else 结构：

```go
func main() {
    score := 85
    
    if score >= 90 {
        fmt.Println("优秀")
    } else if score >= 80 {
        fmt.Println("良好")
    } else if score >= 60 {
        fmt.Println("及格")
    } else {
        fmt.Println("不及格")
    }
}
```

运行结果：
```
良好
```

---

### 🔀 switch 语句

**`switch`** 语句是编写一连串 **`if-else`** 语句的简便方法。它运行第一个 **`case`** 值等于条件表达式的子句。

#### 📝 基本结构

```go
switch var1 {
case val1:
    // ...
case val2:
    // ...
default:
    // ...
}
```

类型判断：

```go
switch x.(type) {
case type1:
    // ...
case type2:
    // ...
default:
    // ...
}
```

#### ⚠️ 注意事项

- 相比于 Java，Go 只会运行选定的 **`case`**，而非之后所有的 **`case`**。在效果上，Go 的做法相当于这些语言中为每个 **`case`** 后面自动添加了所需的 **`break`** 语句
- **`switch`** 的 **`case`** 无需为常量，且取值不限于整数
- 在 case 中以 **`fallthrough`** 语句结束会穿透 switch 语句，只能穿透一个 **`case`** 子句。程序会继续执行下一条 case，且它不会去判断下一个 case 的表达式是否为 true

---

#### 💡 switch 的特殊用法

**1. 一个 case 可以有多个值**

多个值之间使用逗号分隔：

```go
switch day {
case 1, 2, 3, 4, 5:
    fmt.Println("工作日")
case 6, 7:
    fmt.Println("周末")
}
```

**2. 省略 switch 后的表达式**

这种形式更接近于 if-else 结构：

```go
score := 85
switch {
case score >= 90:
    fmt.Println("优秀")
case score >= 80:
    fmt.Println("良好")
case score >= 60:
    fmt.Println("及格")
default:
    fmt.Println("不及格")
}
```

**3. fallthrough 的使用**

Go 语言中的 switch 默认带有 break 效果，但如果需要继续执行下一个 case，可以使用 **`fallthrough`**：

```go
switch {
case score >= 60:
    fmt.Println("及格")
    fallthrough
case score >= 0:
    fmt.Println("分数有效")
}
```

运行结果：
```
及格
分数有效
```

{{<notice tip>}}

**注意**：`fallthrough` 必须是 case 中的最后一条语句，并且会强制执行下一个 case 的代码块，而不判断条件。

{{</notice>}}

**4. switch 用于类型判断**

```go
var x interface{} = 25.0

switch v := x.(type) {
case int:
    fmt.Printf("x是整数，值为%d\n", v)
case float64:
    fmt.Printf("x是浮点数，值为%.2f\n", v)
case string:
    fmt.Printf("x是字符串，值为%s\n", v)
default:
    fmt.Printf("x的类型未知\n")
}
```

运行结果：
```
x是浮点数，值为25.00
```

---

#### 🛠️ 实际应用示例

**1. 错误处理**

```go
if err := doSomething(); err != nil {
    fmt.Println("发生错误:", err)
    return
}
```

**2. 类型判断**

```go
var i interface{} = "Hello"

switch v := i.(type) {
case string:
    fmt.Printf("字符串: %s\n", v)
case int:
    fmt.Printf("整数: %d\n", v)
case bool:
    fmt.Printf("布尔值: %v\n", v)
default:
    fmt.Printf("未知类型\n")
}
```

**3. 状态机**

```go
type State int

const (
    Idle State = iota
    Running
    Paused
    Stopped
)

func handleState(state State) {
    switch state {
    case Idle:
        fmt.Println("系统空闲中")
    case Running:
        fmt.Println("系统运行中")
    case Paused:
        fmt.Println("系统已暂停")
    case Stopped:
        fmt.Println("系统已停止")
    }
}
```

---

#### 🧭 带表达式 switch

```go
switch os := runtime.GOOS; os {
case "darwin":
    fmt.Println("macOS.")
    // fallthrough
case "linux":
    fmt.Println("Linux.")
default:
    fmt.Printf("%s.\n", os)
}
```

#### 🎯 无表达式 switch

无条件 switch 语句可以用于代替多次 **`if-then-else`**，写得更加清晰：

```go
func main() {
    t := time.Now()
    switch {
    case t.Hour() < 12:
        fmt.Println("早上好！")
    case t.Hour() < 17:
        fmt.Println("下午好！")
    default:
        fmt.Println("晚上好！")
    }
}
```

---

## ⏱️ 推迟调用（defer）

**`defer`** 语句会将函数推迟到外层函数返回之后执行。

推迟调用的函数其参数会立即求值，但直到外层函数返回前该函数都不会被调用。

**原理**：推迟调用的函数调用会被压入一个**栈**中。当外层函数返回时，被推迟的调用会按照**后进先出**的顺序调用。

```go
func main() {
    defer fmt.Println("world")
    fmt.Println("hello")
}
// output:
// hello
// world
```

### 💡 常见用途

- 资源释放（关闭文件、解锁互斥锁等）
- 记录函数执行时间
- 捕获 panic 进行恢复

---

## 🚀 跳转控制语句

### 🛑 break

终止某个语句块的执行，用于中断 for 循环。

如果 break 出现在多次嵌套的语句块中，可以使用**标签**来指定终止哪个循环：

```go
label2:
for i := 0; i < 4; i++ {
    label1:
    for j := 0; j < 10; j++ {
        if someCondition {
            break label2  // 跳出外层循环
        }
    }
}
```

### ⏭️ continue

跳过本次循环，继续执行下一次循环。

在 for 循环中，执行 continue 语句会触发 for 增量语句的执行。

```go
for i := 0; i < 10; i++ {
    if i%2 == 0 {
        continue  // 跳过偶数
    }
    fmt.Println(i)  // 只输出奇数
}
```

### 🏷️ goto

Go 语言支持 **`goto`** 语句，但**不推荐**使用，会使代码难以阅读和维护。

```go
for i := 0; i < 10; i++ {
    if i == 5 {
        goto end
    }
}
end:
fmt.Println("跳转到此处")
```

---

## 📚 总结

| 控制结构 | 关键字 | 主要用途 |
|----------|--------|----------|
| 循环 | `for` | 基本循环结构，可替代 while |
| 遍历 | `for-range` | 遍历数组、切片、map、字符串、channel |
| 条件分支 | `if-else` | 条件判断，支持短变量声明 |
| 多分支 | `switch` | 多条件分支，自动 break |
| 推迟执行 | `defer` | 资源清理、延迟操作 |
| 跳出循环 | `break` | 终止循环，支持标签 |
| 跳过本次 | `continue` | 跳过当前迭代 |

**最佳实践**：
- 优先使用 **`for-range`** 遍历集合，代码更简洁
- 使用 **`defer`** 确保资源释放，避免遗漏
- 利用 **`if`** 短变量声明减少代码嵌套
- **`switch`** 比多分支 **`if-else`** 更清晰
