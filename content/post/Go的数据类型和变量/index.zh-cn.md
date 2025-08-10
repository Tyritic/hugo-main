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
## 变量的声明方式

声明变量的一般形式是使用 **`var`** 关键字，有以下使用方法

- 指定变量类型，声明后若不赋值，使用默认值。

  ```go
  var var_name var_type
  ```

- 根据值自行判定变量类型（类型推导）

  ```go
  var v_name = value
  ```

- 省略 **`var`** , 使用初始化声明 **`:=`** 

  - **`:=`** 左侧的变量不应该是已经声明过的，否则会导致编译错误。
  - 在定义变量 a 之前使用它，则会得到编译错误 undefined: a。
  - 声明了一个局部变量却没有在相同的代码块中使用它，同样会得到编译错误
  - 只可以在函数内使用，不能用于声明全局变量


```go
v_name := value
```

示例代码

```go
package main


import "fmt"


func main() {
        //第一种 使用默认值
        var a int
        fmt.Printf("a = %d\n", a)


        //第二种
        var b int = 10
        fmt.Printf("b = %d\n", b)


        //第三种 省略后面的数据类型,自动匹配类型
        var c = 20
        fmt.Printf("c = %d\n", c)


        //第四种 省略var关键字
        d := 3.14
        fmt.Printf("d = %f\n", d)
}
```

- 多变量声明方式

  - 对于全局变量可以采用分解的方式来一次性声明

    ```go
    var x, y int 
    var ( // 分解的写法,一般用于声明全局变量
            a int
            b bool
    )
    ```

  - 也可以直接使用单变量的三种方式

    ```go
    var c, d int = 1, 2
    var e, f = 123, "liudanbing"
    g, h := 123 //只能在函数体内使用
    ```

### 命名规则

- 一个名字必须以一个字母（Unicode 字母）或下划线开头，后面可以跟任意数量的字母、数字或下划线
- 大写字母和小写字母是不同的：heapSort 和 Heapsort 是两个不同的名字
- Go 语言程序员推荐使用**驼峰式**命名，当名字由几个单词组成时优先使用大小写分隔，而不是优先用下划线分隔

## 基本数据类型

Go的数据类型分类与Java类似分为基本数据类型和派生数据类型

- 基本数据类型
  - 数值型
    - 整数型
    - 浮点型
  - 字符型（没有专门的字符型，使用 **`byte`** 来保存字符）
  - 布尔型：**`bool`**
  - 字符串：**`String`**
- 派生数据类型
  - 指针
  - 数组
  - 结构体
  - 管道
  - 函数
  - 切片
  - 接口
  - map

### 数值型

#### 整数型

整数型用于存储整数数值

有符号整数

| 类型  | 有无符号 | 占用存储空间 |       数据范围       |
| :---: | :------: | :----------: | :------------------: |
| int8  |    有    |   1个字节    |     $-128$~$127$     |
| int16 |    有    |   2个字节    | $-2^{15}$~$2^{15}-1$ |
| int32 |    有    |   3个字节    | $-2^{31}$~$2^{31}-1$ |
| int64 |    有    |   4个字节    | $-2^{63}$~$2^{63}-1$ |

无符号整数

|  类型  | 有无符号 | 占用存储空间 |    数据范围    |
| :----: | :------: | :----------: | :------------: |
| uint8  |    无    |   1个字节    |   $0$~$255$    |
| uint16 |    无    |   2个字节    | $0$~$2^{16}-1$ |
| uint32 |    无    |   3个字节    | $0$~$2^{32}-1$ |
| uint64 |    无    |   4个字节    | $0$~$2^{64}-1$ |

其他整数类型

| 类型 | 有无符号 |          占用存储空间          |                           数据范围                           |            注意事项             |
| :--: | :------: | :----------------------------: | :----------------------------------------------------------: | :-----------------------------: |
| int  |    有    | 32位系统4个字节64位系统8个字节 | $-2^{31}$~$2^{31}-1$（32位系统）<br>$-2^{63}$ ~$2^{63}-1$（64位系统） |                                 |
| uint |    无    | 32位系统4个字节64位系统8个字节 |  $0$~$2^{32}-1$（32位系统）<br/>$0$ ~$2^{64}-1$（64位系统）  |                                 |
| rune |    有    |            3个字节             |                     $-2^{31}$~$2^{31}-1$                     | 等价 int32，表示一个 Unicode 码 |
| byte |    无    |            1个字节             |                          $0$~$255$                           |     当要存储字符时选用byte      |

Golang中的默认整数类型为 **`int`**

#### 浮点数型

|  类型   | 占用存储空间 | 表数范围 |
| :-----: | :----------: | :------: |
| float32 |    4字节     |          |
| float64 |    8字节     |          |

注意事项

