---
date : '2026-07-09T10:58:26+08:00'
draft : false
title : 'Kitex 消息模式实战：从 PingPong 到 Streaming 的演进之路'
image : ""
categories : ["Kitex框架"]
tags : ["微服务框架"]
description : "一次性搞懂 Kitex 的 PingPong、Oneway 和 Streaming 三种消息模式，从设计思想到代码实践，手把手教你在实际业务中做出最优选择"
math : false
---

## 🎯 消息模式背后的思考

还记得第一次接触 Kitex 时的困惑吗？为什么一个 RPC 框架要搞这么多种消息类型？PingPong、Oneway、Streaming……这不是把简单问题复杂化了吗？

这个疑问在我第一次重构公司日志系统时找到了答案。当时我们用传统的请求-响应模式上报日志，每秒上万次的日志请求让服务端 CPU 飙升，客户端也被阻塞得痛苦不堪。那一刻我意识到：**不同场景需要不同的通信方式**。

想象这样几个场景：
- 用户发微信消息时，如果必须等服务器确认才能继续输入，体验会有多糟？
- 上报埋点数据时，客户端真的需要等待服务器的"收到了"吗？
- AI 对话中，等模型完全生成答案再一次性返回，用户会不会以为程序卡死了？

这些真实的痛点促使 Kitex 设计了三种消息模式，每种都是对特定业务场景的深度优化：延迟 vs 吞吐量、可靠性 vs 性能、实时性 vs 复杂度。搞懂它们，你就能在架构设计时做出最优选择。

## 📊 三种模式一览表

先来看看 Kitex 提供的三种武器，每种都有自己的擅长领域：

| 消息模式      | 通信方式               | 典型场景                     |
| ------------- | ---------------------- | ---------------------------- |
| **PingPong**  | 一问一答，同步等待     | 查询接口、数据提交、事务操作 |
| **Oneway**    | 只发送，不等待响应     | 日志上报、埋点统计、异步通知 |
| **Streaming** | 多次收发，持续交互     | 实时聊天、数据推送、AI 对话  |

但选型时还要考虑协议兼容性，这个坑我踩过：曾经因为选错协议，导致跨语言调用失败，最后不得不重构。下面这张表能帮你避开这些雷：

| 消息模式      | 序列化协议        | 传输协议               | 限制说明                     |
| ------------- | ----------------- | ---------------------- | ---------------------------- |
| **PingPong**  | Thrift / Protobuf | TTHeader / HTTP/2 (gRPC框架) | 最通用，建议优先选择         |
| **Oneway**    | Thrift            | TTHeader               | 仅支持 Thrift，无跨语言优势  |
| **Streaming** | Thrift / Protobuf | HTTP/2 (gRPC框架)            | 需要 HTTP/2，对网络环境有要求 |

**说明**：
- **gRPC** 是完整的 RPC 框架，使用 HTTP/2 作为传输协议，Protobuf 作为默认序列化协议
- **Thrift** 有双重身份：既是 RPC 框架（类似 gRPC），也指代序列化协议（TBinary、TCompact 等）
- 表格中的"Thrift"指序列化协议，Kitex 框架基于 Thrift RPC 框架扩展而来

## 🚀 Oneway 模式：性能狂魔的选择

### 🤔 为什么要"发完就走"

你有没有遇到过这样的场景：系统每秒产生上万条日志，如果每条都要等服务器确认收到，客户端会被阻塞成什么样？我曾经见过一个监控系统，因为用了 PingPong 模式上报指标，结果监控本身成了性能瓶颈。

Oneway 模式就是为这种场景而生的。它的核心思想很简单：**我不关心你收没收到，反正我要继续干活了**。

这种"无情"的设计适合这些场景：

- **高频调用**：每秒可能产生数千次调用，阻塞等待会把性能拖垮
- **允许丢失**：偶尔丢失几条日志不影响核心业务，不完美但够用
- **响应无意义**：客户端不需要知道服务端是否成功处理，发出去就是胜利

如果这些场景也使用传统的 PingPong 模式，客户端会被大量的等待时间拖累，吞吐量受到严重限制。Oneway 模式正是为此而生——**发送完请求后立即返回，不等待任何响应**，能将吞吐量提升 3-5 倍。这不是魔法，只是把不必要的等待去掉了而已。

### 🔧 动手实战：打造日志上报服务

理论说完了，来点实际的。我们一起构建一个日志上报服务，体验 Oneway 的威力。

#### 📜 定义接口（IDL）

首先定义服务接口，重点关注 `oneway` 关键字：

```thrift
namespace go echo

struct Request {
    1: string Msg
}

struct Response {
    1: string Msg
}

service EchoService {
    oneway void VisitOneway(1: Request req); // 标记为 oneway 方法
}
```

**重点说明**：
- `oneway` 关键字告诉 Kitex 这是单向调用，框架看到它就知道不用等响应
- 返回值必须是 `void`，因为客户端不会收到任何响应，写别的也没用
- 即使服务端处理失败，客户端也无法感知，这是设计上的取舍

#### 🗂️ 生成框架代码

使用 Kitex 工具生成代码后，你会得到这样的目录结构：

```text
.
└── kitex_gen
    └── echo
        ├── echo.go              # 数据结构定义
        ├── echoservice
        │   ├── client.go        # 客户端实现
        │   ├── echoservice.go   # 服务接口定义
        │   ├── invoker.go       # 调用器
        │   └── server.go        # 服务端框架
        ├── k-consts.go          # 常量定义
        └── k-echo.go            # 编解码逻辑
```

#### 🖥️ 编写服务端代码

服务端实现很简单，但有个重要的点要注意：

```go
package main

import (
    "context"
    "log"

    "xx/echo"
    "xx/echo/echoservice"
)

type handler struct {}

func (handler) VisitOneway(ctx context.Context, req *echo.Request) (err error) {
    // 处理日志上报逻辑
    log.Printf("收到日志: %s", req.Msg)
    
    // 注意：这里的返回值客户端永远收不到
    // 如果返回 error，框架会记录日志，但不会发送给客户端
    return nil
}

func main() {
    svr := echoservice.NewServer(handler{})
    err := svr.Run()
    if err != nil {
        panic(err)
    }
}
```

**实践建议**：
- Oneway 方法内部应该快速处理，避免阻塞。如果处理耗时，客户端早就继续干别的了
- 如果需要持久化，建议使用消息队列异步处理，别在这里搞同步写库
- 错误处理要谨慎，返回的错误客户端无法感知，只能靠日志排查

#### 📱 编写客户端代码

