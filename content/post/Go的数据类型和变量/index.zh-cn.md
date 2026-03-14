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

**💡 面试要点：make 和 new 的区别？**

**回答：**

**`make`** 和 **`new`** 都是用于内存分配的内建函数，但使用场景不同：

| 特性 | **`make`** | **`new`** |
|:----:|:----------:|:---------:|
| 用途 | 初始化 slice、map、channel | 分配任意类型的内存 |
| 返回值 | 返回初始化后的值（非指针） | 返回指向零值的指针 |
| 初始化 | 会初始化内部结构 | 只分配内存，不初始化 |
| 零值 | 返回可用的数据结构 | 返回指针指向零值 |

**示例：**

```go
// make：初始化 slice
s := make([]int, 5, 10)  // 返回 []int，已初始化

// make：初始化 map
m := make(map[string]int)  // 返回 map[string]int，已初始化

// make：初始化 channel
ch := make(chan int)  // 返回 chan int，已初始化

// new：分配内存
p := new(int)  // 返回 *int，指向零值 0
fmt.Println(*p)  // 输出：0

// new：分配结构体
type Person struct {
    Name string
    Age  int
}
person := new(Person)  // 返回 *Person
fmt.Println(person.Name)  // 输出：""（零值）
```

**关键区别：**
- **`make`** 只能用于 slice、map、channel，返回初始化后可直接使用的值
- **`new`** 可用于任何类型，返回指针，指向该类型的零值

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

**💡 面试要点：int 和 int32 有什么区别？**

**位宽与取值范围**

- **`int`**：平台相关
  - 64 位架构通常是 **`int64`**（64-bit）
  - 32 位架构是 **`int32`**（32-bit）
  
- **`int32`**：永远是 32 位有符号整数

**选择建议**

- 选 **`int`** 更适合索引和通用计数
- 选 **`int32`** 更适合需要固定宽度的协议和数据结构

**示例：**

```go
import "unsafe"

func main() {
    var a int
    var b int32
    
    fmt.Println(unsafe.Sizeof(a)) // 8（64位系统）
    fmt.Println(unsafe.Sizeof(b)) // 4
}
```

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

**💡 面试要点：rune 和 byte 有什么区别？**

**类型定义：**

- **`byte`**：**`uint8`** 的别名，占用 1 字节
- **`rune`**：**`int32`** 的别名，占用 4 字节

**使用场景：**

- **`byte`**：处理 **ASCII 字符**或二进制数据
- **`rune`**：处理 **Unicode 字符**（如中文、emoji）

**示例：**

```go
s := "你好"

// byte 方式遍历（按字节）
for i := 0; i < len(s); i++ {
    fmt.Printf("%d: %x\n", i, s[i])
}
// 输出：
// 0: e4
// 1: bd
// 2: a0
// 3: e5
// 4: a5
// 5: bd

// rune 方式遍历（按字符）
for i, r := range s {
    fmt.Printf("%d: %c\n", i, r)
}
// 输出：
// 0: 你
// 3: 好
```

**总结：**
- 处理英文用 **`byte`** 足够
- 处理中文、emoji 等多字节字符，必须用 **`rune`**

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

**💡 面试要点：Go string 的底层实现原理**

Go 的字符串底层是一个**只读的字节数组**，通过 **`StringHeader`** 结构体描述：

- **`Data`**：指向底层字节数组的指针
- **`Len`**：字符串的字节长度（不是字符数）

**关键特性：**

1. **不可变性**：字符串内容不能修改，任何修改都会创建新字符串
2. **零拷贝切片**：字符串切片 **`s[i:j]`** 不复制数据，只创建新的 **`StringHeader`**
3. **字节长度**：**`len(s)`** 返回字节数，不是字符数

**示例：**

```go
s := "hello"
// 底层结构：
// Data -> ['h', 'e', 'l', 'l', 'o']
// Len  -> 5

// 切片操作（零拷贝）
sub := s[1:3]  // "el"
// sub 的 Data 仍指向原数组，只是偏移了 1 字节
```

**⚠️ 注意：中文字符串**

```go
s := "你好"
fmt.Println(len(s))  // 输出：6（UTF-8 编码，每个中文 3 字节）

// 获取字符数
fmt.Println(utf8.RuneCountInString(s))  // 输出：2
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

**💡 面试要点：Go 的参数传递是值传递还是引用传递？**

**回答：Go 只有值传递。**

**值传递**：函数调用时，实参的值被复制给形参，形参是实参的副本。

**示例：**

```go
// 传递 int（值类型）
func modifyInt(x int) {
    x = 100  // 修改的是副本
}
func main() {
    a := 10
    modifyInt(a)
    fmt.Println(a)  // 输出：10（原值未变）
}

// 传递指针（仍然是值传递，只是复制的是指针值）
func modifyPointer(x *int) {
    *x = 100  // 通过指针修改原值
}
func main() {
    a := 10
    modifyPointer(&a)
    fmt.Println(a)  // 输出：100（原值被修改）
}
```

**关键理解：**
- 传递指针时，**指针本身被复制**，但两个指针指向同一地址
- slice、map、channel 虽然表现得像引用传递，但本质仍是值传递（传递的是底层数据结构的副本）

**💡 面试要点：Go 有哪些引用类型？**

Go 的引用类型包括：

- **slice**：包含指向底层数组的指针
- **map**：指向哈希表的指针
- **channel**：指向通道结构的指针
- **interface**：包含类型信息和数据指针
- **func**：函数类型
- **指针**：**`*T`** 类型

**注意**：虽然叫"引用类型"，但传递时仍然是值传递（复制指针值）。

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

**💡 面试要点：for range 的底层原理是什么？**

**回答：**

**`for range`** 是 Go 提供的迭代语法糖，底层实现：

**1. 对于 slice/array**

```go
// 源代码
for i, v := range arr {
    // ...
}