- Golang 浮点类型有固定的范围和字段长度，不受具体 OS(操作系统)的影响。
- Golang 的浮点型默认声明为 **`float64`** 类型。

### 字符型

Golang 中没有专门的字符类型，如果要存储单个字符(字母)，一般使用 **`byte`** 来保存。字符串就是一串固定长度的字符连接起来的字符序列。Go的字符串是由单个字节连接起来的。也就是说对于传统的字符串是由字符组成的，而Go的字符串不同，它是由字节组成的。

Go中的字符型使用 **`byte`** 来保存，字符使用 **`' '`** 括起来

```go
var x byte ='a'
```

可以使用转义字符将字符变成特殊字符常量，常见的转义字符如下

- **`\t`** ：制表符
- **`\n`** ：换行符
- **`\r`** ：一个回车

注意事项

- Go的字符采用UTF-8编码，字符本质上是一个整数，直接输出时是输出字符的UTF-8码值
- 使用格式化输出 **`%c`** 才能输出字符值

### 布尔类型

布尔类型使用 **`bool`** 存储，大小为1个字节，只允许值为 **`true`** 和 **`false`**

### 字符串类型

字符串就是一串固定长度的字符连接起来的字符序列。Go 的字符串是由单个字节连接起来的。Go语言的字符串的字节使用 UTF-8 编码标识 Unicode 文本。字符串的编码为UTF8 ，源代码中的文本字符串通常被解释为采用 UTF8 编码的 Unicode 码点（rune）序列。因此字符串可以包含任意的数据

#### 底层原理

```Go
type StringHeader struct {
    Data uintptr
    Len  int
}
```

注意事项

- 在Go中字符串是不可变的，类似Java
- 表示方法
  - 使用双引号 **`“ ”`** 表示字符串会识别转义字符
  - 使用反引号 **`· ·`** 以字符串的原生形式输出，包括换行和特殊字符，可以实现防止攻击、输出源代码等效果
- 字符串之间使用 **`+`** 进行拼接
- 对于长字符串使用分行拼接处理，将 **`+`** 保留在上一行

## 作用域

Go 语言中变量可以在三个地方声明

- 函数内定义的变量
- 函数外定义的变量
- 函数定义中的变量

作用域分为以下几种

- 局部变量：在函数体内声明的变量的作用域只在函数体内，参数和返回值变量也是局部变量
- 全局变量：在函数体外声明的变量可以在整个包甚至外部包（被导出后）使用可以在任何函数中使用
- 形式参数：形式参数会作为函数的局部变量来使用

## 基本数据类型的默认值

在 go 中，数据类型都有一个默认值，当没有赋值时，就会保留默认值，在go 中，默认值又叫零值。

| 数据类型 | 默认值 |
| :------: | :----: |
|   int    |   0    |
|  float   |   0    |
|  string  |   ""   |
|   bool   | false  |

## 基本数据类型之间的相互转换

Go和Java不同，Go不支持数据类型的自动转换需要显式自动转换

语法格式

```go
var i dataType
var j =newType(i)
```

### 基本数据类型和string之间的转换

#### 基本数据类型转string

- **`fmt.Sprintf("%参数",表达式)`**
- 使用 **`strconv`** 包中的函数
  - **`func FormatBool(b bool) string`**
  - **`func FormatInt(i int64,base int) string`**
  - **`func FormatFloat(f float64,fmt byte,prec,bitSize int) string`**

#### string转基本类型

- 使用 **`strcov`** 包中的函数
  - **`func ParseBool(str string) (value bool, err error)`**
  - **`func ParseFloat(s string, bitSize int) (f float64,er error)`**
  - **`func Parselnt(s string, base int, bitSize int) ( int64,err error)`**
  - **`func ParseUint(s string, b int, bitSize int) (n uint64 err error)`**

## 指针

类似于C++，Go保留了指针

指针保存了值的内存地址，其零值为 **`nil`** 。

- 取址符：**`&`** 操作符生成一个指向其操作数的指针，获取地址。
- 解引用：**`*`** 操作符表示指针指向的底层值。

{{<notice tip>}}

- 需要修改原值（引用语义）：如果希望函数里对参数的修改**直接作用到调用方的变量**，就需要传指针
- 避免复制大对象（性能考虑）：Go 的值传递会复制一份参数，如果结构体很大（例如有很多字段或大切片），复制成本高，就可以传指针来避免拷贝。

{{</notice>}}

## 结构体

一个结构体（ **`struct`** ）就是一组 字段（field）。

### 创建和初始化

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

Go的结构体支持匿名字段，用于在一个结构体中插入另一个结构体，可以用于模拟实现继承行为

**结构体常通过指针传递，避免复制整个结构体，提高性能。**

### 注解

