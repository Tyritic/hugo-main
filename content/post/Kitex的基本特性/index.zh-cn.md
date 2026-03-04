---
date : '2025-07-13T22:20:26+08:00'
draft : false
title : 'Kitex的基本特性'
image : ""
categories : ["Kitex框架"]
tags : ["后端开发"]
description : "Kitex的基本特性"
math : true
---

## 📁 Go的项目结构

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

### 📂 kitex_gen 代码结构

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

## 🔧 代码框架生成了什么

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

### 📋 结构体桩代码

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

### 🔧 常见方法

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

### 🏗️ 脚手架

```text
── stockservice // kitex 封装代码主要在这里(Kitex Client/Server的脚手架)
│              ├── client.go // 远程调用
│              ├── invoker.go
│              ├── server.go
│              └── stockservice.go
```

---

## 📡 消息类型

Kitex 支持三种主要的消息类型：**PingPong**、**Oneway** 和 **Streaming**。不同的消息类型适用于不同的业务场景，可以根据实际需求灵活选择。

### 🎯 消息类型概述

| 消息类型 | 说明 |
|---------|------|
| **PingPong** | 客户端发起一个请求后会等待一个响应才可以进行下一次请求 |
| **Oneway** | 客户端发起一个请求后不等待一个响应 |
| **Streaming** | 客户端发起一个或多个请求，等待一个或多个响应 |

### 📊 协议支持矩阵

Kitex 支持的消息类型、序列化协议和传输协议组合如下：

| 消息类型 | 序列化协议 | 传输协议 |
|---------|-----------|---------|
| **PingPong** | Thrift / Protobuf | TTHeader / HTTP2(gRPC) |
| **Oneway** | Thrift | TTHeader |
| **Streaming** | Thrift / Protobuf | HTTP2(gRPC) |

---

## 🛠️ Thrift 消息类型

Kitex 支持基于 **Thrift** 协议的 PingPong、Oneway 消息类型；同时支持 Thrift Streaming over HTTP2。

### 📝 IDL 定义示例

首先，我们需要定义 Thrift IDL 文件来描述接口和数据结构：

```thrift
namespace go echo

struct Request {
    1: string Msg
}

struct Response {
    1: string Msg
}

service EchoService {
    Response Echo(1: Request req); // pingpong method
    oneway void VisitOneway(1: Request req); // oneway method
}
```

### 📁 生成的代码组织结构

使用 Kitex 工具生成代码后，目录结构如下：

```text
.
└── kitex_gen
    └── echo
        ├── echo.go
        ├── echoservice
        │   ├── client.go
        │   ├── echoservice.go
        │   ├── invoker.go
        │   └── server.go
        ├── k-consts.go
        └── k-echo.go
```

### 🏗️ Server 处理代码

以下是 Server 端的处理代码示例：

```go
package main

import (
    "context"

    "xx/echo"
    "xx/echo/echoservice"
)

type handler struct {}

func (handler) Echo(ctx context.Context, req *echo.Request) (r *echo.Response, err error) {
    // 业务逻辑处理
    return &echo.Response{ Msg: "world" }, err
}

func (handler) VisitOneway(ctx context.Context, req *echo.Request) (err error) {
    // Oneway 方法处理，无返回值
    return nil
}

func main() {
    svr := echo.NewServer(handler{})
    err := svr.Run()
    if err != nil {
        panic(err)
    }
}
```

### 🔌 PingPong Client 代码

PingPong 方式的客户端调用示例：

```go
package main

import (
    "context"
    "fmt"

    "xx/echo"
    "xx/echo/echoservice"

    "github.com/cloudwego/kitex/client"
)

func main() {
    // 创建客户端
    cli, err := echoservice.NewClient("destServiceName", client.WithHostPorts("0.0.0.0:8888"))
    if err != nil {
        panic(err)
    }
    
    // 构造请求
    req := echo.NewRequest()
    req.Msg = "hello"
    
    // 发送请求并等待响应
    resp, err := cli.Echo(context.Background(), req)
    if err != nil {
        panic(err)
    }

    fmt.Println(resp.Msg)
    // resp.Msg == "world"
}
```