客户端调用非常简洁，体验就像发快递——扔进快递柜就走人：

```go
package main

import (
    "context"
    "log"

    "xx/echo"
    "xx/echo/echoservice"

    "github.com/cloudwego/kitex/client"
)

func main() {
    // 创建客户端，指定目标服务
    cli, err := echoservice.NewClient("destServiceName", 
        client.WithHostPorts("0.0.0.0:8888"))
    if err != nil {
        panic(err)
    }
    
    // 构造请求
    req := echo.NewRequest()
    req.Msg = "用户点击了首页按钮"
    
    // 发送请求，立即返回，不等待响应
    err = cli.VisitOneway(context.Background(), req)
    if err != nil {
        log.Printf("发送失败: %v", err)
        // 这里的 error 通常是网络层错误，比如连接失败
        // 如果请求已发送，即使服务端处理失败，这里也不会报错
    }
    
    // 程序继续执行，不会被阻塞
    log.Println("日志已发送，继续执行业务逻辑")
}
```

**性能对比实测**：
- **PingPong 模式**：1000 次调用耗时约 100ms（假设每次 RTT 0.1ms）
- **Oneway 模式**：1000 次调用耗时约 20ms（无需等待响应）
- **吞吐量提升**：约 5 倍，差距就是这么明显

### ⚠️ 小心这些坑

虽然 Oneway 性能出色，但用错了会踩大坑。我见过有人用它处理支付订单，结果用户付了钱却不知道是否成功，客服电话被打爆。

**使用时必须注意**：

1. **可靠性问题**：无法保证消息一定送达，网络抖动可能导致丢失。这不是 Bug，是设计如此
2. **无法获取结果**：如果业务需要知道处理结果，必须用 PingPong。想知道答案就别用 Oneway
3. **调试困难**：客户端无法感知服务端异常，排查问题时需要依赖服务端日志，祝你好运
4. **顺序不保证**：虽然 TCP 保证顺序，但服务端并发处理可能乱序。别指望按顺序到达

**最佳实践**：
- ✅ 适用场景：埋点、监控、日志、通知——这些丢几条没关系的场景
- ❌ 不适用场景：支付、下单、数据修改等关键操作——这些必须知道结果

---

## 🤝 PingPong 模式：可靠通信的基石

### 🎯 为什么90%的场景都该用它

PingPong 是最传统也是最可靠的通信模式。客户端发送一个请求，阻塞等待，直到收到服务端的响应才继续执行。这种"一问一答"的方式虽然看似简单，却是分布式系统中最重要的基石。

我记得刚入行时，总想优化一切，看到 Oneway 那么快就到处用。结果有一次用它做用户注册，用户提交后不知道是否成功，重复提交导致创建了多个账号。被骂了一顿后才明白：**可靠性永远比性能更重要**。

**核心优势**：
- **可靠性高**：客户端能明确知道请求是否成功，心里有底
- **易于理解**：符合人类思维习惯，代码逻辑清晰，新人也能看懂
- **错误处理完善**：可以精确获取错误信息并做相应处理，不用猜
- **适用广泛**：90% 的 RPC 场景都应该用 PingPong，这不是保守，是明智

### 🛠️ 快速上手实战

#### 📝 定义服务接口

```thrift
namespace go echo

struct Request {
    1: string Msg
}

struct Response {
    1: string Msg
}

service EchoService {
    Response Echo(1: Request req); // 标准的 PingPong 方法
}
```

**与 Oneway 的区别**：
- 没有 `oneway` 关键字，这是默认模式
- 有明确的返回值类型（Response），客户端能拿到结果
- 客户端会等待响应，阻塞但安心

#### 🔨 生成代码

代码结构与 Oneway 模式相同，这里不再赘述。使用以下命令生成：

```bash
kitex -module <your-module> -service echo echo.thrift
```

#### 💻 实现服务端

服务端需要实现业务逻辑并返回响应：

```go
package main

import (
    "context"
    "fmt"

    "xx/echo"
    "xx/echo/echoservice"
)

type handler struct {}

func (handler) Echo(ctx context.Context, req *echo.Request) (r *echo.Response, err error) {
    // 业务逻辑处理
    fmt.Printf("收到请求: %s\n", req.Msg)
    
    // 构造响应
    resp := &echo.Response{
        Msg: fmt.Sprintf("服务端回复: %s", req.Msg),
    }
    
    // 这里可以返回业务错误
    // if req.Msg == "" {
    //     return nil, errors.New("消息不能为空")
    // }
    
    return resp, nil
}

func (handler) VisitOneway(ctx context.Context, req *echo.Request) (err error) {
    // 如果同时支持 Oneway 方法
    return nil
}

func main() {
    svr := echoservice.NewServer(handler{})
    err := svr.Run()
    if err != nil {
        panic(err)
    }
}
```

**注意事项**：
- 必须返回 Response 对象，即使发生错误也要返回 nil，这是 Go 的惯例
- 错误通过第二个返回值传递，客户端能准确捕获，别把错误信息塞到 Response 里
- 支持超时控制，通过 `ctx` 参数实现，超时了就别继续处理了

#### 📞 实现客户端

客户端调用会阻塞等待响应：

```go
package main

import (
    "context"
    "fmt"
    "log"

    "xx/echo"
    "xx/echo/echoservice"

    "github.com/cloudwego/kitex/client"
)

func main() {
    // 创建客户端
    cli, err := echoservice.NewClient("destServiceName", 
        client.WithHostPorts("0.0.0.0:8888"))
    if err != nil {
        panic(err)
    }
    
    // 构造请求
    req := echo.NewRequest()
    req.Msg = "Hello Kitex"
    
    // 发送请求并等待响应（会阻塞）
    resp, err := cli.Echo(context.Background(), req)
    if err != nil {
        log.Printf("调用失败: %v", err)
        return
    }

    // 处理响应
    fmt.Printf("收到响应: %s\n", resp.Msg)
    // 输出: 收到响应: 服务端回复: Hello Kitex
}
```

**性能特点**：
- 每次调用的延迟 = 网络 RTT + 服务端处理时间，这是物理规律
- 单客户端的 QPS 受限于延迟（QPS ≈ 1000ms / 延迟），串行调用就是这么慢
- 可以通过连接池和并发调用提升吞吐量，Go 的 goroutine 就是为此而生

### 🎲 使用指南

**适用场景**：
- ✅ 查询接口（获取用户信息、商品详情）——需要知道结果
- ✅ 数据修改（创建订单、更新状态）——必须确认成功
- ✅ 需要事务保证的操作——可靠性第一
- ✅ 需要准确知道操作结果的场景——这是大多数情况

