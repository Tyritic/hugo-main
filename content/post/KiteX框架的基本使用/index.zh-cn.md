---
date : '2025-07-05T23:54:35+08:00'
draft : false
title : 'Kitex框架的基本使用'
image : ""
categories : ["Kitex框架"]
tags : ["微服务框架"]
description : "Kitex框架的初步使用"
math : true
---

## 🏗️ Go的项目结构

```text
|--src（源代码）
|	|--app（项目的主要服务，通常使用Hertz框架生成暴露的HTTP服务）
|		|---api
|			|----go_api(HTTP服务)
|		|----faas(faas服务)
|		|----rpc(RPC服务)
|
|	|--biz(业务逻辑代码)
|   |--dao(数据库交互)
|	|--...(其他模块)

```

---

## 🗂️ RPC服务的项目结构

```text
|--rpc（rpc服务集合）
|	|--service_name（单个RPC服务）
|		|---client(RPC客户端)
|		|---dal(数据交互层)
|		|----headlers(RPC服务的具体实现)
|		|----model(数据类型)
|		|----tool(工具层)
|		|----handler.go
|		|----kitex_gen
|	|--biz(业务逻辑代码)
|   |--dao(数据库交互)
|	|--...(其他模块)
```

### 🧩 kitex_gen 代码结构

```text
|-- kitex_gen // Dir for Generated code, which should not be modified. 
|   |-- base
|   |   |-- base.go
|   |   |-- k-base.go
|   |   |-- k-consts.go
|   |-- P
|       |-- S
|           |-- M
│               ├── k-consts.go
│               ├── k-stock.go // kitex 专用的一些拓展内容,FastCodec 序列化代码
│               ├── stock.go // 根据 IDL 生成的编解码文件，由 IDL 编译器生成（结构体桩代码和普通的序列化）
│               └── stockservice // kitex 封装代码主要在这里(Kitex Client/Server的脚手架)
│                   ├── client.go
│                   ├── invoker.go
│                   ├── server.go
│                   └── stockservice.go
```

---

## 🔨 代码框架生成了什么

生成代码主要分为两个部分

- **结构体桩代码 + 普通的序列化代码**
- **创建 Kitex Client/Server 的脚手架**

以 `stock.thrift` 为例

```thrift
namespace go example.shop.stock
include "base.thrift"
struct GetStockReq {
    1: required i64 item_id
}

struct GetStockResp {
    1: required i64 stock,
    2: base.BaseResp baseResp
}

service StockService {
    GetStockResp GetStock(1: GetStockReq req)
}
```

### 📖 结构体桩代码

```go
type Item struct {
	Id          int64  `thrift:"id,1" frugal:"1,default,i64" json:"id"`
	Title       string `thrift:"title,2" frugal:"2,default,string" json:"title"`
	Description string `thrift:"description,3" frugal:"3,default,string" json:"description"`
	Stock       int64  `thrift:"stock,4" frugal:"4,default,i64" json:"stock"`
}

func NewItem() *Item {
	return &Item{}
}

func (p *Item) InitDefault() {
}

func (p *Item) GetId() (v int64) {
	return p.Id
}

func (p *Item) GetTitle() (v string) {
	return p.Title
}

func (p *Item) GetDescription() (v string) {
	return p.Description
}

func (p *Item) GetStock() (v int64) {
	return p.Stock
}
func (p *Item) SetId(val int64) {
	p.Id = val
}
func (p *Item) SetTitle(val string) {
	p.Title = val
}
func (p *Item) SetDescription(val string) {
	p.Description = val
}
func (p *Item) SetStock(val int64) {
	p.Stock = val
}

func (p *Item) String() string {
	if p == nil {
		return "<nil>"
	}
	return fmt.Sprintf("Item(%+v)", *p)
}

var fieldIDToName_Item = map[int16]string{
	1: "id",
	2: "title",
	3: "description",
	4: "stock",
}
```

### 🔍 常见方法

- **`Get/Set`**：作为 Getter 和 Setter，获取字段值
  - 被 option 修饰的字段会被转换为指针，Get 方法获取的是其值
- **`String`**：输出对象的字符串

|                            方法名                            |                  描述&用途                   | CodeGen 内容长度 |
| :----------------------------------------------------------: | :------------------------------------------: | :--------------: |
|                         InitDefault                          |               Frugal 场景需要                |        短        |
|              GetXXXField/SetXXXField/IsSetXXXX               |      GetterSetter，部分 interface 需要       |        短        |
|              Read/ReadFieldX/Write/writeFieldX               |              原生 Apache Codec               |        长        |
|                            String                            |                   Stringer                   |        短        |
|                 DeepEqual/FieldXXXDeepEqual                  |                 set 去重提速                 |        长        |
|                           DeepCopy                           |                RPAL 场景需要                 |        短        |
|                      ThriftService 模板                      |        ServiceInterface 描述接口定义         |        短        |
|             XXXClientFactory、XXXClientProtocol              |       旧的 ThriftClient 代码，不再有用       |       较长       |
|                         XXXProcessor                         |     旧的 Thrift Processor 代码，不再有用     |       较长       |
|                 XXXServiceMethodArgs/Result                  | Thrift 为Method 的入参和返回值单独生成的类型 |        短        |
|                  GetFirstArgument/GetResult                  |              args、result 专用               |        短        |
| FastRead/FastReadFieldX/FastWrite/FastWriteNocopy/BLength/fastWriteFieldX/fieldXLength |               FastCodec 编解码               |        长        |
|                GetOrSetBase/GetOrSetBaseResp                 |      特殊的 Base 相关接口，框架内部使用      |        短        |