### ⚡ Oneway Client 代码

Oneway 方式的客户端调用示例（不等待响应）：

```go
package main

import (
    "context"

    "xx/echo"
    "xx/echo/echoservice"

    "github.com/cloudwego/kitex/client"
)

func main() {
    // 创建客户端
    cli, err := echoservice.NewClient("destServiceName", client.WithHostPorts("0.0.0.0:8888"))
    if err != nil {
        panic(err)
    }
    
    // 构造请求
    req := echo.NewRequest()
    req.Msg = "hello"
    
    // 发送请求，不等待响应
    err = cli.VisitOneway(context.Background(), req)
    if err != nil {
        panic(err)
    }
    // no response return
}
```

{{<notice tip>}}

**提示：** 
- **PingPong** 适用于需要明确响应的场景，如查询、提交数据等
- **Oneway** 适用于不需要等待响应的场景，如日志记录、统计上报等，可以提高吞吐量
- **Streaming** 适用于需要双向流式通信的场景，如实时推送、长连接通信等

{{</notice>}}

---

## 🚀 StreamX 流式接口

StreamX 是 Kitex 在 v0.12.0 版本发布的新一代流式接口，旨在优化流式调用体验，提供更友好、更强大的流式通信能力。

### 📋 StreamX 简介

StreamX 是 Kitex 对原有流式接口的重构和优化，主要特点包括：

- **更友好的 API 设计**：提供更简洁、更易用的流式接口
- **多协议支持**：同时支持 TTHeader Streaming 和 gRPC 协议
- **平滑迁移**：Server 端可以同时兼容两个流式协议，无需担心接口迁移后的协议兼容性问题
- **更好的错误处理**：提供完善的流错误处理机制
- **灵活的生命周期控制**：支持通过 context cancel 控制流式调用生命周期

### 🔧 版本演进

| 版本 | 主要变更 |
|------|---------|
| **v0.12.0** | 首次发布 StreamX 接口，支持 TTHeader Streaming |
| **v0.13.0** | 支持 gRPC 协议，对 StreamX 接口做了二次调整 |
| **v0.13.1** | 修复 gRPC Client 潜在的 Goroutine 泄漏问题 |

{{<notice warning>}}

**注意：** 
- 使用 v0.12.* 的 StreamX 用户升级到 v0.13.0+ 会受到影响，需要进行接口适配
- 建议直接升级到 v0.13.1 或更高版本，以获得更稳定的体验

{{</notice>}}

### 🌐 协议选择

StreamX 支持两种协议：

| 协议类型 | 传输协议 | IDL 语言 | 序列化协议 |
|---------|---------|---------|-----------|
| **TTHeader Streaming** | TTHeader | Thrift | Thrift |
| **gRPC Streaming** | gRPC | Thrift / Protobuf | Thrift / Protobuf |

选定的协议只影响从 IDL 生成代码，无论哪种协议，使用方法均一致。

### ⚙️ 快速开始

#### 📝 定义 IDL

首先定义 Thrift IDL，使用 `streaming.mode` 注解指定流式类型：

```thrift
namespace go echo

struct Request {
    1: string Msg
}

struct Response {
    1: string Msg
}

service TestService {
    // PingPong 非流式接口
    Response PingPong(1: Request req)
    
    // 双向流式
    Response Echo (1: Request req) (streaming.mode="bidirectional")
    
    // 客户端流式
    Response EchoClient (1: Request req) (streaming.mode="client")
    
    // 服务端流式
    Response EchoServer (1: Request req) (streaming.mode="server")
}
```

#### 🏗️ 生成代码

确保 Kitex Tool 已经升级到 v0.13.0+：

```bash
go install github.com/cloudwego/kitex/tool/cmd/kitex@latest
```

为保持与旧流式生成代码的兼容，命令行需加上 `-streamx` flag：

```bash
kitex -streamx -module <go module> -service service echo.thrift
```