// 编译器展开后（伪代码）
len := len(arr)
for i := 0; i < len; i++ {
    v := arr[i]  // v 是副本
    // ...
}
```

**2. 对于 map**

- 使用 **`runtime.mapiterinit`** 初始化迭代器
- 使用 **`runtime.mapiternext`** 获取下一个元素
- 遍历顺序是**随机的**

**3. 对于 string**

- 按 **rune** 遍历，不是按字节
- **`i`** 是字节索引，**`v`** 是 rune 值

**⚠️ 常见陷阱：**

```go
// 陷阱1：v 是副本，修改不影响原数组
arr := []int{1, 2, 3}
for i, v := range arr {
    v = 100  // 只修改副本，不影响原数组
}
fmt.Println(arr)  // [1 2 3]

// 正确做法
for i := range arr {
    arr[i] = 100  // 直接修改原数组
}

// 陷阱2：循环变量复用
var funcs []func()
for i := 0; i < 3; i++ {
    funcs = append(funcs, func() { fmt.Println(i) })
}
for _, f := range funcs {
    f()  // 输出：3 3 3（i 被复用）
}

// 正确做法
for i := 0; i < 3; i++ {
    i := i  // 创建局部变量
    funcs = append(funcs, func() { fmt.Println(i) })
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

### 💡 底层实现原理

Go 的接口分为两种：

**1. 空接口（eface）**

```go
type eface struct {
    _type *_type        // 类型信息
    data  unsafe.Pointer // 数据指针
}
```

<div align="center">
  <img src="eface修改.png" alt="eface" width="60%">
</div>

**2. 带方法的接口（iface）**

```go
type iface struct {
    tab  *itab           // 接口表（包含类型和方法信息）
    data unsafe.Pointer  // 数据指针
}

type itab struct {
    inter *interfacetype // 接口类型信息
    _type *_type         // 具体类型信息
    hash  uint32         // 类型哈希值
    _     [4]byte
    fun   [1]uintptr     // 方法表
}
```
<div align="center">
  <img src="iface修改.png" alt="eface" width="60%">
</div>

**关键区别：**
- **`eface`**：只记录类型和数据，没有方法表
- **`iface`**：额外记录接口类型和方法表，用于方法调用

### 💡 nil interface 和空 interface 的区别

**回答：**

这是一个常见的陷阱问题。

**nil interface**：接口值本身为 **`nil`**
- **`_type`** 为 **`nil`**
- **`data`** 为 **`nil`**

**空 interface**：接口值不为 **`nil`**，但存储的值为 **`nil`**
- **`_type`** 不为 **`nil`**（有类型信息）
- **`data`** 为 **`nil`**

**示例：**

```go
type Person struct {
    Name string
}

func main() {
    // nil interface
    var i interface{}
    fmt.Println(i == nil)  // true
    
    // 空 interface（陷阱！）
    var p *Person = nil
    var j interface{} = p
    fmt.Println(j == nil)  // false！
    // j 的 _type 不为 nil（是 *Person）
    // j 的 data 为 nil
}
```

**正确判断方式：**

```go
func IsNil(i interface{}) bool {
    if i == nil {
        return true
    }
    v := reflect.ValueOf(i)
    switch v.Kind() {
    case reflect.Ptr, reflect.Slice, reflect.Map, reflect.Chan, reflect.Func, reflect.Interface:
        return v.IsNil()
    }
    return false
}
```

### 💡 两个 interface 可以比较

**回答：可以比较，但有条件。**

**比较规则：**

1. **类型不同**：直接返回 **`false`**
2. **类型相同**：比较动态值
3. **动态值不可比较**：会 **`panic`**

**示例：**

```go
var a interface{} = []int{1, 2, 3}
var b interface{} = []int{1, 2, 3}

// fmt.Println(a == b)  // panic: comparing uncomparable type []int
```

**可比较的类型：**
- 基本类型：**`int`**、**`string`**、**`bool`** 等
- 指针、**`channel`**
- 结构体（所有字段可比较）
- 数组（元素可比较）

**不可比较的类型：**
- **`slice`**、**`map`**、**`func`**

**💡 面试要点：interface 的使用场景有哪些？**

**1. 空接口作为通用容器**

```go
func PrintAny(v interface{}) {
    fmt.Println(v)
}
```

**2. 接口作为函数参数（多态）**

```go
type Shape interface {
    Area() float64
}

func PrintArea(s Shape) {
    fmt.Println(s.Area())
}
```

**3. 接口组合**

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type ReadWriter interface {
    Reader
    Writer
}
```

**4. 接口断言（类型判断）**

```go
func Handle(v interface{}) {
    switch val := v.(type) {
    case int:
        fmt.Printf("int: %d\n", val)
    case string:
        fmt.Printf("string: %s\n", val)
    default:
        fmt.Printf("unknown type: %T\n", val)
    }
}
```

**最佳实践：**
- **小接口**：接口方法越少越好（1-3 个方法）
- **接收接口，返回结构体**：函数参数用接口，返回值用具体类型
- **避免空接口滥用**：空接口会丢失类型安全

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