### 🛠️ 脚手架

```text
── stockservice // kitex 封装代码主要在这里(Kitex Client/Server的脚手架)
│              ├── client.go // 远程调用
│              ├── invoker.go
│              ├── server.go
│              └── stockservice.go
```

## 🚀 单RPC服务开发流程

### 🛠️ 环境准备

**kitex tool** 是 Kitex 框架提供的用于生成代码的一个命令行工具。目前，kitex 支持 thrift 和 protobuf 的 IDL，并支持生成一个服务端项目的骨架。kitex 的使用需要依赖于 IDL 编译器确保你已经完成 IDL 编译器的安装。

```bash
go install github.com/cloudwego/kitex/tool/cmd/kitex@latest
```

安装成功后，执行 `kitex --version` 可以看到具体版本号的输出（版本号有差异，以 x.x.x 示例）：

```bash
$ kitex --version
vx.x.x
```

### 📄 编写idl文件

编写 idl 文件，构造 rpc 的请求和响应格式

```thrift
namespace go toutiao.kitex.demo
struct HelloRequest {
    1: required string Message,
}
struct HelloResponse {
    1: required string Message,
}
service GreetService {
    HelloResponse SayHello(1: HelloRequest request);
}
```

按照编码规范，**`namespace go`** 的后面使用 **PSM**（Product, Subsys, Module）

### ⚙️ 生成项目代码

```bash
kitex -module gomodule_name -service p.s.m idl/kitex_greet.thrift
```

- **`module`**：和 go.mod 的 module 名一致
- **`service`**：指定服务的 PSM，PSM 可以在 output/setting.py 中查看
- idl 文件路径

生成代码的项目结构

```text
|-- build.sh // scripts for compiling
|-- conf // config files
|   `-- kitex.yml
|-- go.mod // go module file
|-- handler.go // You should implement your business logics in this file.
|-- idl
|   |-- base.thrift
|   `-- kitex_greet.thrift
|-- kitex_gen // Dir for Generated code, which should not be modified. 
|   |-- base
|   |   |-- base.go
|   |   |-- k-base.go
|   |   `-- k-consts.go
|   `-- toutiao
|       `-- kitex
|           `-- demo
|               |-- greetservice
|               |   |-- client.go
|               |   |-- greetservice.go
|               |   |-- invoker.go
|               |   `-- server.go
|               |-- k-consts.go
|               |-- k-kitex_greet.go
|               `-- kitex_greet.go
|-- main.go
`-- script // Some startup scripts required by runtime
    |-- bootstrap.sh
    `-- settings.py
```

目录结构会根据 P.S.M 生成三级目录

其中 idl 中定义的 **`struct`** 保存在第三目录（M）中，**`client`** 保存在 thrift 文件中的服务名下

### 💻 编写业务代码

#### 🖥️ 服务端

对于服务端的部分，需要在 **`handler.go`** 中实现我们的服务端逻辑。

生成的 **`handler.go`**，其中包含了在 idl 内定义的 SayHello 方法。

```go
// GreetServiceImpl implements the last service interface defined in the IDL.
type GreetServiceImpl struct{}

// SayHello implements the GreetServiceImpl interface.
func (s *GreetServiceImpl) SayHello(ctx context.Context, request *demo.HelloRequest) (resp *demo.HelloResponse, err error) {
	// TODO: Your code here...
	fmt.Println("Received:", request.Message)
	resp = &demo.HelloResponse{
		Message: "I am happy to receive your message!",
	}
	return
}
```

#### 👤 客户端

- **新建客户端**
- **指定服务端地址**（本地测试直接使用 WithHostPosts 来进行配置）
- **构造请求**
- **调用并打印响应结果**

```go
package main

import (
   "code.byted.org/kite/kitex/client"
   "code.byted.org/kitex/kitex_example/kitex_gen/toutiao/kitex/demo"
   "code.byted.org/kitex/kitex_example/kitex_gen/toutiao/kitex/demo/greetservice"
   "context"
   "fmt"
)

func main() {
   var opts []client.Option
   // specify the address of the server
   opts = append(opts, client.WithHostPorts("localhost:8888"))
   // construct a client
   cli := greetservice.MustNewClient("kitex.thrift.example", opts...)
   ctx := context.Background()
   // initialize one request 
   req := &demo.HelloRequest{
      Message: "Hello",
   }

   // make a call
   resp, err := cli.SayHello(ctx, req)
   if err != nil {
      fmt.Printf("failed: %s\n", err.Error())
   } else {
      fmt.Printf("OK: %s\n", resp.Message)
   }
}
```