#### 🔌 初始化 Client

```go
import ".../kitex_gen/echo/testservice"
import "github.com/cloudwego/kitex/client"

cli, err := testservice.NewClient(
    "service.name",
    client.WithHostPorts("127.0.0.1:8888"),
)
```

#### 🏢 初始化 Server

```go
import ".../kitex_gen/echo/testservice"
import "github.com/cloudwego/kitex/server"

svr := testservice.NewServer(
    new(serviceImpl),
    server.WithHostPorts(":8888"),
)
```

---

### 📤 客户端流式 (Client Streaming)

#### 💡 使用场景

客户端需要发送多份数据给 Server 端，Server 端处理完所有数据后发送一条消息给 Client。

**典型应用场景：**
- 批量数据上传
- 大文件分片传输
- 多轮数据提交后获取最终结果

**交互流程：**
```
client.Send(req)  === req ==>  server.Recv(req)
                      ...
client.Send(req)  === req ==>  server.Recv(req)

client.CloseSend() === EOF ==>  server.Recv(EOF)
client.Recv(res)  <== res ===  server.SendAndClose(res)

或者简化为：
client.CloseAndRecv(res) === EOF ==> server.Recv(EOF)
                          <== res === server.SendAndClose(res)
```

#### 🏗️ Server 端实现

```go
import (
    "context"
    "io"
    "log"
    
    "xx/echo"
    "xx/echo/testservice"
)

type serviceImpl struct{}

func (si *serviceImpl) EchoClient(
    ctx context.Context,
    stream echo.TestService_EchoClientServer,
) (err error) {
    var totalMessages int
    
    // 持续接收客户端消息
    for {
        req, err := stream.Recv(ctx)
        if err == io.EOF {
            // 客户端发送完毕，返回最终结果
            res := &echo.Response{
                Msg: fmt.Sprintf("共收到 %d 条消息", totalMessages),
            }
            return stream.SendAndClose(ctx, res)
        }
        if err != nil {
            log.Printf("接收错误: %v", err)
            return err
        }
        
        log.Printf("收到消息: %s", req.Msg)
        totalMessages++
    }
}
```

**注意事项：**
- Server 必须在 handler 结束时调用 `SendAndClose` 返回一个 Response
- 当收到 `io.EOF` 时表示客户端已发送完毕

#### 🔌 Client 端使用

```go
import (
    "context"
    "log"
    
    "xx/echo"
    "xx/echo/testservice"
)

func clientStreamingExample(cli testservice.Client) {
    // 创建流
    stream, err := cli.EchoClient(context.Background())
    if err != nil {
        log.Fatalf("创建流失败: %v", err)
    }
    
    // 发送多条消息
    for i := 0; i < 3; i++ {
        req := &echo.Request{
            Msg: fmt.Sprintf("客户端消息 %d", i),
        }
        err = stream.Send(stream.Context(), req)
        if err != nil {
            log.Printf("发送失败: %v", err)
            break
        }
    }
    
    // 方式1: CloseSend + Recv
    err = stream.CloseSend(stream.Context())
    if err != nil {
        log.Printf("关闭发送端失败: %v", err)
        return
    }
    
    res, err := stream.Recv(stream.Context())
    if err != nil {
        log.Printf("接收响应失败: %v", err)
        return
    }
    
    // 方式2: CloseAndRecv (简化写法)
    // res, err := stream.CloseAndRecv(stream.Context())
    
    log.Printf("服务端响应: %s", res.Msg)
}
```

**注意事项：**
- Client 必须调用 `CloseAndRecv()` 或者 `CloseSend() + Recv()`
- 这会告知 Server 不再有新数据发送

---

### 📥 服务端流式 (Server Streaming)

#### 💡 使用场景

Client 发送一个请求给 Server，Server 持续发送多个返回给 Client。

**典型应用场景：**
- ChatGPT 类型的 AI 对话（流式输出）
- 实时数据推送
- 大文件下载
- 实时日志流

