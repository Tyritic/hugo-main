---
date : '2025-06-11T16:57:17+08:00'
draft : false
title : 'Go的数据类型和变量'
image : ""
categories : ["Golang"]
tags : [""]
description : "Go中变量的声明和踩坑点"
math : true
---

## 📝 变量的声明方式

声明变量的一般形式是使用 **`var`** 关键字，有以下使用方法：

---

### 📦 单变量声明

#### 1️⃣ 指定变量类型

声明后若不赋值，使用默认值。

```go
var var_name var_type
```

#### 2️⃣ 类型推导

根据值自行判定变量类型。

```go
var v_name = value
```

#### 3️⃣ 短变量声明

省略 **`var`**，使用 **`:=`** 初始化声明。

```go
v_name := value
```

**注意事项**：
- **`:=`** 左侧的变量不应该是已经声明过的，否则会导致编译错误
- 在定义变量 a 之前使用它，则会得到编译错误 `undefined: a`
- 声明了一个局部变量却没有在相同的代码块中使用它，同样会得到编译错误
- 只可以在函数内使用，不能用于声明全局变量

#### 💻 示例代码

```go
package main

import "fmt"

func main() {
    // 第一种：使用默认值
    var a int
    fmt.Printf("a = %d\n", a)

    // 第二种：指定类型和值
    var b int = 10
    fmt.Printf("b = %d\n", b)

    // 第三种：省略类型，自动匹配
    var c = 20
    fmt.Printf("c = %d\n", c)

    // 第四种：短变量声明
    d := 3.14
    fmt.Printf("d = %f\n", d)
}
```

---

### 📦 多变量声明

#### 全局变量分解写法

```go
var x, y int
var ( // 分解的写法，一般用于声明全局变量
    a int
    b bool
)
```

#### 函数内多变量声明

```go
var c, d int = 1, 2
var e, f = 123, "liudanbing"
g, h := 123, "hello" // 只能在函数体内使用
```

---

## 🏷️ 命名规则

- 一个名字必须以一个字母（Unicode 字母）或下划线开头，后面可以跟任意数量的字母、数字或下划线
- 大写字母和小写字母是不同的：`heapSort` 和 `Heapsort` 是两个不同的名字
- Go 语言程序员推荐使用**驼峰式**命名，当名字由几个单词组成时优先使用大小写分隔，而不是优先用下划线分隔

---

## 📊 基本数据类型

Go 的数据类型分类与 Java 类似，分为**基本数据类型**和**派生数据类型**。

### 📋 数据类型概览

| 类型分类 | 具体类型 |
|---------|---------|
| **基本数据类型** | 数值型（整数、浮点）、字符型、布尔型、字符串 |
| **派生数据类型** | 指针、数组、结构体、管道、函数、切片、接口、map |

---

### 🔢 数值型

#### 整数型

**有符号整数**：

| 类型 | 有无符号 | 占用存储空间 | 数据范围 |
|:----:|:--------:|:------------:|:--------:|
| int8 | 有 | 1 个字节 | $-128$ ~ $127$ |
| int16 | 有 | 2 个字节 | $-2^{15}$ ~ $2^{15}-1$ |
| int32 | 有 | 4 个字节 | $-2^{31}$ ~ $2^{31}-1$ |
| int64 | 有 | 8 个字节 | $-2^{63}$ ~ $2^{63}-1$ |

**无符号整数**：

| 类型 | 有无符号 | 占用存储空间 | 数据范围 |
|:----:|:--------:|:------------:|:--------:|
| uint8 | 无 | 1 个字节 | $0$ ~ $255$ |
| uint16 | 无 | 2 个字节 | $0$ ~ $2^{16}-1$ |
| uint32 | 无 | 4 个字节 | $0$ ~ $2^{32}-1$ |
| uint64 | 无 | 8 个字节 | $0$ ~ $2^{64}-1$ |

**其他整数类型**：