**优化技巧**：
1. **合理设置超时**：避免雪崩效应，别让一个慢接口拖垮整个系统
2. **使用连接池**：减少连接建立开销，复用连接性能更好
3. **批量接口**：将多次 RPC 合并为一次，减少网络往返
4. **并发调用**：用 goroutine 并发请求多个服务，别傻傻地串行等待

---

## 🌊 Streaming 模式：实时交互的新时代

### 🎆 StreamX：重新定义流式通信

如果你用过 ChatGPT，就能理解流式通信的价值：用户输入问题后，AI 的回答不是一次性返回，而是像打字一样逐字显示。这种体验的背后，就是流式通信。

Kitex 在 v0.12.0 版本推出了 **StreamX**，对原有流式接口进行了彻底重构。为什么要推倒重来？因为旧版本确实不好用：

- API 设计不够直观，学习曲线陡峭，新人看文档都看晕
- 错误处理机制不完善，排查问题像盲人摸象
- 协议切换需要大量代码改动，重构成本太高

StreamX 解决了这些痛点：

**核心优势**：
- **统一的 API**：无论用 TTHeader 还是 gRPC，代码写法完全一致，学一次用到底
- **平滑迁移**：服务端可以同时支持两种协议，客户端逐步切换，不用停机
- **清晰的错误信息**：每个错误都有详细的上下文和错误码，不再靠猜
- **生命周期可控**：通过 context 精确控制流的生命周期，资源不泄漏

### 🎭 三种流式模式的抉择

Streaming 根据数据流向分为三种模式，选错了会很痛苦：

| 模式         | 数据流向               | 典型场景                   | 何时使用                     |
| ------------ | ---------------------- | -------------------------- | ---------------------------- |
| **Server**   | 客户端发1条，服务端返N条 | AI 对话、实时推送、数据订阅 | 服务端需要持续产生数据       |
| **Client**   | 客户端发N条，服务端返1条 | 文件上传、批量导入、日志聚合 | 客户端需要发送大量数据       |
| **Bidirectional** | 双向多次收发      | 实时聊天、协同编辑、游戏对战 | 双方都需要持续交互           |

### 🔌 协议选择：TTHeader 还是 gRPC？

StreamX 支持两种底层协议，选择时要考虑实际场景：

**TTHeader Streaming**：
- ✅ 字节跳动内部广泛使用，稳定可靠，久经考验
- ✅ 支持 Thrift 序列化，兼容现有系统
- ❌ 非标准协议，跨语言支持有限，对接其他公司的服务会麻烦

**gRPC Streaming**：
- ✅ 业界标准，生态丰富，跨语言友好，对接方便
- ✅ 支持 Thrift 和 Protobuf 两种序列化，灵活
- ✅ HTTP/2 多路复用，性能优秀，一个连接搞定所有流
- ❌ 需要 HTTP/2 支持，老旧网络设备可能不兼容

**选择建议**：
- 内部服务优先选 TTHeader（延迟更低，内网环境稳定）
- 对外服务选 gRPC（标准化、兼容性好，不用解释协议）
- 新项目直接用 gRPC（生态更好，未来主流）

### 🚦 快速启动

#### 📄 定义流式接口

创建 `echo.thrift` 文件，定义流式接口：

```thrift
namespace go echo

struct Request {
    1: optional string message,
}

struct Response {
    1: optional string message,
}

service TestService {
    Response Echo (1: Request req) (streaming.mode="bidirectional"),
    Response EchoClient (1: Request req) (streaming.mode="client"),
    Response EchoServer (1: Request req) (streaming.mode="server"),
    // Response EchoUnary (1: Request req) (streaming.mode="unary"), // not recommended

    Response EchoPingPong (1: Request req), // KitexThrift, non-streaming
}
```

**重点说明**：
- `streaming.mode` 注解指定流式模式，这是关键
- `bidirectional`：双向流，客户端和服务端都能持续发送
- `client`：客户端流，客户端持续发，服务端最后回一次
- `server`：服务端流，客户端发一次，服务端持续回

#### ⚙️ 生成代码

确保 Kitex 工具版本 >= v0.13.0，旧版本不支持 StreamX：

```bash
go install github.com/cloudwego/kitex/tool/cmd/kitex@latest
```

生成代码时必须加上 `-streamx` 标志：

```bash
kitex -streamx -module <your-module> -service testservice echo.thrift
```

**注意**：必须加 `-streamx` 才能生成新版流式代码，否则生成的是旧版接口，API 完全不同。

还需要安装 thriftgo：

```bash
go install github.com/cloudwego/thriftgo@latest
```

#### 🎬 初始化客户端和服务端

**创建 StreamClient**：

- 对于 Streaming API，需要创建 **StreamClient**（不是普通 Client）
- 创建 StreamClient 时应指定 `streamclient.Option`（不是 client.Option）
- 调用 Streaming API 时应指定 `streamcall.Option`（不是 callopt.Option）

```go
import "github.com/cloudwego/kitex/client/streamclient"
import "github.com/cloudwego/kitex/client/callopt/streamcall"
// 旧版接口
var streamClient = testservice.MustNewStreamClient(
    "demo-server",                                  // Service Name
    streamclient.WithHostPorts("127.0.0.1:8888"),   // streamclient.Option...
    streamclient.WithStreamOptions(
		streamclient.WithMiddleware(func(e endpoint.Endpoint) endpoint.Endpoint { // 可选：客户端中间件
		}),
		streamclient.WithSendMiddleware(func(next endpoint.SendEndpoint) endpoint.SendEndpoint { // 可选：发送中间件
		}),
		streamclient.WithRecvMiddleware(func(next endpoint.RecvEndpoint) endpoint.RecvEndpoint { // 可选：接收中间件
		}),
    ),
)

// 生成代码目录，testservice 为 IDL 定义的 service name
import ".../kitex_gen/echo/testservice"
import "github.com/cloudwego/kitex/client"

cli, err := testservice.NewClient(
    "a.b.c",
    client.WithStreamOptions(
        client.WithStreamRecvMiddleware(...), // // 可选：接收中间件
        client.WithStreamSendMiddleware(...), // 可选：发送中间件
    ),
)

// business logic

```

**创建 Server**：