**交互流程：**
```
client.Send(req)   === req ==>   server.Recv(req)
client.Recv(res)   <== res ===   server.Send(res)
                       ...
client.Recv(res)   <== res ===   server.Send(res)
client.Recv(EOF)   <== EOF ===   server handler return
```

#### 🏗️ Server 端实现

```go
import (
    "context"
    "log"
    "time"
    
    "xx/echo"
    "xx/echo/testservice"
)

func (si *serviceImpl) EchoServer(
    ctx context.Context,
    req *echo.Request,
    stream echo.TestService_EchoServerServer,
) error {
    log.Printf("收到请求: %s", req.Msg)
    
    // 持续发送多个响应
    for i := 0; i < 5; i++ {
        resp := &echo.Response{
            Msg: fmt.Sprintf("服务端响应 %d: %s", i, req.Msg),
        }
        
        err := stream.Send(ctx, resp)
        if err != nil {
            log.Printf("发送失败: %v", err)
            return err
        }
        
        time.Sleep(500 * time.Millisecond)
    }
    
    return nil
}
```

**注意事项：**
- Server 可以持续调用 `Send()` 发送多个响应
- Handler 返回时会自动发送 EOF 给 Client

#### 🔌 Client 端使用

```go
import (
    "context"
    "errors"
    "io"
    "log"
    
    "xx/echo"
    "xx/echo/testservice"
)

func serverStreamingExample(cli testservice.Client) {
    // 创建流并发送请求
    req := &echo.Request{Msg: "Hello Server"}
    stream, err := cli.EchoServer(context.Background(), req)
    if err != nil {
        log.Fatalf("创建流失败: %v", err)
    }
    
    // 持续接收响应
    for {
        res, err := stream.Recv(stream.Context())
        if errors.Is(err, io.EOF) {
            // 服务端发送完毕
            break
        }
        if err != nil {
            log.Printf("接收失败: %v", err)
            break
        }
        
        log.Printf("收到响应: %s", res.Msg)
    }
}
```

**注意事项：**
- Client 必须判断 `io.EOF` 错误并结束循环
- 当收到 EOF 时表示服务端已发送完毕

---

### 🔄 双向流式 (Bidirectional Streaming)

#### 💡 使用场景

Client 与 Server 都可以随时发送多条消息，双方可以独立地读写数据。

**典型应用场景：**
- 实时聊天应用
- 实时游戏
- 实时数据同步
- 双向实时监控

**交互流程：**
```
* Goroutine 1 (发送) *
client.Send(req)   === req ==>   server.Recv(req)
                       ...
client.Send(req)   === req ==>   server.Recv(req)
client.CloseSend() === EOF ==>   server.Recv(EOF)

* Goroutine 2 (接收) *
client.Recv(res)   <== res ===   server.Send(res)
                       ...
client.Recv(res)   <== res ===   server.Send(res)
client.Recv(EOF)   <== EOF ===   server handler return
```

#### 🏗️ Server 端实现

```go
import (
    "context"
    "errors"
    "io"
    "log"
    "sync"
    
    "xx/echo"
    "xx/echo/testservice"
)

func (si *serviceImpl) Echo(
    ctx context.Context,
    stream echo.TestService_EchoServer,
) error {
    var wg sync.WaitGroup
    wg.Add(2)
    
    // Goroutine 1: 接收客户端消息
    go func() {
        defer wg.Done()
        for {
            req, err := stream.Recv(ctx)
            if errors.Is(err, io.EOF) {
                log.Println("客户端发送完毕")
                return
            }
            if err != nil {
                log.Printf("接收错误: %v", err)
                return
            }
            
            log.Printf("收到客户端消息: %s", req.Msg)
        }
    }()
    
    // Goroutine 2: 发送响应给客户端
    go func() {
        defer wg.Done()
        for i := 0; i < 10; i++ {
            select {
            case <-ctx.Done():
                log.Println("Context 已取消")
                return
            default:
            }
            
            resp := &echo.Response{
                Msg: fmt.Sprintf("服务端消息 %d", i),
            }
            
            err := stream.Send(ctx, resp)
            if err != nil {
                log.Printf("发送错误: %v", err)
                return
            }
        }
    }()
    
    wg.Wait()
    return nil
}
```