| 类型 | 有无符号 | 占用存储空间 | 说明 |
|:----:|:--------:|:------------:|:----:|
| int | 有 | 32 位系统 4 字节<br>64 位系统 8 字节 | 默认整数类型 |
| uint | 无 | 32 位系统 4 字节<br>64 位系统 8 字节 | 无符号默认类型 |
| rune | 有 | 4 个字节 | 等价 int32，表示 Unicode 码点 |
| byte | 无 | 1 个字节 | uint8 的别名，存储字符 |

#### 浮点数型

| 类型 | 占用存储空间 | 说明 |
|:----:|:------------:|:----:|
| float32 | 4 字节 | 单精度浮点 |
| float64 | 8 字节 | 双精度浮点（默认） |

**注意事项**：
- Go 浮点类型有固定的范围和字段长度，不受具体操作系统的影响
- Go 的浮点型**默认声明为 float64** 类型

---

### 🔤 字符型

Go 中没有专门的字符类型，如果要存储单个字符（字母），一般使用 **`byte`** 来保存。

```go
var x byte = 'a'
```

**常见转义字符**：

| 转义字符 | 含义 |
|:--------:|:----:|
| `\t` | 制表符 |
| `\n` | 换行符 |
| `\r` | 回车符 |

**注意事项**：
- Go 的字符采用 UTF-8 编码，字符本质上是一个整数
- 直接输出时输出的是字符的 UTF-8 码值
- 使用格式化输出 **`%c`** 才能输出字符值

---

### ✅ 布尔类型

布尔类型使用 **`bool`** 存储，大小为 1 个字节，只允许值为 **`true`** 和 **`false`**。

---

### 📜 字符串类型

字符串是一串固定长度的字符连接起来的字符序列。Go 的字符串是由单个字节连接起来的，采用 **UTF-8** 编码。

#### 🔧 底层原理

```go
type StringHeader struct {
    Data uintptr  // 指向字节数组的指针
    Len  int      // 字符串长度
}
```

#### ⚠️ 注意事项

- 在 Go 中字符串是**不可变的**，类似 Java
- **双引号** `" "`：表示字符串，会识别转义字符
- **反引号** `` ` ` ``：以字符串的原生形式输出，包括换行和特殊字符
- 字符串之间使用 **`+`** 进行拼接
- 对于长字符串使用分行拼接处理，将 **`+`** 保留在上一行

---

## 🌐 作用域

Go 语言中变量可以在三个地方声明：

- **函数内定义的变量**：局部变量
- **函数外定义的变量**：全局变量
- **函数定义中的变量**：形式参数

### 📍 作用域分类

| 作用域类型 | 说明 |
|:----------:|:----:|
| **局部变量** | 在函数体内声明，作用域只在函数体内，参数和返回值变量也是局部变量 |
| **全局变量** | 在函数体外声明，可在整个包甚至外部包（被导出后）使用 |
| **形式参数** | 会作为函数的局部变量来使用 |

---

## 🎯 基本数据类型的默认值

在 Go 中，数据类型都有一个默认值（零值）。

| 数据类型 | 默认值 |
|:--------:|:------:|
| int | 0 |
| float | 0 |
| string | "" |
| bool | false |

---

## 🔄 基本数据类型之间的相互转换

Go 和 Java 不同，**Go 不支持数据类型的自动转换**，需要显式转换。

### 📝 语法格式

```go
var i dataType
var j = newType(i)
```

### 📤 基本数据类型转 string

- **`fmt.Sprintf("%参数", 表达式)`**
- 使用 **`strconv`** 包中的函数：
  - `func FormatBool(b bool) string`
  - `func FormatInt(i int64, base int) string`
  - `func FormatFloat(f float64, fmt byte, prec, bitSize int) string`

### 📥 string 转基本类型

- 使用 **`strconv`** 包中的函数：
  - `func ParseBool(str string) (value bool, err error)`
  - `func ParseFloat(s string, bitSize int) (f float64, err error)`
  - `func ParseInt(s string, base int, bitSize int) (i int64, err error)`
  - `func ParseUint(s string, b int, bitSize int) (n uint64, err error)`

---

## 🔗 指针

类似于 C++，Go 保留了指针。

指针保存了值的内存地址，其零值为 **`nil`**。