虽然 Go 本身语法中没有类似 Java 中的 **`@Annotation`** 的注解机制，但结构体字段可以使用反引号（`）添加 tag，以传递元信息（meta info）给反射或其他工具使用。

- 标签必须用 **反引号（`）** 包裹。
- 每个 tag 是 **`key:"value"`** 形式，多个 tag 之间以空格分隔。
- 每个 key 应唯一。

```go
type User struct {
    ID    int    `json:"id" db:"user_id" validate:"required"`
    Name  string `json:"name" db:"username" comment:"用户姓名"`
    Email string `json:"email,omitempty" validate:"email"`
}
```

### 方法绑定

利用方法绑定可以实现类似Java的成员方法的效果。**方法绑定** 指的是某个方法被**绑定（关联）到某个类型的值（value）或指针（pointer）上，从而可以通过该值或指针来调用这个方法**。

```go
func (var_name varType) func_name(parameter_type parmeterlist) return_type {
    
}
```

- 接收者是值：传的是**副本**，原值不受影响。可以通过 **`Person`** 值或 **`*Person`** 调用
- 接收者是指针：可以修改原对象内容

### JSON解析

Go通常使用使用标准库中的 **`import "encoding/json"`** 做序列化和反序列化

- 序列化：Go对象 → JSON字符串
- 反序列化：JSON字符串 → Go对象

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
	data, err := json.Marshal(u)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(data)) // 输出：{"name":"Alice","age":30}
    
    // 反序列化
    jsonStr := `{"name":"Bob","age":25}`

	var u User
	err := json.Unmarshal([]byte(jsonStr), &u)
	if err != nil {
		panic(err)
	}
	fmt.Println(u.Name, u.Age) // 输出：Bob 25
}
```

Json Tag属性

- **`json:"name,varType"`** ：将字段编码为 **`name`** ，数据类型为varType
- **`json:"name,omitempty"`** ：若字段为零值则忽略
- **`json:"-"`** ：忽略该字段，不参与序列化

相比 Go 的官方 **`encoding/json`**，**`jsoniter`** 性能更高，**通常快 2～5 倍**，且完全兼容原有代码接口（几乎无需改动即可替换）。

```go
import jsoniter "github.com/json-iterator/go"

var json = jsoniter.ConfigCompatibleWithStandardLibrary

// 替代 encoding/json 的 Marshal 和 Unmarshal
data, _ := json.Marshal(obj)
json.Unmarshal(data, &obj)
```



## type关键字

在 Go 语言中，type是一个重要而且常用的关键字。它可以用于定义结构体、类型别名、方法等。

可以用于定义类型别名

```Go
//定义类型别名 - 别名实际上是为了更好的理解代码
type MyInt = int
var i MyInt = 12
var int = 8
fmt.Println(i + j)
fmt.Printf("%T", i)    //int

//类型定义
type MyInt int
var i MyInt = 12
var j int = 8    //j不能和i直接相加，因为类型不同
fmt.Println(int(i) + j)    //需要强制类型转换
fmt.Printf("%T", i)        //main.MyInt
```

在编译的时候，类型别名会被直接替换成对应类型。

可以用于类型判断

```go
switch v := i.(type) {
    case int:
        fmt.Println("int 类型，值是", v)
    case string:
        fmt.Println("string 类型，值是", v)
    case bool:
        fmt.Println("bool 类型，值是", v)
    default:
        fmt.Println("未知类型")
    }