**注意事项：**
- Server 必须在 Recv 时判断 `io.EOF` 并结束循环
- 通常使用两个 goroutine 分别处理发送和接收
- 需要使用 context 来协调生命周期

#### 🔌 Client 端使用

```go
import (
    "context"
    "errors"
    "io"
    "log"
    "sync"
    "time"
    
    "xx/echo"
    "xx/echo/testservice"
)

func bidirectionalStreamingExample(cli testservice.Client) {
    // 创建双向流
    stream, err := cli.Echo(context.Background())
    if err != nil {
        log.Fatalf("创建流失败: %v", err)
    }
    
    var wg sync.WaitGroup
    wg.Add(2)
    
    // Goroutine 1: 发送消息
    go func() {
        defer wg.Done()
        for i := 0; i < 5; i++ {
            req := &echo.Request{
                Msg: fmt.Sprintf("客户端消息 %d", i),
            }
            
            err := stream.Send(stream.Context(), req)
            if err != nil {
                log.Printf("发送失败: %v", err)
                return
            }
            
            time.Sleep(time.Second)
        }
        
        // 发送完毕，关闭发送端
        err = stream.CloseSend(stream.Context())
        if err != nil {
            log.Printf("关闭发送端失败: %v", err)
        }
    }()
    
    // Goroutine 2: 接收消息
    go func() {
        defer wg.Done()
        for {
            res, err := stream.Recv(stream.Context())
            if errors.Is(err, io.EOF) {
                log.Println("服务端发送完毕")
                break
            }
            if err != nil {
                log.Printf("接收失败: %v", err)
                break
            }
            
            log.Printf("收到服务端消息: %s", res.Msg)
        }
    }()
    
    // 等待两个 goroutine 完成
    wg.Wait()
}
```

**注意事项：**
- Client 必须在发送结束后调用 `CloseSend()`
- Client 必须在 Recv 时判断 `io.EOF` 并结束循环
- 通常使用两个 goroutine 分别处理发送和接收

---

### 🎯 StreamX 最佳实践

#### ⚠️ 流错误处理

StreamX 提供了完善的错误处理机制：

```go
stream, err := cli.Echo(ctx)
if err != nil {
    // 处理流创建错误
    return
}

for {
    req, err := stream.Recv(ctx)
    if err != nil {
        if errors.Is(err, io.EOF) {
            // 正常结束
            break
        }
        // 处理其他错误
        log.Printf("接收错误: %v", err)
        break
    }
    // 处理请求
}
```

#### ⏱️ 流生命周期控制

使用 context 控制流式调用的生命周期：

```go
// 创建带超时的 context
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

stream, err := cli.Echo(ctx)
if err != nil {
    return
}

// 当 context 被取消时，流会自动关闭
```

#### ⏰ TTHeader Streaming 超时配置

StreamX 支持接口级别的 Recv 超时配置：

```go
import "github.com/cloudwego/kitex/pkg/streaming"

// 在调用时设置接收超时
resp, err := cli.StreamMethod(ctx, req, streaming.WithRecvTimeout(5*time.Second))
```

{{<notice tip>}}

**StreamX 使用建议：**
- **新服务**：直接使用 StreamX 接口，获得更好的开发体验
- **存量服务**：可以平滑迁移到 StreamX，Server 端可同时兼容新旧协议
- **性能敏感**：TTHeader Streaming 通常具有更好的性能表现
- **互通需求**：gRPC 协议适合需要与其他 gRPC 服务互通的场景
- **客户端流式**：适用于批量数据上传、多轮提交等场景
- **服务端流式**：适用于 AI 对话、实时推送、大文件下载等场景
- **双向流式**：适用于实时聊天、游戏、数据同步等场景

{{</notice>}}

---

## 🔌 StreamX 流中间件