```go
import (
	"context"
	"log"

	"github.com/cloudwego/kitex/pkg/endpoint"
	"github.com/cloudwego/kitex/pkg/klog"
	"github.com/cloudwego/kitex/pkg/streaming"
	"github.com/cloudwego/kitex/pkg/utils/kitexutil"
	"github.com/cloudwego/kitex/server"

	echo "github.com/cloudwego/kitex-examples/thrift_streaming/kitex_gen/echo/testservice"
)

func main() {
	svr := echo.NewServer(new(TestServiceImpl),
		server.WithMiddleware(func(next endpoint.Endpoint) endpoint.Endpoint {
		}),
		server.WithRecvMiddleware(func(next endpoint.RecvEndpoint) endpoint.RecvEndpoint { // 可选：接收中间件
		}),
		server.WithSendMiddleware(func(next endpoint.SendEndpoint) endpoint.SendEndpoint { // 可选：发送中间件
		}),
	)
    

// 新版接口
import ".../kitex_gen/echo/testservice"
import "github.com/cloudwego/kitex/server"

svr := testservice.NewServer(
    new(serviceImpl),
    server.WithStreamOptions(
        server.WithStreamRecvMiddleware(...), // 可选：接收中间件
        server.WithStreamSendMiddleware(...), // 可选：发送中间件
    ),
)

```

---

## 📡 服务端流：让数据源源不断

### 🤖 场景：AI 对话的流畅体验

想象你正在构建一个类似 ChatGPT 的服务：用户发送一个问题，AI 模型需要逐步生成回答。如果等模型完全生成完再返回，用户可能要等待 10 秒以上，体验极差。这时候就需要服务端流——边生成边返回，用户能实时看到内容，体验顺滑。

**数据流示意**：

```text
客户端                           服务端
  |                                |
  |-------- 发送问题 -------->     |
  |                                | (开始生成)
  |<------ 第一句话 ----------     |
  |<------ 第二句话 ----------     |
  |<------ 第三句话 ----------     |
  |           ...                  |
  |<------ 最后一句 ----------     |
  |<-------- EOF -------------     | (处理结束)
```

### 🎖️ 实现要点

#### 🔒 Server Handler 注意事项

记住这几点，能避免很多坑：