```



## 数组

类型 [n]T 表示一个数组，它拥有 `n` 个类型为 `T` 的值。

### 声明方法

```Go
var a [n]T //基本方式
primes := [6]int{2, 3, 5, 7, 11, 13} //字面量声明
balance := [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0} //不确定数组长度
```

### 存储特点

- 数组的长度是其类型的一部分，因此数组不能改变大小。
- 数组元素类型相同
- 数组在内存中连续存储
- 如果数组长度不确定，可以使用 `...` 代替数组的长度，编译器会根据元素个数自行推断数组的长度
- 数组是值类型，并不是隐式的指向第一个元素的指针（比如 C 语言的数组），而是一个完整的值赋值和传参会复制整个数组

### 遍历方式

使用 **`range`** 循环进行遍历，其中第一个返回值为数组下标，第二个返回值为数组值

```Go
for i, v := range b {     // 通过数组指针迭代数组的元素
    fmt.Println(i, v)
}
```

## 值数据类型和引用数据类型

数据类型分为值数据类型和引用数据类型

- 值数据类型：这种类型的变量直接指向存在内存中的值
- 引用数据类型：这种类型的变量存储的是变量所在的内存地址

常见的值数据类型有

- 布尔：bool
- 字符串：string
- 数值型
  - 有符号整数
    - **`int`**  
    - **`int8`**  
    - **`int16`**  
    - **`int32`**  
    - **`int64`**
  - 无符号整数
    - **`uint`** 
    - **`uint8`** 
    - **`uint16`** 
    - **`uint32`** 
    - **`uint64`** 
    - **`uintptr`**
  - 字符型：**`byte`** // uint8 的别名 
  - **`rune`** // int32 的别名，表示一个 Unicode 码位
  - 浮点型
    - **`float32`** 
    - **`float64`**
  - 虚数
    - **`complex64`** 
    - **`complex128`**
- 数组
- 结构体

常见的引用数据类型

- 指针
- 切片
- 映射

## 常量

常量是一个简单值的标识符，在程序运行时，不会被修改的量。

### 定义

常量中的数据类型只可以是布尔型、数字型（整数型、浮点型和复数）和字符串型。

```go
const identifier [type] = value
```

- 其中type可以省略，go可以通过类型推断
- 常量不能用 **`:=`** 语法声明。

### 自增长

在 Go 中，一个方便的习惯就是使用 **`iota`** 标示符，它简化了常量用于增长数字的定义，给以上相同的值以准确的分类。

```go
const (
    CategoryBooks = iota // 0
    CategoryHealth       // 1
    CategoryClothing     // 2
)
```

底层原理：当你在一个 **`const`** 组中仅仅有一个标示符在一行的时候，它将使用增长的 **`iota`** 取得前面的表达式并且再运用它

## 接口类型

在 Go 里，**接口（interface）** 是一种**类型**，它定义了一组方法签名（方法集合），但**不包含实现**。
 任何实现了接口中所有方法的类型，都被认为**实现了该接口**

### 基本定义

```go
type Speaker interface {
    Speak() string
}
```

- 这个接口要求实现一个 **`Speak() string`** 方法。
- 任何类型只要实现了这个方法，就**自动**实现了 **`Speaker`** 接口。

### 空接口

```go
var x interface{}
```

空接口 **`interface{}`** 没有任何方法 → **任何类型**都实现了它常用于存放任意类型数据

## 类型系统

### 组成部分

- **基本类型：** 包括整数类型（如 **`int`** 、**`int8`** 、**`int16`** 等）、浮点数类型（如 **`float32`** 、**`float64`** ）、布尔类型（ **`bool`** ）、字符串类型（ **`string`** ）等。
- **复合类型：**
  - 数组：具有固定长度的相同类型元素的序列。
  - 切片：可以动态增长或收缩的元素序列。
  - 结构体：将不同类型的数据组合在一起形成一个新的类型。
  - 指针：用于指向其他变量的地址。
  - 映射（字典）：存储键值对的数据结构。
- **接口类型：** 定义了一组方法签名，具体的类型可以实现这些接口。
- **类型别名：** 可以为已有的类型定义一个新的名称。

### 类型元数据

不管是内置类型还是自定义类型都有对应的类型描述信息，称为它的 “类型元数据”。而且每种类型的元数据都是全局唯一的，这些类型元数据构成了 Go 语言的 “类型系统”

每个类型元数据的 Header被放到了 **`runtime._type`** 结构体

```Go
type _type struct {
    size        uintptr
    ptrdata     uintptr
    hash        uint32
    tflag       tflag
    align       uint8
    fieldalign  uint8
    kind        uint8
    // ......
}
```

在 **`_type`** 之后存储的是各种类型额外需要描述的信息 例如 slice 的类型元数据在 **`_type`** 结构体后面记录着一个 **`*type`**，指向其存储的元素的类型元数据。如果是 string 类型的 slice，下面这个 **`*_type`** 类型的指针就指向 string 类型的元数据。

如果是自定义类型，在其它描述信息的后面还会有一个 uncommontype 结构体。

```go
type uncommontype struct {
    pkgpath   nameOff    // 记录类型所在的包路径
    mcount    uint16     // 记录了该类型关联到多少个方法
    _         uint16
    moff      uint32     // 记录的是这些方法元数据组成的数组相对于这个uncommontype结构体偏移了多少字节
    _         uint32
}
```

### 类型断言

类型断言（Type Assertion）是 Go 语言里**从接口类型变量里取出具体类型值**的一种语法。

因为在 Go 中，**`interface{}`**（或其他接口类型）可以存放**任意类型的值**，但是取出来时如果想用它的具体类型功能，就要用类型断言。

基本语法

```go
value, ok := x.(T)
```

- **`x`** 是一个接口类型变量（比如 **`interface{}`**）。
- **`T`** 是你要断言的具体类型。

如果 **`x`** 的底层类型是 **`T`**：

- **`value`** 会得到类型为 **`T`** 的值
- **`ok`** 为 **`true`**

如果不是：

- **`value`** 是 **`T`** 的零值
- **`ok`** 为 **`false`**

断言可以不带ok，这种方式如果断言失败会直接 **`panic`**，所以**建议在不确定类型时加 `ok` 判断**