- **取址符** **`&`**：生成一个指向其操作数的指针，获取地址
- **解引用** **`*`**：通过指针访问或修改它指向的值

{{<notice tip>}}

- **需要修改原值**：如果希望函数里对参数的修改**直接作用到调用方的变量**，就需要传指针
- **避免复制大对象**：Go 的值传递会复制一份参数，如果结构体很大，复制成本高，可以传指针来避免拷贝

{{</notice>}}

---

## 🏗️ 结构体

一个结构体（**`struct`**）就是一组字段（field）。

### 📝 创建和初始化

```go
// 声明
type struct_variable_type struct {
   member definition
   member definition
   ...
   member definition
}

// 初始化
variable_name := structure_variable_type {
    member1: value1,
    member2: value2,
    membern: valuen,
}
```

Go 的结构体支持**匿名字段**，用于在一个结构体中插入另一个结构体，可以模拟实现继承行为。

**结构体常通过指针传递，避免复制整个结构体，提高性能。**

---

### 🏷️ 结构体标签（Tag）

虽然 Go 本身语法中没有类似 Java 中的 **`@Annotation`** 的注解机制，但结构体字段可以使用反引号（`）添加 tag，以传递元信息给反射或其他工具使用。

- 标签必须用**反引号（`）**包裹
- 每个 tag 是 **`key:"value"`** 形式，多个 tag 之间以空格分隔
- 每个 key 应唯一

```go
type User struct {
    ID    int    `json:"id" db:"user_id" validate:"required"`
    Name  string `json:"name" db:"username" comment:"用户姓名"`
    Email string `json:"email,omitempty" validate:"email"`
}
```

---

### 🔗 方法绑定

利用方法绑定可以实现类似 Java 的成员方法的效果。**方法绑定**指的是某个方法被**绑定（关联）到某个类型的值（value）或指针（pointer）上**。

```go
func (var_name varType) func_name(parameter_type parameterlist) return_type {
    // 方法体
}
```

- **值接收者**：传的是**副本**，原值不受影响
- **指针接收者**：可以修改原对象内容

---

### 🔄 JSON 解析

Go 通常使用标准库中的 **`encoding/json`** 做序列化和反序列化。

```go
package main

import (
    "encoding/json"
    "fmt"
)

type User struct {
    Name string `json:"name"` // 指定 JSON 字段名
    Age  int    `json:"age"`
}

func main() {
    // 序列化
    u := User{Name: "Alice", Age: 30}
    data, _ := json.Marshal(u)
    fmt.Println(string(data)) // {"name":"Alice","age":30}
    
    // 反序列化
    jsonStr := `{"name":"Bob","age":25}`
    var u2 User
    json.Unmarshal([]byte(jsonStr), &u2)
    fmt.Println(u2.Name, u2.Age) // Bob 25
}
```

**JSON Tag 属性**：
- `json:"name"`：将字段编码为指定名称
- `json:"name,omitempty"`：若字段为零值则忽略
- `json:"-"`：忽略该字段，不参与序列化

---

### 🔀 继承和聚合

Go 语言中没有类的概念，但可以通过**结构体嵌入**（匿名字段）来实现面向对象编程的某些特性。

```go
type Animal struct {
    Name string
}

func (a *Animal) speak() {
    fmt.Printf("%s speaks\n", a.Name)
}

type Dog struct {
    *Animal  // 嵌入 Animal
    Breed string
}

func (d *Dog) Bark() {
    fmt.Printf("%s the %s dog barks\n", d.Name, d.Breed)
}
```

---

## 🎯 结构体高级特性（面试重点）

### 🆚 struct 能不能比较？

在 Go 里，**struct 可以使用 `==` 和 `!=` 比较**，前提是 struct 内的**所有字段都是可比较的**（comparable）。

**可比较类型**：
- 基本类型（int、string、bool 等）
- 指针、channel、interface

**不可比较类型**：
- **slice、map、func** 不是可比较类型，只能与 nil 比较