StreamX 提供了强大的中间件机制，可以在流式调用的不同阶段注入自定义逻辑，实现日志记录、监控、限流、认证等功能。

### 📋 中间件类型

StreamX 支持三种中间件类型，分别在不同的触发时机执行：

| 中间件类型 | 触发时机 | 适用场景 |
|-----------|---------|---------|
| **Stream 中间件** | 每次创建流时 | 流创建前/后的处理，如日志、认证 |
| **Stream Recv/Send 中间件** | 流收发消息时 | 消息级别的处理，如监控、限流、日志 |
| **Unary 中间件** | 非流式接口调用时 | 仅对非流式方法生效 |

### 🛠️ 类型定义

#### Stream 中间件

```go
// Client 侧
// github.com/cloudwego/kitex/pkg/endpoint/cep
type StreamEndpoint func(ctx context.Context) (stream streaming.ClientStream, err error)
type StreamMiddleware func(next StreamEndpoint) StreamEndpoint

// Server 侧
// github.com/cloudwego/kitex/pkg/endpoint/sep
type StreamEndpoint func(ctx context.Context, stream streaming.ServerStream) (err error)
type StreamMiddleware func(next StreamEndpoint) StreamEndpoint
```

**参数说明：**
- `stream`：为单次 RPC 创建的流对象
- Client middleware 内 `next` 函数执行后，stream 即完成创建
- Server middleware 内 `next` 函数执行后，server handler 即完成处理

#### Stream Recv/Send 中间件

```go
// Client 侧
// github.com/cloudwego/kitex/pkg/endpoint/cep
type StreamRecvEndpoint func(ctx context.Context, stream streaming.ClientStream, message interface{}) (err error)
type StreamRecvMiddleware func(next StreamRecvEndpoint) StreamRecvEndpoint

type StreamSendEndpoint func(ctx context.Context, stream streaming.ClientStream, message interface{}) (err error)
type StreamSendMiddleware func(next StreamSendEndpoint) StreamSendEndpoint

// Server 侧
// github.com/cloudwego/kitex/pkg/endpoint/sep
type StreamRecvEndpoint func(ctx context.Context, stream streaming.ServerStream, message interface{}) (err error)
type StreamRecvMiddleware func(next StreamRecvEndpoint) StreamRecvEndpoint

type StreamSendEndpoint func(ctx context.Context, stream streaming.ServerStream, message interface{}) (err error)
type StreamSendMiddleware func(next StreamSendEndpoint) StreamSendEndpoint
```

**参数说明：**
- `stream`：直接获取当前的流对象
- `message`：代表真实的请求和响应

#### Unary 中间件

对所有非流式接口，提供 UnaryMiddleware 用于注入仅对所有 unary 方法生效的中间件：

```go
type UnaryEndpoint Endpoint
type UnaryMiddleware func(next UnaryEndpoint) UnaryEndpoint

// 使用方式：
// client.WithUnaryOptions(client.WithUnaryMiddleware(mw))
// server.WithUnaryOptions(server.WithUnaryMiddleware(mw))
```

{{<notice info>}}

**说明：**
- UnaryMiddleware 与 kitex 原生支持的 `WithMiddleware` 方法签名完全一致
- 区别在于 `WithMiddleware` 可以同时对 streaming 方法生效
- UnaryMiddleware 仅对非流式方法生效

{{</notice>}}

### 📊 Next 函数调用前后行为

| 中间件类型 | Next 调用前 | Next 调用后 |
|-----------|------------|------------|
| **StreamRecvMiddleware** | 数据未真正收，刚调用 `stream.Recv()` 函数<br>res 参数为空 | 数据已收到或遇到错误<br>res 参数有真实值 |
| **StreamSendMiddleware** | 数据未真正发送，刚调用 `stream.Send()` 函数<br>req 参数为真实请求 | 数据发送完成或遇到错误<br>req 参数为真实请求 |

### 🔧 注入 Client 侧中间件

