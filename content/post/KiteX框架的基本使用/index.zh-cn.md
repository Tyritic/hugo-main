---
date : '2025-07-05T23:54:35+08:00'
draft : false
title : 'KiteX框架的基本使用'
image : ""
categories : ["Kitex框架"]
tags : ["后端开发"]
description : "Kitex框架的初步使用"
math : true
---

## Kitex框架介绍

KiteX [kaɪt’eks] 是字节跳动内部的 Golang 微服务 RPC 框架，已经在 GitHub 上开源，具有高性能、强可扩展的特点，在字节内部已广泛使用。支持 Thrift、[gRPC、Kitex Protobuf](https://bytedance.larkoffice.com/wiki/wikcnCMy5WGHHgP54lxjpwl135b?create_from=create_doc_to_wiki) 协议

## Kitex框架特点

- **高性能**

使用自研的高性能网络库 [Netpoll](https://github.com/cloudwego/netpoll)，性能相较 go net 具有显著优势，性能情况详见 [Kitex-benchmark](https://github.com/cloudwego/kitex-benchmark)。

- **多消息协议**

RPC 消息协议默认支持 **Thrift**、**Kitex** **Protobuf**、**gRPC**。Thrift 支持 Buffered 和 Framed 二进制协议；Kitex Protobuf 是 Kitex 自定义的 Protobuf 消息协议，协议格式类似 Thrift；gRPC 是对 gRPC 消息协议的支持，可以与 gRPC 互通。除此之外，使用者也可以扩展自己的消息协议。

- **多传输协议**

传输协议封装消息协议进行 RPC 互通，传输协议可以额外透传元信息，用于服务治理，Kitex 支持的传输协议有 **TTHeader**、**HTTP2**。TTHeader 可以和 Thrift、Kitex Protobuf 结合使用；HTTP2 目前主要是结合 gRPC 协议使用，后续也会支持 Thrift。

- **多种消息类型**

支持 **PingPong**、**Oneway**、**双向 Streaming**。其中 Oneway 目前只对 Thrift 协议支持，双向 Streaming 支持 gRPC 和 Thrift（[Kitex - Thrift over gRPC streaming 使用说明](https://bytedance.larkoffice.com/wiki/HfwVw8nXWizuNwkxzmTcrzPtnMe) ）。

- **服务治理**

支持服务注册/发现、负载均衡、熔断、限流、重试、监控、链路跟踪、日志、诊断等服务治理模块，以上能力均与内部的基础设施打通，内部使用者直接使用即可，详细可见[用户使用指南](https://bytedance.feishu.cn/wiki/wikcnl64glyMqlUf4V1kJrlrEnb)。

- **代码生成**

Kitex 内置代码生成工具，可支持生成 **Thrift**、**Protobuf** 以及脚手架代码。

- **扩展性**

提供了较多的扩展接口以及默认扩展实现，使用者也可以根据需要自行定制扩展。

## 单RPC服务开发流程

### 环境准备

**kitex tool** 是 Kitex 框架提供的用于生成代码的一个命令行工具。目前，kitex 支持 thrift 和 protobuf 的 IDL，并支持生成一个服务端项目的骨架。kitex 的使用需要依赖于 IDL 编译器确保你已经完成 IDL 编译器的安装。

```bash
go install github.com/cloudwego/kitex/tool/cmd/kitex@latest
```

### 编写idl文件

编写idl文件，构造rpc的请求和响应格式

```
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

按照编码规范，**`namespace go`** 的后面使用PSM（Product, Subsys, Module）

### 生成项目代码

```bash
kitex -module gomodule_name -service p.s.m idl/kitex_greet.thrift
```

- **`module`** ：和go.mod的module名一致
- **`service`** ：指定服务的PSM，PSM可以在output/setting.py中查看
- idl文件路径

生成代码的项目结构

```
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

目录结构会根据P.S.M生成三级目录

其中idl中定义的 **`struct`** 保存在第三目录（M）中，**`client`** 保存在thrift文件中的服务名下

### 编写业务代码

#### 服务端

对于服务端的部分，需要在 **`handler.go`** 中实现我们的服务端逻辑。

生成的 **`handler.go`** ，其中包含了在 idl 内定义的 SayHello 方法。

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

#### 客户端

- 新建客户端
- 指定服务端地址（本地测试直接使用WithHostPosts来进行配置）
- 构造请求
- 调用并打印响应结果

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

### 运行/调用服务

运行前先更新依赖

#### Linux/MacOS

**服务端部分**

目录中的`build.sh`是用来编译的脚本，所以直接运行`sh build.sh`即可。

```Bash
sh build.sh
```

编译完成后，目录中会新增`output`目录：

```C++
output
├── bin // 真正可执行文件所在的目录
│   └── kitex.thrift.example
├── bootstrap.sh // 运行的脚本
├── conf // 配置文件所在目录，每一次编译都会将 conf 目录下的文件复制到这里
│   └── kitex.yml
└── settings.py // 无视它就好
```

执行 **`sh output/bootstrap.sh`** ，就可以看到运行的输出

**客户端部分**

运行客户端代码完成一次调用

```go
go run ./client
```

#### Windows

**服务端部分**

```bash
go run .
```

**客户端部分**

```shell
go run ./client
```

## 多RPC服务的开发流程

### 编写idl文件

将所有服务的idl文件放在一个idl文件夹中

### 为每个idl文件生成代码

有了 IDL 以后便可以通过 kitex 工具生成项目代码了。先回到项目的根目录，为每个idl文件执行kitex 命令

```shell
kitex -module go_module_name idl/item.thrift
```

- **`-module`** ：参数表明生成代码的 `go mod` 中的 module name
- idl文件路径

生成的代码分两部分，一部分是结构体的编解码序列化代码，由 IDL 编译器生成；另一部分由 kitex 工具在前者产物上叠加，生成用于创建和发起 RPC 调用的桩代码。它们默认都在 `kitex_gen` 目录下。

### 生成每个服务的脚手架

为每个RPC 服务分别单独创建目录。再分别进入各自的目录中，执行如下命令生成脚手架代码

```bash
kitex -module go_module_name -service P.S.M -use example_shop/kitex_gen ../../idl/item.thrift
```

- **`-module`** ：参数表明生成代码的 **`go mod`** 中的 **`module name`**
- **`-service`** ：参数表明我们要生成脚手架代码
- **`-use`** ： 参数表示让 kitex 不生成 `kitex_gen` 目录，而使用该选项给出的 **`import path`** 。
- 最后一个参数则为该服务的 IDL 文件

### 编写业务代码

- **`idl`** 中的 **`struct`** ：使用 **`M.NewStructName`** 函数
- **`handler`** 中的函数：使用RPC客户端调用，且每一个函数都含有形参 **`context.Context`**

## 拓展-Kite框架

KiteX框架由Kite框架改进而来，本文仅做基本的使用介绍

### 环境准备

#### 安装代码生成工具

```
go install github.com/kite/kitool/v3@latest
```

#### 安装thrift0.0.2

参考网上教程

### 编写idl文件

同kitex

### 生成脚手架

kite/kitc 没有支持 go mod，因此生成的代码都在 **`$GOPATH`** 下，可选的解决方案：

1. 用 --gopath 指定生成的目录
2. 将你的项目放到 **`$GOPATH/src`** 的指定目录中
3. 将生成的代码拷贝过来覆盖当前目录
4. 在 **`$GOPATH/src`** 的指定目录创建链接到你的项目

```shell
$ kitool new -s [-i idlFilePath] [-cmd Thrift Command] --prefix {Project Path Prefix} webarch.kite.example
```

- `-s`表示本次生成服务端代码
- `-c`表示本次生成客户端代码，在使用`kitool new`时`-s` `-c`至少应该使用其中一个
- `-i`表示 idl 文件的路径
- `-cmd`表示当前开发者机器上的`thrift`命令路径，如果`thrift`命令已经在系统的`$PATH`环境变量中可以省略，另外后续代码统一从服务端生成，因此这个参数也是可以省略的
- `--prefix`表示用于生成`Thrift`代码的包前缀，这个`prefix`是当前项目相对于`$GOPAT``H/src`的相对路径。这样可以生成出`import`路径正确的`Thrift`代码
- `-trans`表示当前需要生成代码的服务的`thrift transport`是什么
  - `取值 ``Buffered`` 或 ``Framed`，默认使用`Buffered`
  - `目标服务如是 archon 的 ``C+``+ ``Thrift`服务，应使用`Framed`，否则服务端有性能问题
- `-proto`表示当前需要生成代码的服务的`thrift protocol`是什么，可以是`Binary`，`Compact`，通常使用`Binary`
- `webarch.kite.example`表示需要初始化的服务的名字，即为`PSM`，服务的唯一标识。
- 更多参数使用说明可通过`kitool help new`查看