```go
// ✅ 可以比较
type Person struct {
    Name string
    Age  int
}
p1 := Person{"Alice", 30}
p2 := Person{"Alice", 30}
fmt.Println(p1 == p2) // true

// ❌ 不能比较（包含 slice）
type Student struct {
    Name  string
    Scores []int  // slice 不可比较
}
```

---

### 🆚 两个 interface 能比较吗？

**可以比较，但有条件**：

1. 比较动态类型是否相同
2. 如果相同，再比较动态值
3. **如果底层类型不可比较（slice、map、func），会 panic**

```go
var a interface{} = []int{1, 2, 3}
var b interface{} = []int{1, 2, 3}
// fmt.Println(a == b) // ❌ panic：slice 不可比较
```

---

### ❓ Go 有没有 this 指针？

Go 语言里**没有像 Java 或 C++ 那样的 this 指针**，但它有一个等价但更灵活的概念：**方法的接收者（receiver）**。

Go 在定义方法时，**显式声明接收者**是谁：

```go
func (p Person) GetName() string {
    return p.Name  // p 就相当于 this
}
```

---

### ✅ 如何判断结构体是否实现了某接口？

使用**类型断言**来判断：

```go
var _ Speaker = (*Person)(nil)  // 编译期检查

// 或者运行时检查
var s Speaker = p
_, ok := s.(Person)
```

**如果结构体实现了接口的所有方法，就实现了该接口**（隐式实现）。

---

### 🔧 类型别名 vs 类型定义

| 特性 | 类型别名 `type A = B` | 类型定义 `type A B` |
|:----:|:---------------------:|:-------------------:|
| 兼容性 | 与原类型完全兼容 | 与原类型不兼容，需要显式转换 |
| 方法支持 | 不能添加方法 | 可以添加方法，实现接口 |
| 类型安全 | 允许隐式转换 | 更强的类型安全 |

```go
// 类型别名
type MyInt = int
var i MyInt = 12
var j int = 8
fmt.Println(i + j)  // ✅ 可以直接相加

// 类型定义
type MyInt2 int
var k MyInt2 = 12
// fmt.Println(k + j)  // ❌ 类型不匹配
fmt.Println(int(k) + j)  // ✅ 需要显式转换
```

---

### 🔗 结构体嵌入 vs 继承

**结构体嵌入**通过匿名字段实现：

```go
type Animal struct {
    Name string
}

type Dog struct {
    Animal  // 嵌入
    Breed string
}
```

**与继承的区别**：
- 嵌入是**组合关系**而非继承关系
- 外层结构体**不会获得内层的类型身份**
- 不能用于类型断言或接口实现
- 强调按需组合和松耦合设计

---

### 🎯 值接收者 vs 指针接收者

| 特性 | 值接收者 `(t T)` | 指针接收者 `(t *T)` |
|:----:|:----------------:|:-------------------:|
| 修改原对象 | ❌ 修改的是副本 | ✅ 可以修改原对象 |
| 拷贝开销 | 有（复制整个对象） | 小（只复制指针） |
| 方法集 | T 只包含值接收者方法 | *T 包含值和指针接收者方法 |
| nil 处理 | 可以调用 | 需要检查 nil |

**自动取址与解址**：
- 调用指针接收者方法时，如果接收者是值类型，编译器自动取址
- 调用值接收者方法时，如果接收者是指针类型，编译器自动解址

---

### 📦 空接口 interface{} 的底层实现

在 Go runtime 里，接口值本质上是 **"类型信息 + 数据指针"** 的二元组。

```go
type eface struct {  // 空接口的底层结构
    _type *_type        // 指向运行时类型信息
    data  unsafe.Pointer // 指向实际数据
}
```

**为什么空接口能接收任意类型？**

因为 `interface{}` 方法集合为空（0 个方法），所以**任何类型都天然实现空接口**。

---

### 🔍 类型断言的两种方式

#### 直接断言（失败会 panic）

```go
v := x.(T)
```

#### Comma-ok 断言（失败不 panic）

```go
v, ok := x.(T)
if ok {
    // 类型断言成功
}
```

**建议**：在不确定类型时，**始终使用 comma-ok 形式**。

---

## 🔤 type 关键字

