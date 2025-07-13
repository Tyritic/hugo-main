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

### 循环结构

Go 只有一种循环结构：**`for`** 循环。

基本的 **`for`** 循环由三部分组成，它们用分号隔开：

- 初始化语句：在第一次迭代前执行，通常为一句短变量声明（可选）
- 条件表达式：在每次迭代前求值
- 后置语句：在每次迭代的结尾执行（可选）

```Go
func main() {
        sum := 0
        for i := 0; i < 10; i++ {
                sum += i
        }
        fmt.Println(sum)
}
```

实现Java中的while循环只需要去掉初始化语句和后置语句

```Go
for sum < 1000 {
                sum += sum
        }
```

### 分支结构

#### if结构

类似于Java的if结构，表达式外无需小括号 **`( )`** ，而大括号 **`{ }`** 则是必须的。

##### 基本结构

```go
if 布尔表达式 {
   /* 在布尔表达式为 true 时执行 */
}

if 布尔表达式 {
   /* 在布尔表达式为 true 时执行 */
} else {
  /* 在布尔表达式为 false 时执行 */
}
```

示例代码

```Go
func sqrt(x float64) string {
        if x < 0 {
                return sqrt(-x) + "i"
        }
        return fmt.Sprint(math.Sqrt(x))
}
```

**`if`** 语句可以在条件表达式前执行一个短变量声明语句

```Go
func pow(x, n, lim float64) float64 {
        if v := math.Pow(x, n); v < lim {
                return v
        }
        return lim
}
```

{{<notice tip>}}

在 Go 语言中，**`ok`** 是一种**惯用写法**，它出现在多值赋值中，表示一个操作是否成功，通常是一个 **布尔值（bool）**。

通常在if语句的条件表达式之前使用

{{</notice>}}

#### switch结构

**`switch`** 语句是编写一连串 **`if - else`** 语句的简便方法。它运行第一个 **`case`** 值 值等于条件表达式的子句。

##### 基本结构

```go
switch var1 {
    case val1:
        ...
    case val2:
        ...
    default:
        ...
}
```

```go
switch x.(type){
    case type:
       statement(s);      
    case type:
       statement(s); 
    /* 你可以定义任意个数的case */
    default: /* 可选 */
       statement(s);
}
```

##### 注意事项

- 相比于Java，Go 只会运行选定的 **`case`** ，而非之后所有的 **`case`**。 在效果上，Go 的做法相当于这些语言中为每个 **`case`** 后面自动添加了所需的 **`break`** 语句。
- **`switch`** 的 `case` 无需为常量，且取值不限于整数。
- 在case中以 **`fallthrough`** 语句结束会穿透switch语句，只能穿透一个 **`case`** 子句。程序会继续执行下一条 case，且它不会去判断下一个 case 的表达式是否为 true。

```Go
switch os := runtime.GOOS; os {
        case "darwin":
                fmt.Println("macOS.")
                // fallthrough
        case "linux":
                fmt.Println("Linux.")
        default:
                // freebsd, openbsd,
                // plan9, windows...
                fmt.Printf("%s.\n", os)
        }
```

无条件switch语句可以用于代替多次 **`if-then-else`** 写得更加清晰。

```Go
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

### 推迟调用

defer 语句会将函数推迟到外层函数返回之后执行。

推迟调用的函数其参数会立即求值，但直到外层函数返回前该函数都不会被调用。

原理：推迟调用的函数调用会被压入一个栈中。 当外层函数返回时，被推迟的调用会按照后进先出的顺序调用。

```Go
func main() {
        defer fmt.Println("world")

        fmt.Println("hello")
}
// output:
// hello
// world
```

### 跳转控制语句

- **`break`** ：终止某个语句块的执行，用于中断for循环
  - 如果break出现在多次嵌套的语句块中，可以使用标签来指定终止哪个循环
  - ```Go
    label2
    for i:=0;i<4;i++{
        label1
        for j:=0;j<10;j++{
            break label2
        }
     }
        
    ```
- **`continue`**：跳过本次循环，继续执行下一次循环。
  - for 循环中，执行 continue 语句会触发 for 增量语句的执行