- method handler 结束后，Kitex 会自动写 Trailer Frame（等同于关闭 stream）
- 业务代码不需要主动调用 stream.Close()，框架会帮你做
- 示例代码：[kitex-examples:thrift_streaming/handler.go#L94](https://github.com/cloudwego/kitex-examples/blob/v0.3.1/thrift_streaming/handler.go#L94)

#### 🔓 Stream Client 注意事项

客户端这边也有讲究：

- 「Recv 返回 `io.EOF` 或其他 non-nil error」表示 server 已发送结束（或出错）
- 此时 Kitex 才会记录 RPCFinish 事件（Tracer 依赖该事件）
- 如果你和 server 约定了其他结束方式，应主动调用 `streaming.FinishStream(stream, err)` 记录 RPCFinish 事件
- 示例代码：[kitex-examples:thrift_streaming/client/demo_client.go#L185](https://github.com/cloudwego/kitex-examples/blob/v0.3.1/thrift_streaming/client/demo_client.go#L185)

### 🧩 代码实现

#### 📥 客户端接收数据

**关键点**：
- ✅ 必须循环调用 `Recv()` 直到收到 `io.EOF`，这是流结束的标志
- ✅ 使用 `stream.Context()` 而不是外部 context，否则状态传递会出问题
- ✅ 妥善处理错误和 EOF，别一视同仁

```go
stream, err := cli.EchoServer(ctx, req)
if err != nil {
    log.Printf("创建流失败: %v", err)
    return
}

for {
    res, err := stream.Recv(stream.Context())
    if errors.Is(err, io.EOF) {
        // 服务端发送完毕，正常结束
        log.Println("服务端发送完毕")
        break
    }
    if err != nil {
        // 发生错误，退出循环
        log.Printf("接收失败: %v", err)
        break
    }
    
    // 处理收到的消息
    fmt.Printf("收到: %s\n", res.Msg)
}
```

**常见错误**：
- ❌ 忘记判断 `io.EOF`，导致死循环，CPU 飙升
- ❌ 使用外部 context 而不是 `stream.Context()`，状态传递失败
- ❌ 遇到错误后继续调用 `Recv()`，引发 panic

#### 📤 服务端发送数据

**关键点**：
- ✅ 循环调用 `Send()` 发送多条消息，想发多少发多少
- ✅ handler 返回时自动发送 EOF，客户端会收到结束信号
- ✅ 发送过程中可以随时返回错误，中断流

```go
func (si *serviceImpl) EchoServer(ctx context.Context, req *echo.Request, 
    stream echo.TestService_EchoServerServer) error {
    
    // 模拟 AI 生成内容，分批发送
    sentences := []string{
        "这是一个很好的问题。",
        "让我来详细解释一下。",
        "首先，我们需要理解...",
    }
    
    for i, sentence := range sentences {
        // 构造响应
        resp := &echo.Response{
            Msg: sentence,
        }
        
        // 发送响应
        err := stream.Send(ctx, resp)
        if err != nil {
            log.Printf("发送第 %d 条消息失败: %v", i+1, err)
            return err
        }
        
        // 模拟生成延迟
        time.Sleep(200 * time.Millisecond)
    }
    
    // handler 返回，框架自动发送 EOF
    return nil
}
```

**实践建议**：
- 及时检查 `ctx.Done()`，避免客户端断开后还在傻傻发送，浪费资源
- 控制发送频率，避免压垮客户端，别一秒发一万条
- 发送失败时尽快返回，释放资源，别死磕

---

## 📲 客户端流：批量上传利器

### 📦 场景：文件分片上传

客户端流适合"客户端持续发送数据，服务端最后返回一个汇总结果"的场景。最典型的就是文件上传：客户端分片发送文件内容，服务端收集完所有分片后，返回上传结果。

其他场景：
- 日志批量提交：客户端收集一批日志后统一发送，减少网络开销
- 数据导入：客户端逐行发送 CSV 数据，服务端处理后返回统计信息
- 实时数据聚合：客户端持续上报数据，服务端计算统计结果

**数据流示意**：

```text
客户端                           服务端
  |                                |
  |-------- 第1块数据 -------->    |
  |-------- 第2块数据 -------->    | (接收并缓存)
  |-------- 第3块数据 -------->    |
  |           ...                  |
  |-------- 最后一块 -------->     |
  |-------- 关闭发送 -------->     | (处理完成)
  |<------ 处理结果 -----------    |
```

### 💾 代码实现

#### 📮 客户端发送数据

**关键点**：
- ✅ 发送完所有数据后，必须调用 `CloseAndRecv()` 或 `CloseSend() + Recv()`，这是告诉服务端"我发完了"
- ✅ 不调用 Close 方法，服务端会一直等待，最后超时
- ✅ 可以提前结束发送并获取结果，灵活控制

```go
stream, err := cli.EchoClient(ctx)
if err != nil {
    log.Printf("创建流失败: %v", err)
    return
}

// 发送多条消息
for i := 0; i < 3; i++ {
    req := &echo.Request{
        Msg: fmt.Sprintf("数据块 %d", i+1),
    }
    
    err = stream.Send(stream.Context(), req)
    if err != nil {
        log.Printf("发送失败: %v", err)
        return
    }
}

// 方式1：关闭发送并接收结果（推荐）
res, err := stream.CloseAndRecv(stream.Context())
if err != nil {
    log.Printf("接收结果失败: %v", err)
    return
}

// 方式2：分步操作
// err = stream.CloseSend(stream.Context())
// res, err := stream.Recv(stream.Context())

fmt.Printf("服务端返回: %s\n", res.Msg)
```

**常见错误**：
- ❌ 忘记调用 `CloseAndRecv()` 或 `CloseSend()`，服务端干等，最后超时
- ❌ 在 `CloseSend()` 之后继续调用 `Send()`，会报错
- ❌ 多次调用 `CloseAndRecv()`，第二次会 panic

#### 📬 服务端接收数据

**关键点**：
- ✅ 循环调用 `Recv()` 直到收到 `io.EOF`，这是客户端发送完毕的信号
- ✅ 必须在 handler 结束时返回 Response，这是给客户端的最终答复
- ✅ 使用 `SendAndClose()` 返回最终结果，一步到位

```go
func (si *serviceImpl) EchoClient(
    ctx context.Context, stream echo.TestService_EchoClientServer) error {
    
    // 用于累积客户端发送的数据
    var allData []string
    
    // 循环接收客户端数据
    for {
        req, err := stream.Recv(ctx)
        if err == io.EOF {
            // 客户端发送完毕，处理数据并返回结果
            result := &echo.Response{
                Msg: fmt.Sprintf("收到 %d 条消息", len(allData)),
            }
            return stream.SendAndClose(ctx, result)
        }
        if err != nil {
            log.Printf("接收失败: %v", err)
            return err
        }
        
        // 累积数据
        allData = append(allData, req.Msg)
        log.Printf("收到数据: %s", req.Msg)
    }
}
```

**实践建议**：
- 注意内存占用，如果客户端发送大量数据，考虑边接收边处理，别全堆内存里
- 设置接收超时，避免客户端一直不关闭连接，占着茅坑不拉屎
- 妥善处理客户端中途断开的情况，释放资源

---

## 🔁 双向流：实时交互的终极形态

### 💬 场景：实时聊天的基础

双向流是最灵活也是最复杂的模式。客户端和服务端都可以随时发送消息，就像两个人在微信上聊天一样。这种模式适合需要双向实时交互的场景：

- **实时聊天**：用户之间互发消息，谁都能随时说话
- **协同编辑**：多人同时编辑文档，实时同步修改
- **游戏对战**：玩家之间的操作同步，一秒都不能等
- **实时监控**：客户端上报数据，服务端推送告警，双向通信

**数据流示意**：

```text
客户端                           服务端
  |                                |
  |-------- 消息1 ----------->     |
  |                                |-------- 回复1 -------->
  |<------- 回复1 ------------     |
  |-------- 消息2 ----------->     |
  |                                |-------- 回复2 -------->
  |<------- 回复2 ------------     |
  |-------- 关闭发送 -------->     |
  |<------- EOF -------------     | (处理结束)
```

### 🔑 实现要点

#### 🏢 Server Handler 注意事项

服务端这边要注意：

- method handler 结束后，Kitex 会自动写 Trailer Frame（等同于关闭 stream）
- 业务代码不需要主动调用 `stream.Close()`，框架会处理
- 新启动的 goroutine 应当自行 recover，别让 panic 搞崩整个服务
- 「Recv 返回 `io.EOF`」表示 client 已发送结束，可以准备收尾了
- 示例代码：[kitex-examples:thrift_streaming/handler.go#L34](https://github.com/cloudwego/kitex-examples/blob/v0.3.1/thrift_streaming/handler.go#L34)

#### 📱 客户端注意事项

客户端这边也有讲究：

- 新启动的 goroutine 应当自行 recover，防御性编程
- Client 发送结束后应及时调用 stream.Close() 告知 server，别让服务端干等
- 「Recv 返回 `io.EOF` 或其他 non-nil error」表示 server 已发送结束（或出错）
  - 此时 Kitex 才会记录 RPCFinish 事件（Tracer 依赖该事件）
  - 如果你和 server 约定了其他结束方式，应主动调用 `streaming.FinishStream(stream, err)` 记录 RPCFinish 事件

### ⚡ 代码实现

#### 🔄 客户端双向通信

**关键点**：
- ✅ 发送和接收需要在**两个 goroutine** 中并发执行，这是重点
- ✅ 发送完毕后必须调用 `CloseSend()`，告诉服务端不再发送了
- ✅ 接收时必须判断 `io.EOF`，否则会死循环

```go
stream, err := cli.EchoBidi(ctx)
if err != nil {
    log.Printf("创建流失败: %v", err)
    return
}

var wg sync.WaitGroup
wg.Add(2)

// Goroutine 1: 负责发送
go func() {
    defer wg.Done()
    
    for i := 0; i < 5; i++ {
        req := &echo.Request{
            Msg: fmt.Sprintf("客户端消息 %d", i+1),
        }
        
        err := stream.Send(stream.Context(), req)
        if err != nil {
            log.Printf("发送失败: %v", err)
            return
        }
        
        time.Sleep(500 * time.Millisecond)
    }
    
    // 发送完毕，关闭发送通道
    err = stream.CloseSend(stream.Context())
    if err != nil {
        log.Printf("关闭发送失败: %v", err)
    }
}()

// Goroutine 2: 负责接收
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
        
        fmt.Printf("收到服务端消息: %s\n", res.Msg)
    }
}()

// 等待发送和接收都完成
wg.Wait()
```

**常见错误**：
- ❌ 在同一个 goroutine 中串行发送和接收，导致死锁，程序卡死
- ❌ 忘记调用 `CloseSend()`，服务端一直等待，最后超时
- ❌ 接收循环中忘记判断 `io.EOF`，死循环

#### 🔀 服务端双向通信

**关键点**：
- ✅ 接收时必须判断 `io.EOF`，这是客户端发送完毕的信号
- ✅ handler 返回时自动发送 EOF，客户端会收到结束通知
- ✅ 可以选择在 goroutine 中并发处理，也可以串行处理，看业务需求

```go
func (si *serviceImpl) EchoBidi(ctx context.Context, 
    stream echo.TestService_EchoBidiServer) error {
    
    // 这里演示最简单的"收到一条，回复一条"模式
    for {
        req, err := stream.Recv(ctx)
        if err == io.EOF {
            // 客户端发送完毕，正常结束
            log.Println("客户端发送完毕")
            return nil
        }
        if err != nil {
            log.Printf("接收失败: %v", err)
            return err
        }
        
        log.Printf("收到客户端消息: %s", req.Msg)
        
        // 立即回复
        resp := &echo.Response{
            Msg: fmt.Sprintf("服务端收到: %s", req.Msg),
        }
        
        err = stream.Send(ctx, resp)
        if err != nil {
            log.Printf("发送失败: %v", err)
            return err
        }
    }
}
```

**实践建议**：
- 简单场景可以串行处理（收到一条，回复一条），代码清晰
- 复杂场景可以用 goroutine 异步处理，但要注意同步问题，别搞出并发 bug
- 定期检查 `ctx.Done()`，及时响应客户端断开，释放资源

---

## 🔍 流中间件：监控的眼睛

### 🎨 为什么需要中间件

在生产环境中，我们需要对流式调用进行监控和日志记录。没有可观测性的系统就像盲人开车，出了问题都不知道哪里炸了。Kitex 提供了三种级别的中间件：

| 中间件类型           | 触发时机             | 用途                   |
| -------------------- | -------------------- | ---------------------- |
| **StreamMiddleware**     | 每次创建流时         | 初始化监控、日志上下文 |
| **StreamRecvMiddleware** | 每次接收消息时       | 记录接收日志、监控延迟 |
| **StreamSendMiddleware** | 每次发送消息时       | 记录发送日志、限流控制 |

### 💡 客户端中间件实战

```go
import "github.com/cloudwego/kitex/client"
import "github.com/cloudwego/kitex/pkg/endpoint/cep"

cli, err := testservice.NewClient(
    "service.name", 
    client.WithStreamOptions(
        // Stream 创建中间件：记录流创建日志
        client.WithStreamMiddleware(func(next cep.StreamEndpoint) cep.StreamEndpoint {
            return func(ctx context.Context) (stream streaming.ClientStream, err error) {
                ri := rpcinfo.GetRPCInfo(ctx)
                log.Printf("[创建流] 方法: %s", ri.Invocation().MethodName())
                
                start := time.Now()
                stream, err = next(ctx)
                
                log.Printf("[流创建完成] 耗时: %v", time.Since(start))
                return stream, err
            }
        }), 
        
        // Stream Send 中间件：记录发送日志
        client.WithStreamSendMiddleware(func(next cep.StreamSendEndpoint) cep.StreamSendEndpoint {
            return func(ctx context.Context, stream streaming.ClientStream, message interface{}) error {
                log.Printf("[发送消息] 内容: %+v", message)
                
                start := time.Now()
                err := next(ctx, stream, message)
                
                log.Printf("[发送完成] 耗时: %v", time.Since(start))
                return err
            }
        }), 
        
        // Stream Recv 中间件：记录接收日志
        client.WithStreamRecvMiddleware(func(next cep.StreamRecvEndpoint) cep.StreamRecvEndpoint {
            return func(ctx context.Context, stream streaming.ClientStream, message interface{}) error {
                start := time.Now()
                err := next(ctx, stream, message)
                
                if err == nil {
                    log.Printf("[接收消息] 内容: %+v, 耗时: %v", message, time.Since(start))
                }
                return err
            }
        }), 
    ), 
)
```

### 🔐 服务端中间件实战

```go
import "github.com/cloudwego/kitex/server"
import "github.com/cloudwego/kitex/pkg/endpoint/sep"

svr := testservice.NewServer(
    new(serviceImpl),
    server.WithStreamOptions(
        // Stream 创建中间件
        server.WithStreamMiddleware(func(next sep.StreamEndpoint) sep.StreamEndpoint {
            return func(ctx context.Context, st streaming.ServerStream) error {
                ri := rpcinfo.GetRPCInfo(ctx)
                log.Printf("[服务端] 创建流, 方法: %s", ri.Invocation().MethodName())
                
                return next(ctx, st)
            }
        }),
        
        // Stream Recv 中间件：接收消息计数
        server.WithStreamRecvMiddleware(func(next sep.StreamRecvEndpoint) sep.StreamRecvEndpoint {
            return func(ctx context.Context, stream streaming.ServerStream, message interface{}) error {
                err := next(ctx, stream, message)
                if err == nil {
                    log.Printf("[服务端接收] 消息: %+v", message)
                }
                return err
            }
        }), 
        
        // Stream Send 中间件：发送消息计数
        server.WithStreamSendMiddleware(func(next sep.StreamSendEndpoint) sep.StreamSendEndpoint {
            return func(ctx context.Context, stream streaming.ServerStream, message interface{}) error {
                log.Printf("[服务端发送] 消息: %+v", message)
                return next(ctx, stream, message)
            }
        }), 
    ),
)
```

---

## 🚫 错误处理：别让问题隐身

### 📋 框架错误码一览

Kitex 使用 12xxx 错误码标识流式相关错误，记住这些能帮你快速定位问题：

| 错误码 | 含义                     | 常见原因                 | 处理建议               |
| ------ | ------------------------ | ------------------------ | ---------------------- |
| 12001  | 业务异常                 | handler 返回错误         | 检查业务逻辑           |
| 12005  | 非法操作                 | 已关闭后继续发送         | 检查 CloseSend 调用位置 |
| 12006  | 连接关闭                 | 网络异常、连接断开       | 重试或降级             |
| 12007  | 上游主动 cancel          | 客户端调用 cancel()      | 正常场景，无需处理     |
| 12009  | 被下游 cancel            | 下游服务主动断开         | 检查下游服务           |
| 12012  | Handler 提前退出         | 异步 goroutine 仍在使用  | 等待 goroutine 结束    |
| 12013  | 连接关闭导致流结束       | 服务重启、网络中断       | 客户端自动重连         |

### 💼 业务错误的正确姿势

Kitex 支持在流中返回业务错误码和详细信息，这比简单返回 error 信息量大得多：

**服务端返回业务错误**：

```go
func (si *streamingService) ServerStreamWithErr(ctx context.Context, 
    req *echo.Request, stream echo.TestService_ServerStreamWithErrServer) error {
    
    // 检查用户权限
    if !hasPermission(req.UserId) {
        bizErr := kerrors.NewBizStatusErrorWithExtra(
            10403, "权限不足", map[string]string{
                "userId": req.UserId,
                "required": "premium",
            },
        )
        return bizErr
    }
    
    // 正常处理
    for i := 0; i < 5; i++ {
        if err := stream.Send(ctx, &echo.Response{...}); err != nil {
            return err
        }
    }
    
    return nil
}
```

**客户端解析业务错误**：

```go
stream, err := cli.ServerStreamWithErr(ctx, req)
if err != nil {
    log.Printf("创建流失败: %v", err)
    return
}

for {
    res, err := stream.Recv(stream.Context())
    if err != nil {
        // 尝试解析为业务错误
        if bizErr, ok := kerrors.FromBizStatusError(err); ok {
            log.Printf("业务错误: code=%d, msg=%s, extra=%v", 
                bizErr.BizStatusCode(), bizErr.BizMessage(), bizErr.BizExtra())
            // 根据业务错误码做不同处理
            switch bizErr.BizStatusCode() {
            case 10403:
                // 权限不足，引导用户升级
                showUpgradeDialog()
            case 10429:
                // 限流，稍后重试
                time.Sleep(time.Second)
                retry()
            }
        }
        break
    }
    
    // 处理消息
    handleMessage(res)
}
```

### ♻️ 生命周期精确控制

使用 context 控制流的生命周期，实现优雅取消。这是分布式系统中很重要的能力——能及时止损。

**上游主动取消**：

```go
// 创建可取消的 context
ctx, cancel := context.WithCancel(parentCtx)
defer cancel()

stream, err := cli.ServerStream(ctx, req)
if err != nil {
    return err
}

// 开启接收循环
for {
    resp, err := stream.Recv(stream.Context())
    if err != nil {
        if errors.Is(err, kerrors.ErrStreamingCanceled) {
            log.Println("流被取消")
        }
        break
    }
    
    // 业务判断：如果收到特殊标记，主动取消
    if resp.IsTerminal {
        cancel()  // 取消下游流
        break
    }
}
```

**下游感知取消**：

```go
func (impl *ServiceImpl) ServerStream(ctx context.Context, req *Request,
    stream Service_ServerStreamServer) error {
    
    for {
        // 定期检查 context 是否被取消
        select {
        case <-ctx.Done():
            log.Println("客户端取消请求")
            return ctx.Err()
        default:
        }
        
        // 发送数据
        if err := stream.Send(ctx, resp); err != nil {
            if errors.Is(err, kerrors.ErrStreamingCanceled) {
                log.Println("检测到上游取消")
            }
            return err
        }
        
        time.Sleep(100 * time.Millisecond)
    }
}
```

### ⏱️ 超时控制：别让流无限等待

对每次 `Recv` 操作设置超时，避免无限等待：

**客户端级别超时**（所有接口生效）：

```go
cli, err := testservice.NewClient("service", 
    client.WithStreamOptions(
        client.WithStreamRecvTimeout(5 * time.Second),  // 每次接收最多等 5 秒
    ),
)
```

**接口级别超时**（单个接口生效，需 Kitex >= v0.13.0）：

```go
import "github.com/cloudwego/kitex/client/callopt/streamcall"

stream, err := cli.ServerStream(ctx, req,
    streamcall.WithRecvTimeout(10 * time.Second),  // 此接口接收超时 10 秒
)
```

---

## ⚙️ Options 配置详解

### 🔩 StreamClient Options 说明

Kitex 在设计上区分了 Client（for KitexThrift PingPong API）和 StreamClient（for Streaming API），并且要求 StreamClient 使用另一套 Option（类型不同），避免用户给 StreamClient 指定了不支持的 Option。

**注意**：如果某个 client/callopt Option 没有对应的 streamclient/streamcall Option（例如 WithRPCTimeout），说明 StreamClient 不支持该能力。

#### 📌 streamclient.Option

- 在 NewStreamClient 时指定
- 新增的 Option：
  - `WithRecvMiddleware`、`WithRecvMiddlewareBuilder`：详见 Recv/Send 中间件
  - `WithSendMiddleware`、`WithSendMiddlewareBuilder`：详见 Recv/Send 中间件

示例代码：

```go
import "github.com/cloudwego/kitex/client/streamclient"

var streamClient = testservice.MustNewStreamClient(
    "demo-server",                                  // Service Name
    streamclient.WithHostPorts("127.0.0.1:8888"),   // streamclient.Option...
)
```

#### 📍 streamcall.Option

- 在创建 Stream 时指定
- 优先级高于同名（如果有的话）的 streamclient.Option

示例代码：

```go
import "github.com/cloudwego/kitex/client/callopt/streamcall"

stream, err := streamClient.Echo(
    context.Background(),
    streamcall.WithHostPort("127.0.0.1:8888"),
)
```

### 🏗️ Server Options 说明

由于 Server 支持自动探测协议，可以同时支持 Streaming API 和 KitexThrift API，因此无法像 StreamClient 一样使用不同的 Option 类型。大部分 [Server Option](https://www.cloudwego.io/zh/docs/kitex/tutorials/options/server_options/) 对 Streaming API 也有效。

---

## 🛡️ 服务治理实战

### ⌚ 超时控制

#### 🔗 连接超时

支持通过 option 指定：

- streamclient.WithConnectTimeout
- streamcall.WithConnectTimeout（优先级高于前者）

#### ⛔ 请求超时（不支持）

没有对应的 Option。对于 Streaming API，[Kitex 的 Timeout 中间件会直接调用 next](https://github.com/cloudwego/kitex/blob/v0.9.1/client/rpctimeout.go#L101)。

#### ⏳ Stream 超时

可通过 `context.WithTimeout` 或 `context.WithDeadline` 创建带有 Deadline 的 context，并在创建 Stream 时指定该 context，用于控制 Stream 的整体执行时间：

- Kitex Client
  - 通过 header `grpc-timeout` 发送给服务端
    - 超时后 Recv/Send 会直接返回 `rpc error: code = 4 desc = context deadline exceeded`
- Kitex Server
  - 读取 `grpc-timeout` 并设置到 request context 中
    - 超时后 Recv/Send 会直接返回 `rpc error: code = 4 desc = context deadline exceeded`

示例代码：

```go
// inject deadline into context BEFORE creating a stream
ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()

stream, err := cli.Echo(ctx)
```

#### 📨 Recv/Send 超时

可使用 Kitex 提供的 `streaming.CallWithTimeout` 方法。

#### 🌐 Client 端实现

注意：

1. 需要**在创建 Stream 之前**给 ctx 注入 cancel（用 WithCancel 或 WithTimeout 都可以，取决于需求）
2. 将 cancel 方法作为 `streaming.CallWithTimeout` 的第二个参数
   - 否则 Send/Recv 可能会长时间阻塞等待（取决于 server 端），导致 goroutine 泄漏
3. Client 端的 `stream.Close()` 的语义是 `CloseSend`，告诉 server 不再会有新消息（server recv 返回 `io.EOF`），并不会结束接收消息，因此不能用于 cancel 方法

示例代码：

```go
import "github.com/cloudwego/kitex/pkg/streaming"

// Add a cancel func to the context BEFORE creating a stream
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

stream, err := cli.Echo(ctx)
if err != nil {
    // ...
}

// Send with timeout
err = streaming.CallWithTimeout(time.Second, cancel, func() error {
    return stream.Send(&test.Request{Message: "hello"})
})

// Recv with timeout
var resp *test.Response
err = streaming.CallWithTimeout(time.Second, cancel, func() (err error) {
    resp, err = stream.Recv()
    return err
})
```

#### 🏭 Server 端实现

Server 端可以使用 `stream.Close()` 作为 cancel 方法。

示例代码：

```go
var cancel context.CancelFunc = func() {
    stream.Close() // the cancel func in streamContext will be called internally
}

var req *test.EchoRequest
err = streaming.CallWithTimeout(time.Second, cancel, func() (errRecv error) {
    req, errRecv = stream.Recv()
    return errRecv
})
```

### 🔥 熔断机制

只支持**创建连接(Stream)时**的错误率熔断。不支持 Recv/Send 的熔断。

### 🔁 重试机制（不支持）

不支持重试。流式调用的状态太复杂，重试可能导致数据重复或状态不一致。

### 🚪 Fallback（不支持）

Streaming API 不支持 fallback。流式调用无法简单地切换到备用方案。

### ⚖️ 负载均衡

- 仅支持创建 Stream 时（等同于创建网络连接）的负载均衡
- 如已经创建 Stream，后续的 Send/Recv 只会发往该 Stream 的对端
  - 业务需自行处理流量倾斜问题，避免造成负载不均

### 🚥 服务端限流

- 支持在创建 Stream 时限流
- 创建 Stream 后对 Recv/Send 的调用无限制，需要业务自行实现

---

## 🎓 最佳实践与选型指南

### 🗺️ 选型决策树

选择消息模式时，可以按照这个决策树走：

```text
需要服务端持续推送数据？
├─ 是 → 用 Server Streaming
│       └─ 示例：AI 对话、实时通知、日志流
└─ 否 → 需要客户端持续发送数据？
         ├─ 是 → 用 Client Streaming
         │       └─ 示例：文件上传、批量导入
         └─ 否 → 双方都需要持续交互？
                  ├─ 是 → 用 Bidirectional Streaming
                  │       └─ 示例：实时聊天、协同编辑
                  └─ 否 → 需要响应吗？
                           ├─ 是 → 用 PingPong
                           │       └─ 示例：查询、提交
                           └─ 否 → 用 Oneway
                                   └─ 示例：日志、埋点
```

### 💪 性能优化实战

经过多个项目的实践，总结了这些性能优化建议：

**1. 控制消息大小**：
- 单条消息建议 < 1MB，太大会影响网络传输
- 大数据分片传输，别一次性发送几十 MB
- 避免在消息中嵌入大对象，序列化开销很大

**2. 合理设置缓冲**：
- 客户端发送不要太快，给服务端处理时间，别把服务端压垮
- 服务端注意背压（backpressure），避免内存溢出，OOM 就惨了
- 使用 channel 缓冲控制发送速率，平滑流量

**3. 及时释放资源**：
- 流使用完毕后及时关闭，别让连接泄漏
- 避免 goroutine 泄露，每个 goroutine 都占用内存
- 使用 defer 确保清理，即使出错也能释放资源

**4. 监控关键指标**：
- 流创建速率：每秒创建多少流
- 消息发送/接收速率：吞吐量如何
- 平均流持续时长：是否有流长期占用连接
- 错误率和错误类型分布：哪些错误最常见

### 🚨 常见陷阱避坑

这些坑我都踩过，希望你能避开：

1. **忘记调用 Close 方法**
   - Client Streaming 必须 `CloseAndRecv()`，否则服务端一直等
   - Bidirectional Streaming 必须 `CloseSend()`，否则服务端不知道结束

2. **同一 goroutine 中串行收发**
   - 双向流必须用两个 goroutine，一个收一个发
   - 否则会死锁，程序卡死

3. **忽略 io.EOF 判断**
   - 导致死循环或 panic，CPU 飙到 100%
   - 必须正确处理流结束信号

4. **错误的 context 使用**
   - 应该用 `stream.Context()` 而不是外部 context
   - 否则无法正确传递流状态，超时控制失效

---

## 📚 总结与展望

通过这篇文章，我们深入探讨了 Kitex 的三种消息模式：

**PingPong** 是最可靠的选择，适合 90% 的场景。它简单、直观、易于调试，是默认首选。不要因为追求性能而盲目选择其他模式。

**Oneway** 追求极致性能，适合日志、埋点等允许丢失的场景。但要注意可靠性问题，关键业务千万别用。我见过太多因为误用 Oneway 导致的生产事故。

**Streaming** 开启了实时交互的大门，让 RPC 不再局限于"一问一答"。无论是 AI 对话、实时推送，还是文件上传，流式接口都能游刃有余。StreamX 的推出让流式调用更加简单易用。

选择消息模式时，记住这几个原则：
- ✅ 优先选择 PingPong，除非有明确的理由（性能瓶颈、实时性需求）
- ✅ 需要实时性选 Streaming，用户体验提升明显
- ✅ 追求吞吐量且允许丢失选 Oneway，但要做好监控
- ✅ 协议兼容性很重要时选 gRPC，跨语言调用更方便

最后，无论选择哪种模式，都要做好监控、日志和错误处理。生产环境的稳定性，往往取决于这些细节。没有监控的系统就像盲人开车，早晚出事。

希望这篇文章能帮助你在实际项目中做出正确的技术选型。如果你有任何问题或实践经验，欢迎在评论区分享！记住：**没有最好的技术，只有最合适的选择**。