```go
import (
    "github.com/cloudwego/kitex/client"
    "github.com/cloudwego/kitex/pkg/endpoint/cep"
    "github.com/cloudwego/kitex/pkg/rpcinfo"
    "github.com/cloudwego/kitex/pkg/streaming"
)

cli, err := testservice.NewClient(
    "service.name",
    client.WithHostPorts("127.0.0.1:8888"),
    client.WithStreamOptions(
        // Stream 中间件：流创建时触发
        client.WithStreamMiddleware(func(next cep.StreamEndpoint) cep.StreamEndpoint {
            return func(ctx context.Context) (stream streaming.ClientStream, err error) {
                ri := rpcinfo.GetRPCInfo(ctx)
                println("创建流, 方法: ", ri.Invocation().MethodName())
                return next(ctx)
            }
        }),
        
        // Stream Send 中间件：发送消息时触发
        client.WithStreamSendMiddleware(func(next cep.StreamSendEndpoint) cep.StreamSendEndpoint {
            return func(ctx context.Context, stream streaming.ClientStream, message interface{}) (err error) {
                ri := rpcinfo.GetRPCInfo(stream.Context())
                println("发送消息, 方法: ", ri.Invocation().MethodName())
                return next(ctx, stream, message)
            }
        }),
        
        // Stream Recv 中间件：接收消息时触发
        client.WithStreamRecvMiddleware(func(next cep.StreamRecvEndpoint) cep.StreamRecvEndpoint {
            return func(ctx context.Context, stream streaming.ClientStream, message interface{}) (err error) {
                ri := rpcinfo.GetRPCInfo(stream.Context())
                println("接收消息, 方法: ", ri.Invocation().MethodName())
                return next(ctx, stream, message)
            }
        }),
    ),
)
```

### 🏢 注入 Server 侧中间件

```go
import (
    "github.com/cloudwego/kitex/server"
    "github.com/cloudwego/kitex/pkg/endpoint/sep"
    "github.com/cloudwego/kitex/pkg/rpcinfo"
    "github.com/cloudwego/kitex/pkg/streaming"
)

svr, err := testservice.NewServer(
    new(serviceImpl),
    server.WithHostPorts(":8888"),
    server.WithStreamOptions(
        // Stream 中间件：流创建时触发
        server.WithStreamMiddleware(func(next sep.StreamEndpoint) sep.StreamEndpoint {
            return func(ctx context.Context, st streaming.ServerStream) (err error) {
                ri := rpcinfo.GetRPCInfo(ctx)
                println("创建流, 方法: ", ri.Invocation().MethodName())
                return next(ctx, st)
            }
        }),
        
        // Stream Recv 中间件：接收消息时触发
        server.WithStreamRecvMiddleware(func(next sep.StreamRecvEndpoint) sep.StreamRecvEndpoint {
            return func(ctx context.Context, stream streaming.ServerStream, message interface{}) (err error) {
                ri := rpcinfo.GetRPCInfo(ctx)
                println("接收消息, 方法: ", ri.Invocation().MethodName())
                return next(ctx, stream, message)
            }
        }),
        
        // Stream Send 中间件：发送消息时触发
        server.WithStreamSendMiddleware(func(next sep.StreamSendEndpoint) sep.StreamSendEndpoint {
            return func(ctx context.Context, stream streaming.ServerStream, message interface{}) (err error) {
                ri := rpcinfo.GetRPCInfo(ctx)
                println("发送消息, 方法: ", ri.Invocation().MethodName())
                return next(ctx, stream, message)
            }
        }),
    ),
)
```

{{<notice tip>}}

**流中间件使用建议：**
- **日志记录**：使用 Stream 中间件记录流创建，使用 Recv/Send 中间件记录消息收发
- **性能监控**：在中间件中记录耗时、消息大小等指标
- **限流控制**：在 Send/Recv 中间件中实现流量控制
- **认证鉴权**：在 Stream 中间件中进行认证，在消息级别中间件中进行细粒度鉴权
- **上下文传递**：通过 `stream.Context()` 获取和传递上下文信息

{{</notice>}}