### ▶️ 运行/调用服务

运行前先更新依赖

#### 🐧 Linux/MacOS

**服务端部分**

目录中的 `build.sh` 是用来编译的脚本，所以直接运行 `sh build.sh` 即可。

```bash
sh build.sh
```

编译完成后，目录中会新增 `output` 目录：

```text
output
├── bin // 真正可执行文件所在的目录
│   └── kitex.thrift.example
├── bootstrap.sh // 运行的脚本
├── conf // 配置文件所在目录，每一次编译都会将 conf 目录下的文件复制到这里
│   └── kitex.yml
└── settings.py // 无视它就好
```

执行 **`sh output/bootstrap.sh`**，就可以看到运行的输出

**客户端部分**

运行客户端代码完成一次调用

```bash
go run ./client
```

#### 🪟 Windows

**服务端部分**

```bash
go run .
```

**客户端部分**

```shell
go run ./client
```

---

## 🔧 多RPC服务的开发流程

### 📝 编写idl文件

将所有服务的 idl 文件放在一个 idl 文件夹中

### ⚡ 为每个idl文件生成代码

有了 IDL 以后便可以通过 kitex 工具生成项目代码了。先回到项目的根目录，为每个 idl 文件执行 kitex 命令

```shell
kitex -module go_module_name idl/item.thrift
```

- **`-module`**：参数表明生成代码的 `go mod` 中的 module name
- idl 文件路径

生成的代码分两部分，一部分是结构体的编解码序列化代码，由 IDL 编译器生成；另一部分由 kitex 工具在前者产物上叠加，生成用于创建和发起 RPC 调用的桩代码。它们默认都在 `kitex_gen` 目录下。

### 🏛️ 生成每个服务的脚手架

为每个 RPC 服务分别单独创建目录。再分别进入各自的目录中，执行如下命令生成脚手架代码

```bash
kitex -module go_module_name -service P.S.M -use example_shop/kitex_gen ../../idl/item.thrift
```

- **`-module`**：参数表明生成代码的 **`go mod`** 中的 **`module name`**
- **`-service`**：参数表明我们要生成脚手架代码
- **`-use`**：参数表示让 kitex 不生成 `kitex_gen` 目录，而使用该选项给出的 **`import path`**。
- 最后一个参数则为该服务的 IDL 文件

### 🎯 编写业务代码

- **`idl`** 中的 **`struct`**：使用 **`M.NewStructName`** 函数
- **`handler`** 中的函数：使用 RPC 客户端调用，且每一个函数都含有形参 **`context.Context`**

---

## 🔍 拓展-Kite框架

KiteX 框架由 Kite 框架改进而来，本文仅做基本的使用介绍

### 📦 环境准备

#### 📥 安装代码生成工具

```bash
go install github.com/kite/kitool/v3@latest
```

#### 🔧 安装thrift0.0.2

参考网上教程

### 💾 编写idl文件

同 kitex

### 🔨 生成脚手架

kite/kitc 没有支持 go mod，因此生成的代码都在 **`$GOPATH`** 下，可选的解决方案：

1. 用 --gopath 指定生成的目录
2. 将你的项目放到 **`$GOPATH/src`** 的指定目录中
3. 将生成的代码拷贝过来覆盖当前目录
4. 在 **`$GOPATH/src`** 的指定目录创建链接到你的项目

```shell
$ kitool new -s [-i idlFilePath] [-cmd Thrift Command] --prefix {Project Path Prefix} webarch.kite.example
```

- **`-s`** 表示本次生成服务端代码
- **`-c`** 表示本次生成客户端代码，在使用 `kitool new` 时 `-s` `-c` 至少应该使用其中一个
- **`-i`** 表示 idl 文件的路径
- **`-cmd`** 表示当前开发者机器上的 `thrift` 命令路径，如果 `thrift` 命令已经在系统的 `$PATH` 环境变量中可以省略，另外后续代码统一从服务端生成，因此这个参数也是可以省略的
- **`--prefix`** 表示用于生成 `Thrift` 代码的包前缀，这个 prefix 是当前项目相对于 `$GOPATH/src` 的相对路径。这样可以生成出 import 路径正确的 Thrift 代码
- **`-trans`** 表示当前需要生成代码的服务的 `thrift transport` 是什么
  - 取值 `Buffered` 或 `Framed`，默认使用 `Buffered`
  - 目标服务如是 archon 的 `C++` `Thrift` 服务，应使用 `Framed`，否则服务端有性能问题
- **`-proto`** 表示当前需要生成代码的服务的 `thrift protocol` 是什么，可以是 `Binary`，`Compact`，通常使用 `Binary`
- `webarch.kite.example` 表示需要初始化的服务的名字，即为 `PSM`，服务的唯一标识。
- 更多参数使用说明可通过 `kitool help new` 查看