在 Go 语言中，`type` 是一个重要而且常用的关键字，可以用于定义结构体、类型别名、方法等。

### 📝 类型别名与类型定义

```go
// 类型别名
type MyInt = int

// 类型定义
type MyInt2 int
```

### 🔍 类型判断

```go
switch v := i.(type) {
case int:
    fmt.Println("int 类型，值是", v)
case string:
    fmt.Println("string 类型，值是", v)
default:
    fmt.Println("未知类型")
}
```

---

## 📚 数组

类型 `[n]T` 表示一个数组，它拥有 `n` 个类型为 `T` 的值。

### 📝 声明方法

```go
var a [n]T                    // 基本方式
primes := [6]int{2, 3, 5, 7, 11, 13}  // 字面量声明
balance := [...]float32{1000.0, 2.0}  // 编译器推断长度
```

### 📦 存储特点

- 数组的长度是其类型的一部分，因此数组**不能改变大小**
- 数组元素类型相同，在内存中**连续存储**
- 数组是**值类型**，赋值和传参会**复制整个数组**

### 🔄 遍历方式

```go
for i, v := range arr {
    fmt.Println(i, v)
}
```

---

## 📊 值类型和引用类型

### 📍 值数据类型

变量直接指向存在内存中的值：

- 布尔：`bool`
- 字符串：`string`
- 数值型：`int`、`int8` ~ `int64`、`uint`、`float32`、`float64`、`complex64`、`complex128`
- 字符型：`byte`、`rune`
- 数组、结构体

### 📍 引用数据类型

变量存储的是变量所在的内存地址：

- 指针
- 切片（slice）
- 映射（map）
- 通道（channel）
- 接口（interface）
- 函数（func）

---

## 🔒 常量

常量是一个简单值的标识符，在程序运行时**不会被修改**。

### 📝 定义

```go
const identifier [type] = value
```

- `type` 可以省略，Go 可以通过类型推断
- 常量**不能用 `:=` 语法声明**

### 📈 自增长（iota）

```go
const (
    CategoryBooks = iota    // 0
    CategoryHealth          // 1
    CategoryClothing        // 2
)
```

---

## 🔌 接口类型

在 Go 里，**接口（interface）**是一种**类型**，它定义了一组方法签名，但**不包含实现**。

### 📝 基本定义

```go
type Speaker interface {
    Speak() string
}
```

- 任何类型只要实现了接口中**所有方法**，就**自动**实现了该接口
- 这种实现是**隐式**的，不需要显式声明

### 📦 空接口

```go
var x interface{}
```

空接口 `interface{}` 没有任何方法 → **任何类型**都实现了它，常用于存放任意类型数据。

---

## 🧬 类型系统

### 📋 组成部分

- **基本类型**：整数、浮点数、布尔、字符串
- **复合类型**：数组、切片、结构体、指针、映射
- **接口类型**：定义方法签名
- **类型别名**：为已有类型定义新名称

### 📊 类型元数据

每个类型都有对应的类型描述信息，称为**类型元数据**，构成 Go 语言的**类型系统**。

```go
type _type struct {
    size       uintptr
    ptrdata    uintptr
    hash       uint32
    tflag      tflag
    align      uint8
    fieldalign uint8
    kind       uint8
    // ...
}
```

---

## 📚 总结

| 特性 | 说明 |
|:----:|:----:|
| 变量声明 | `var`、`:=` 两种方式 |
| 基本类型 | 数值、字符、布尔、字符串 |
| 派生类型 | 指针、数组、切片、map、结构体、接口、channel |
| 结构体 | 支持嵌入（组合）、标签、方法绑定 |
| 接口 | 隐式实现、空接口可存任意类型 |
| 类型转换 | 必须显式转换，不支持自动转换 |
| 值 vs 引用 | 数组、结构体是值类型；slice、map、channel 是引用类型 |

**面试重点**：
- struct 可比较的条件
- 值接收者 vs 指针接收者的区别
- 类型别名 vs 类型定义的区别
- 结构体嵌入 vs 继承的区别
- 空接口的底层实现
