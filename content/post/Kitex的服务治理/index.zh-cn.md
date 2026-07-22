---
date : '2025-01-20T10:00:00+08:00'
draft : false
title : 'Kitex 的服务治理'
image : ""
categories : ["个人项目"]
tags : ["Kitex", "RPC", "微服务", "服务治理", "负载均衡", "熔断降级"]
description : "深入探讨 Kitex 框架中的服务治理能力，包括注册发现、负载均衡、熔断降级、限流、超时重试和可观测性等核心功能"
---

## 🧠 服务治理概述

服务治理是微服务架构中的关键能力，用于管理服务间的通信、保证系统稳定性和可靠性。Kitex 作为字节跳动开源的高性能 Go RPC 框架，内置了完整的服务治理功能，包括服务注册与发现、负载均衡、熔断降级、限流控制、超时重试等。

通过服务治理，我们可以：
- 自动发现和管理服务实例
- 智能分配请求流量
- 快速隔离故障节点
- 防止级联故障扩散
- 监控和追踪请求链路

---

## 🗂️ 服务注册与发现（Registry）

### 📒 什么是服务注册与发现

服务注册与发现是微服务的基础设施。服务启动时向注册中心注册自己的地址和元数据，客户端通过注册中心获取可用的服务实例列表。

Kitex 支持多种注册中心，包括：
- **etcd**：分布式键值存储，高可用和强一致性
- **Nacos**：阿里开源的服务发现中心
- **Consul**：HashiCorp 的服务网格工具
- **Zookeeper**：分布式协调系统

### 🛠️ 使用 etcd 作为注册中心

首先安装 Kitex 的 etcd 扩展：

```bash
go get github.com/kitex-contrib/registry-etcd
```

服务端注册实例：

```go
package main

import (
	"context"
	"github.com/cloudwego/kitex/pkg/rpcinfo"
	"github.com/cloudwego/kitex/server"
	etcd "github.com/kitex-contrib/registry-etcd"
	"log"
)

func main() {
	// 创建 etcd 注册器
	r, err := etcd.NewEtcdRegistry(
		[]string{"127.0.0.1:2379"}, // etcd 服务器地址
	)
	if err != nil {
		log.Fatal(err)
	}

	// 创建服务器，并注册到 etcd
	svr := server.NewServer(
		new(UserServiceImpl),
		server.WithRegistry(r),
		server.WithServiceAddr(rpcinfo.NewNetAddr("tcp", "127.0.0.1:8081")),
	)

	if err := svr.Run(); err != nil {
		log.Fatal(err)
	}
}
```

客户端从注册中心发现服务：

```go
package main

import (
	"context"
	"github.com/cloudwego/kitex/client"
	etcd "github.com/kitex-contrib/registry-etcd"
	"log"
)

func main() {
	// 创建 etcd 解析器（发现服务）
	r, err := etcd.NewEtcdResolver(
		[]string{"127.0.0.1:2379"}, // etcd 服务器地址
	)
	if err != nil {
		log.Fatal(err)
	}

	// 创建客户端，通过服务名发现服务
	cli, err := user.NewClient(
		"user-service", // 服务名
		client.WithResolver(r),
	)
	if err != nil {
		log.Fatal(err)
	}

	resp, err := cli.GetUser(context.Background(), &user.GetUserReq{UserId: "123"})
	if err != nil {
		log.Fatal(err)
	}
	log.Println(resp)
}
```

### 💓 心跳保活机制

Kitex 提供心跳保活机制，定期向注册中心续约，确保服务实例信息的及时性：

```go
svr := server.NewServer(
	new(UserServiceImpl),
	server.WithRegistry(r),
	server.WithServiceAddr(rpcinfo.NewNetAddr("tcp", "127.0.0.1:8081")),
)
```

etcd 的心跳和过期机制：
- 服务启动时向 etcd 注册，带有 TTL（生存时间）
- 定期续约以保持注册信息有效
- 服务异常停止时，ttl 过期后自动从注册中心移除

---

## ⚖️ 负载均衡策略（LoadBalancer）

### 🔍 负载均衡的重要性

负载均衡是分散流量、提高系统吞吐量和可靠性的关键。Kitex 提供多种开箱即用的负载均衡策略。

Kitex 内置的负载均衡策略包括：

- WeightedRoundRobin：该 LoadBalancer 使用的是基于权重的轮询策略，也是 Kitex 的默认策略。该 LoadBalancer 能让所有下游实例拥有最小的同时 inflight 请求数，以减少下游过载情况的发生。如果所有的实例的权重都一样，会使用一个纯轮询的实现，来避免加权计算的一些额外开销。

- InterleavedWeightedRoundRobin（kitex >= v0.7.0）：与 [WeightedRoundRobin](https://www.cloudwego.io/zh/docs/kitex/tutorials/service-governance/loadbalance/#weightedroundrobin) 相同， 该 LoadBalancer 使用的也是基于权重的轮询策略。区别在于 [WeightedRoundRobin](https://www.cloudwego.io/zh/docs/kitex/tutorials/service-governance/loadbalance/#weightedroundrobin) 的空间复杂度是将所有实例按权重选择一遍的最小正周期（所有实例权重的和除以所有实例权重的最大公约数）， 而该 LoadBalancer 的空间复杂度是下游实例数，在下游实例数权重总和非常大时更节省空间。

- WeightedRandom：顾名思义，这个 LoadBalancer 使用的是基于权重的随机策略。这个 LoadBalancer 会依据实例的权重进行加权随机，并保证每个实例分配到的负载和自己的权重成比例。如果所有的实例的权重都一样，会使用一个纯随机的实现，来避免加权计算的一些额外开销。

- Alias Method（kitex >= v0.9.0）：使用别名方法的 LoadBalancer ，具体来说实现的是 [Darts, Dice, and Coins](https://www.keithschwarz.com/darts-dice-coins/) 中的 Vose’s Alias Method，使用 O(n) 时间生成别名表，之后在 O(1) 时间内选取实例，选取效率比 [WeightedRandom](https://www.cloudwego.io/zh/docs/kitex/tutorials/service-governance/loadbalance/#weightedrandom) 更高

- ConsistentHash：一致性哈希主要适用于对上下文（如实例本地缓存）依赖程度高的场景，如希望同一个类型的请求打到同一台机器，则可使用该负载均衡方法。

- Tagging Based：提供了一个基于标签的负载均衡策略，允许根据客户端上的标签将集群划分为不同的子集。

  这适用于有状态服务或多租户服务的场景，使得可以对服务实例进行更细粒度的控制和路由。

  - 基于标签的子集划分: 便于特定请求定向到相应的服务实例；
  - 适用于多态服务: 支持有状态服务的特定需求，在多租户环境中实现请求路由；
  - 自定义标签函数: 允许通过自定义函数使用标签，以实现更复杂的负载均衡策略。

Kitex 默认使用的是 WeightedRoundRobin。



### 💡 选择合适的策略

不同的负载均衡策略适用于不同场景：

| 策略 | 优势 | 适用场景 |
|------|------|--------|
| WeightedRoundRobin | 分布均匀，公平性好 | 大多数通用场景 |
| WeightedRandom | 实现简单，随机分布 | 服务实例均匀，无状态服务 |
| Alias Method | O(1) 选实例，效率最高 | 大量实例且权重差异大 |
| ConsistentHash | 会话亲和性 | 需要粘性会话的服务 |

### 🔬 自定义负载均衡器

如果内置策略不满足需求，可以实现自定义策略：

```go
package main

import (
	"github.com/cloudwego/kitex/pkg/loadbalance"
)

// 加权轮询负载均衡器
type WeightedRoundRobinBalancer struct {
	weights []int
	current int
}

func (b *WeightedRoundRobinBalancer) Choose(
	ctx context.Context,
	request interface{},
	ep []loadbalance.Endpoint,
) loadbalance.Endpoint {
	if len(ep) == 0 {
		return nil
	}

	// 简化实现：按权重轮询
	total := 0
	for _, w := range b.weights {
		total += w
	}

	b.current = (b.current + 1) % total
	current := 0

	for i, w := range b.weights {
		current += w
		if b.current < current {
			return ep[i]
		}
	}

	return ep[0]
}

func (b *WeightedRoundRobinBalancer) Rebalance(ep loadbalance.Builder) {}
```

---

## 🚨 熔断（Circuit Breaker）

### ❗ 熔断的必要性

在分布式系统中，某个服务可能出现故障，如果还持续向其发送请求，会造成资源浪费和级联故障。熔断器模式通过快速失败，保护系统。通过设置一些动态开关，当下游出错时，手动的关闭对下游的调用；

### 🔄 熔断原理

#### 🎚️ 熔断策略

**熔断器的思路很简单：根据RPC的成功失败情况，限制对下游的访问**

通常熔断器分为三个时期：

- CLOSED：RPC 正常时，为 CLOSED
- OPEN：当 RPC 错误增多时，熔断器会被触发
- HALFOPEN：OPEN 后经过一定的冷却时间，熔断器变为 HALFOPEN，HALFOPEN 时会对下游进行一些有策略的访问，然后根据结果决定是变为 CLOSED，还是 OPEN

熔断器有三种状态：

```
[CLOSED] ---> tripped ----> [OPEN]<-------+
    ^                          |           ^
    |                          v           |
    +                          |      detect fail
    |                          |           |
    |                    cooling timeout   |
    ^                          |           ^
    |                          v           |
    +--- detect succeed --<-[HALFOPEN]-->--+
```

#### 🔔 触发策略

Kitex 默认提供了三个基本的熔断触发策略：

- 连续错误数达到阈值 (ConsecutiveTripFunc)
- 错误数达到阈值 (ThresholdTripFunc)
- 错误率达到阈值 (RateTripFunc)

当然，你可以通过实现 TripFunc 函数来写自己的熔断触发策略；

Circuitbreaker 会在每次 Fail 或者 Timeout 时，去调用 TripFunc，来决定是否触发熔断

#### ❄️ 冷却策略

进入 OPEN 状态后，熔断器会冷却一段时间，默认是 10 秒，当然该参数可配置 (CoolingTimeout)；

在这段时期内，所有的 IsAllowed() 请求将会被返回 false；

冷却完毕后进入 HALFOPEN；

#### 🕒 半打开时策略

在 HALFOPEN 时，熔断器每隔 " 一段时间 " 便会放过一个请求，当连续成功 " 若干数目 " 的请求后，熔断器将变为 CLOSED； 如果其中有任意一个失败，则将变为 OPEN；

该过程是一个逐渐试探下游，并打开的过程；

上述的 " 一段时间 “(DetectTimeout) 和 " 若干数目 “(DEFAULT_HALFOPEN_SUCCESSES) 都是可以配置的；

### 💻 在 Kitex 中使用熔断

Kitex 提供了熔断器的实现，但是没有默认开启，需要用户主动使用。下面简单介绍一下如何使用以及 Kitex 熔断器的策略。

```go
import (
        ...
        "github.com/cloudwego/kitex/client"
        "github.com/cloudwego/kitex/pkg/circuitbreak"
        "github.com/cloudwego/kitex/pkg/rpcinfo"
)

// GenServiceCBKeyFunc returns a key which determines the granularity of the CBSuite
func GenServiceCBKeyFunc(ri rpcinfo.RPCInfo) string {
        // circuitbreak.RPCInfo2Key returns "$fromServiceName/$toServiceName/$method"
        return circuitbreak.RPCInfo2Key(ri)
}

func main() {
        // build a new CBSuite with
        cbs := circuitbreak.NewCBSuite(GenServiceCBKeyFunc)

        var opts []client.Option

        // add to the client options
        opts = append(opts, client.WithCircuitBreaker(cbs))

        // init client
        cli, err := echoservice.NewClient(targetService, opts...)

        // update circuit breaker config for a certain key (should be consistent with GenServiceCBKeyFunc)
        // this can be called at any time, and will take effect for following requests
        cbs.UpdateServiceCBConfig("fromServiceName/toServiceName/method", circuitbreak.CBConfig{
                Enable: true,
                ErrRate: 0.3,   // requests will be blocked if error rate >= 30%
                MinSample: 200, // this config takes effect if sampled requests are more than `MinSample`
        })

        // send requests with the client above
        ...
}
```

Kitex 大部分服务治理模块都是通过 middleware 集成，熔断也是一样。Kitex 提供了一套 CBSuite，封装了服务粒度的熔断器和实例粒度的熔断器。

- 服务粒度熔断
  - 按照服务粒度进行熔断统计，通过 WithMiddleware 添加。服务粒度的具体划分取决于 Circuit Breaker Key，既熔断统计的 key，初始化 CBSuite 时需要传入 **GenServiceCBKeyFunc**，默认提供的是 circuitbreak.RPCInfo2Key ，该 key 的格式是 `fromServiceName/toServiceName/method`，即按照方法级别的异常做熔断统计。
- 实例粒度熔断
  - 按照实例粒度进行熔断统计，主要用于解决单实例异常问题，如果触发了实例级别熔断，框架会自动重试。
  - 注意，框架自动重试的前提是需要通过 **WithInstanceMW** 添加，WithInstanceMW 添加的 middleware 会在负载均衡后执行。
- 熔断阈值及**阈值变更**
  - 默认的熔断阈值是 `ErrRate: 0.5, MinSample: 200`，错误率达到 50% 触发熔断，同时要求统计量 >200。若要调整阈值，调用 CBSuite 的 `UpdateServiceCBConfig` 和 `UpdateInstanceCBConfig` 来更新 Key 的阈值。

---

## 🛟 降级（FallBack）

### 📘 功能说明

业务在 RPC 请求失败后通常会有一些降级措施保证有效返回（比如请求超时、熔断后，构造默认返回），Kitex 的 Fallback 支持对所有异常请求进行处理。同时，因为业务异常通常会通过 Resp（BaseResp） 返回，所以也支持对 Resp 进行处理。

#### 📋 支持降级的结果类型

- **RPC** **Error**：RPC 请求异常，如超时、熔断、限流、协议等 RPC 层面的异常
- **业务 Error**：业务自定义的异常，区别于 RPC 异常
- **Resp**：在没有使用业务异常的情况下，用户会在 Resp（BaseResp） 中定义错误返回，所以也支持对 Resp 判断做 fallback

#### 📡 监控上报

Fallback 后可能直接返回成功的 Resp，对用户而言是一次成功请求，但 RPC 层面还是失败请求，所以监控默认以原来的结果上报，但支持配置化调整为以 Fallback 结果上报。框fallback.Policy 提供了 **EnableReportAsFallback()** 方法可以选择以 Fallback 结果上报。

**注意**：如果原结果本来就不是 RPC 失败（业务 Error），但如果在 Fallback 里返回了 error，即使 设置了 EnableReportAsFallback，框架也不会以 Fallback 结果上报。

| **原结果**                                  | **是否使用 EnableReportAsFallback()** | **上报结果**                                                 |
| ------------------------------------------- | ------------------------------------- | ------------------------------------------------------------ |
| RPC 失败                                    | 是                                    | fallback 结果                                                |
| RPC 失败                                    | 否                                    | is_error=1 (rpcinfo.GetRPCInfo(ctx).Stats().Error() is not nil) |
| 业务错误 （Biz Err 或 BaseResp 非成功状态） | 是/否                                 | is_error=0 (rpcinfo.GetRPCInfo(ctx).Stats().Error() is nil)  |

### 🔌 使用方式

#### 🧷 Client维度限制

```go
import (
    "github.com/cloudwego/kitex/client"
)

var opts []client.Option
opts = append(opts, client.WithFallback(yourFallbackPolicy))

xxxCli := xxxservice.NewClient("target_service", opts...)
```

#### 📞 Call维度配置

```go
import (
    "github.com/cloudwego/kitex/client/callopt"
)

xxxCli.XXXMethod(ctx, req, callopt.WithFallback(yourFallbackPolicy))
```

### 🛡️ 降级策略

#### 📐 FallBack Func定义

Kitex 提供两种 Fallback Func 定义：

1. 以 XXXArgs/XXXResult 作为 req/resp 参数，与 Middleware 相同
2. 以真实的 RPC Req/Resp 作为参数，与 Handler 的参数类型相同

**XXXArgs/XXXResult 作为 req/resp 参数**

注意：必须通过 result.SetSuccess(yourFallbackResult) 替换原返回值。

后者符合使用直觉，对用户更加友好，但不兼容有多个请求参数的 API，因此框架默认使用前一种方法。

```go
// Func is the definition for fallback func, which can do fallback both for error and resp.
// Notice !! The args and result are not the real rpc req and resp, are respectively XXArgs and XXXResult of generated code.
// setup eg: client.WithFallback(fallback.NewFallbackPolicy(yourFunc))
type Func func(ctx context.Context, args utils.KitexArgs, result utils.KitexResult, err error) (fbErr error)

// use demo
client.WithFallback(
fallback.NewFallbackPolicy(
func(ctx context.Context, args utils.KitexArgs,
result utils.KitexResult, err error) (fbErr error) {
// your fallback logic...
result.SetSuccess(yourFallbackResult)
return
}))
```

**真实的** **RPC** **Req/Resp 作为参数**

通过使用 Kitex 提供的 **fallback.UnwrapHelper**，可以定义签名为 RealReqRespFunc 的 Fallback Func，参数类型和 Handler 的 req、resp 一致。

注意：如果需要返回 resp，这里需要构造真实的 RPC resp 作为返回值，Helper 会调用 SetSuccess 方法 替换原返回值。

```go
// RealReqRespFunc is the definition for fallback func with real rpc req as param, and must return the real rpc resp.
// setup eg: client.WithFallback(fallback.NewFallbackPolicy(fallback.UnwrapHelper(yourRealReqRespFunc)))
type RealReqRespFunc func(ctx context.Context, req, resp interface{}, err error) (fbResp interface{}, fbErr error)

// use demo
client.WithFallback(fallback.NewFallbackPolicy(fallback.UnwrapHelper(func(ctx context.Context, req, resp interface{}, err error) (fbResp interface{}, fbErr error) {
// your fallback logic...
return fbResp, fbErr
}))
```

#### 🏭 构造 Fallback Policy

默认的构造方法 NewFallbackPolicy，框架会对 Error 和 Resp 均触发 Fallback 执行，为了方便业务使用，如果用户是希望对 Error 或者 超时/熔断 做 fallback，框架也提供了封装。

- **对 Error 和 Resp 均做判断执行 Fallback**

  ```go
  // 方法1：XXXArgs/XXXResult as params
  fallback.NewFallbackPolicy(func(ctx context.Context, args utils.KitexArgs, result utils.KitexResult, err error) (fbErr error) {
     // your fallback logic...
     result.SetSuccess(yourFallbackResult)
     return
  })
  
  // 方法2：real rpc req/resp as params
  fallback.NewFallbackPolicy(fallback.UnwrapHelper(func(ctx context.Context, req, resp interface{}, err error) (fbResp interface{}, fbErr error) {
     // your fallback logic...
     return
  })
  ```

- **只对 Error（包括业务 Error） 进行 Fallback**

  ```go
  // 1: XXXArgs/XXXResult as params
  fallback.ErrorFallback(func(ctx context.Context, args utils.KitexArgs, result utils.KitexResult, err error) (fbErr error) {
     // your fallback logic...
     result.SetSuccess(yourFallbackResult)
     return
  })
  
  // 2: real rpc req/resp as params
  fallback.ErrorFallback(fallback.UnwrapHelper(func(ctx context.Context, req, resp interface{}, err error) (fbResp interface{}, fbErr error) {
     // your fallback logic...
     return
  })
  ```

- **只对超时和熔断 Error 进行 Fallback**

  ```go
  // 1: XXXArgs/XXXResult as params
  fallback.TimeoutAndCBFallback(func(ctx context.Context, args utils.KitexArgs, result utils.KitexResult, err error) (fbErr error) {
     // your fallback logic...
     result.SetSuccess(yourFallbackResult)
     return
  })
  
  // 2: real rpc req/resp as params
  fallback.TimeoutAndCBFallback(fallback.UnwrapHelper(func(ctx context.Context, req, resp interface{}, err error) (fbResp interface{}, fbErr error) {
     // your fallback logic...
     return
  }))
  ```

---

## 📈 限流控制（Rate Limiting）

### ❓ 为什么需要限流

限流防止流量突增导致服务过载。通过限制单位时间内的请求数，保护系统稳定性。

### 🚦 实现限流

目前 Kitex 支持用户自定义的 QPS 限流器和连接数限流器，同时提供了默认的实现。

#### 🎛️ 默认限流器

```go
import "github.com/cloudwego/kitex/pkg/limit"

func main() {
	svr := xxxservice.NewServer(handler, server.WithLimit(&limit.Option{MaxConnections: 10000, MaxQPS: 1000}))
	svr.Run()
}
```

参数说明：

- `MaxConnections` 表示最大连接数
- `MaxQPS` 表示最大 QPS
- `UpdateControl` 提供动态修改限流阈值的能力

底层实现

- 默认限流器分别使用 ConcurrencyLimiter 和 RateLimiter 对最大连接数和最大 QPS 进行限流。
  - ConcurrencyLimiter：简单的计数器；
  - RateLimiter：这里的限流算法采用了 " 令牌桶算法 “。

#### 🔧 自定义限流器

```go
import (
    "context"
    "time"

    "github.com/cloudwego/kitex/pkg/limiter"
    "github.com/cloudwego/kitex/pkg/rpcinfo"
    "github.com/cloudwego/kitex/server"
)

type qpsLimiter struct{}

func (l *qpsLimiter) Acquire(ctx context.Context) bool {
    ri := rpcinfo.GetRPCInfo(ctx)
    md := ri.From().Method()
    return acquire(md) // return true to allow this request
}

func (l *qpsLimiter) Status(ctx context.Context) (max, current int, interval time.Duration) {
    // max: the maximum number of requests allowed in the interval;
    // current: the remaining number of requests allowed in the interval;
    return
}

type connectionLimiter struct{}

func (l *connectionLimiter) Acquire(ctx context.Context) bool {
    ri := rpcinfo.GetRPCInfo(ctx)
    addr := ri.From().Address()
    return acquire(addr) // return true to allow this connection
}

func (l *connectionLimiter) Release(ctx context.Context) {
    ri := rpcinfo.GetRPCInfo(ctx)
    addr := ri.From().Address()
    return release(addr) // release occupied resource by the connection, only called after the release is successful.
}

func (l *connectionLimiter) Status(ctx context.Context) (limit, occupied int) {
    // limit: the maximum number of connections allowed.
    // occupied: the number of existing connections.
    return
}

func main() {
    myQPSLimiter := &qpsLimiter{}
    myConnectionLimiter := &connectionLimiter{}
    svr := xxxservice.NewServer(handler, server.WithQPSLimiter(myQPSLimiter), server.WithConnectionLimiter(myConnectionLimiter))
    svr.Run()
}
```

### 🛰️ 监控

默认限流器定义了 `LimitReporter` 接口，用于限流状态监控，例如当前连接数过多、QPS 过大等。

如有需求，用户需要自行实现该接口，并通过 `WithLimitReporter` 注入。

```go
// LimitReporter is the interface define to report(metric or print log) when limit happen
type LimitReporter interface {
    ConnOverloadReport()
    QPSOverloadReport()
}
```



## ⏱️ 超时（Timeout）

Kitex 中共有几种「超时」：客户端连接超时(Connection Timeout)、客户端请求超时(RPC Timeout)、服务端读写超时(Read/Write Timeout)、服务端退出超时(Exit Wait Timeout)。

### ⌛ 客户端超时

#### ⏰ 配置项

- 连接超时：ConnTimeout (default=50ms)
  - 建立一条新连接的最大等待时间；
  - 可设置为任意值（无上限）；如未设置，默认值为 50ms；
  - 如经常遇到 dial timeout 可考虑调大该值，及使用长连接池（详见 client.WithLongConnection）。

- 请求超时：RPCTimeout (default=0, 不限时)
  - 限制一次 rpc 调用的最大用时；如超时，返回 `kerrors.ErrRPCTimeout`；
  - 可指定任意值（无上限）；如未指定，默认为 0，表示不限制等待时间；
  - 超时默认不会重试。

#### ⏲️ 配置方式

##### 🧾 代码配置 - Client Option（Client 粒度配置）

在初始化 client 时传入：

```go
import "github.com/cloudwego/kitex/client"

cli, err := xxx.NewClient(targetService,
    client.WithConnectTimeout(100 * time.Millisecond),
    client.WithRPCTimeout(2 * time.Second))
```

##### 💱 代码配置 - Call Option（请求粒度配置，优先级高于 client option）

发起请求时传入：

```go
import "github.com/cloudwego/kitex/client/callopt"

rsp, err := cli.YourMethod(ctx, req,
    callopt.WithConnectTimeout(100 * time.Millisecond))
    callopt.WithRPCTimeout(2 * time.Second))
```

##### ⚙️ 动态配置 - TimeoutProvider（优先级低于前述 Option）

适用于需要动态配置的场景，每次请求前，Client 会调用 TimeoutProvider 获取 RPCTimeout 和 ConnectionTimeout。

在初始化 client 时传入用户自定义的 `rpcinfo.TimeoutProvider`：

```go
import (
    "github.com/cloudwego/kitex/client"
    "github.com/cloudwego/kitex/pkg/rpcinfo"
)

type UserTimeoutProvider struct {}

func (UserTimeoutProvider) Timeouts(ri rpcinfo.RPCInfo) rpcinfo.Timeouts {
    // 需返回 RPCTimeout、ConnectTimeout
    // ReadWriteTimeout 实际未被使用，建议返回值与 RPCTimeout 相同
}

opt := client.WithTimeoutProvider(&UserTimeoutProvider{})
cli, err := xxx.NewClient(targetService, opt)
```

### 🛎️ 服务端超时

#### ⏳ 配置项

- ReadWriteTimeout (default=5s)
  - 在连接上读写数据所能忍受的最大等待时间，主要为防止异常连接卡住协程；
  - 不是 Handler 执行超时时间；
  - 只在 server 端生效，一般无需关心。

举例：client 端数据分多次发送，如果发送间隔过长，会触发 server 端读等待超时；这时需考虑调大 ReadWriteTimeout。

- ExitWaitTime（default=5s）
  - Server 在收到退出信号时的等待时间；
  - 如果超过该等待时间，Server 将会强制结束所有在处理的请求（客户端会收到错误）。

#### 🔩 配置方式

- WithReadWriteTimeout在初始化 Server 时指定：

  ```go
  import "github.com/cloudwego/kitex/server"
  
  svr := yourservice.NewServer(handler,
      server.WithReadWriteTimeout(5 * time.Second),
  )
  ```

- WithExitWaitTime在初始化 Server 时指定：

  ```go
  import "github.com/cloudwego/kitex/server"
  
  svr := yourservice.NewServer(handler,
      server.WithExitWaitTime(5 * time.Second),
  )
  ```

---

## 🔁 重试（Retry）

kitex目前有四类重试：

- 异常重试：为了提高服务整体的成功率。默认只针对超时错误重试，同时支持用户指定异常或 Resp 重试
- Backup Request：减少服务的延迟波动。在设置时间内未返回，再次发送请求，任意请求结束（成功或失败）则结束。
- Mixed Retry (混合 异常重试 和 Backup Request)：
  - 确认你要请求的接口**具有幂等性**，再开启重试
  - 异常重试 和 备用请求 在一个方法上不能同时启用，如果需要同时启用请使用 Mixed Retry
  - 超时重试会增加延迟
  - 流式接口还不支持重试
- 框架建连失败重试（默认机制）：建连失败是网络层面问题，由于请求未发出，框架会默认重试，一般用户无需关注

### 🔂 异常重试（Failure Retry）

默认只对超时重试，可配置支持指定异常或 Resp 重试

---

## 👁️ 监控与可观测性（Observability）

### 📝 三大支柱：Metrics、Logs、Traces

### 📊 指标收集（Metrics）

Kitex 内置的重要指标包括：
- 请求延迟（Latency）
- 错误率（Error Rate）
- 吞吐量（Throughput）
- 连接数（Connection Count）

```go
package main

import (
	"github.com/cloudwego/kitex/pkg/stats"
)

// 自定义 stats 收集器
type CustomStatsHandler struct {}

func (h *CustomStatsHandler) Start(ctx context.Context, event stats.Event) context.Context {
	// 记录请求开始时间
	return context.WithValue(ctx, "start_time", time.Now())
}

func (h *CustomStatsHandler) Finish(ctx context.Context, event stats.Event) {
	// 计算请求耗时并记录
	if startTime, ok := ctx.Value("start_time").(time.Time); ok {
		duration := time.Since(startTime)
		// 上报到监控系统
		log.Printf("Request took %v", duration)
	}
}

func main() {
	svr := server.NewServer(
		new(UserServiceImpl),
		server.WithStatsHandler(&CustomStatsHandler{}),
	)
	svr.Run()
}
```

### 🕸️ 链路追踪（Distributed Tracing）

使用 Jaeger 进行链路追踪：

```go
package main

import (
	"github.com/cloudwego/kitex/pkg/transmeta"
	"github.com/cloudwego/kitex/pkg/rpcinfo"
)

// Kitex 通过 MetaHandler 支持链路追踪
type TracingMetaHandler struct{}

func (h *TracingMetaHandler) OnConnectHook(ri rpcinfo.RPCInfo) error {
	// 在连接建立时生成或传递 trace ID
	if traceID := getTraceID(); traceID != "" {
		ri.Invocation().SetRPCInfo(rpcinfo.TraceID, traceID)
	}
	return nil
}

func getTraceID() string {
	// 从上下文获取或生成 trace ID
	return "trace-" + generateUUID()
}
```

### 📄 日志输出

```go
package main

import (
	"github.com/cloudwego/kitex/pkg/klog"
)

func main() {
	// 配置日志级别和格式
	klog.SetLevel(klog.LevelInfo)

	// 在业务逻辑中记录关键信息
	klog.Infof("User %s accessed service", userID)
	klog.Warnf("Service latency high: %v", duration)
	klog.Errorf("Service error: %v", err)
}
```

---

## 🏛️ 实践案例

### 🏗️ 完整服务治理示例

构建一个包含完整服务治理功能的用户服务：

```go
package main

import (
	"context"
	"github.com/cloudwego/kitex/client"
	"github.com/cloudwego/kitex/pkg/circuitbreak"
	"github.com/cloudwego/kitex/pkg/loadbalance"
	"github.com/cloudwego/kitex/server"
	etcd "github.com/kitex-contrib/registry-etcd"
	"golang.org/x/time/rate"
	"time"
)

// 创建客户端的最佳实践
func createUserServiceClient() (user.Client, error) {
	// 1. 注册中心
	resolver, err := etcd.NewEtcdResolver(
		[]string{"127.0.0.1:2379"},
	)
	if err != nil {
		return nil, err
	}

	// 2. 熔断器
	cbSuite := circuitbreak.NewCBSuite(
		circuitbreak.DefaultCBConfig(),
	)

	// 3. 负载均衡
	lb := loadbalance.NewRoundRobinBalancer()

	// 4. 创建客户端
	cli, err := user.NewClient(
		"user-service",
		client.WithResolver(resolver),
		client.WithSuite(cbSuite),
		client.WithLoadBalancer(lb),
		client.WithRequestTimeout(time.Second * 3),
	)

	return cli, err
}

// 创建服务端的最佳实践
func createUserService() error {
	// 1. 注册中心
	registry, err := etcd.NewEtcdRegistry(
		[]string{"127.0.0.1:2379"},
	)
	if err != nil {
		return err
	}

	// 2. 限流器
	limiter := rate.NewLimiter(rate.Limit(1000), 100)

	// 3. 创建服务器
	svr := server.NewServer(
		new(UserServiceImpl),
		server.WithRegistry(registry),
		server.WithServiceAddr(rpcinfo.NewNetAddr("tcp", "127.0.0.1:8081")),
		server.WithMiddleware(func(next server.Handler) server.Handler {
			return func(ctx context.Context, req, resp interface{}) error {
				if !limiter.Allow() {
					return fmt.Errorf("rate limit exceeded")
				}
				return next(ctx, req, resp)
			}
		}),
	)

	return svr.Run()
}
```

### ⚠️ 监控告警设置

```go
package main

// 实现服务级别的监控告警
type ServiceMonitor struct {
	errorRate    float64
	latency      time.Duration
	alertHandler func(string, string)
}

func (m *ServiceMonitor) Check() {
	// 检查错误率
	if m.errorRate > 0.05 { // 5% 错误率
		m.alertHandler("error_rate_high", 
			fmt.Sprintf("Error rate: %.2f%%", m.errorRate*100))
	}

	// 检查延迟
	if m.latency > time.Second { // > 1秒
		m.alertHandler("latency_high", 
			fmt.Sprintf("Latency: %v", m.latency))
	}
}
```

---

## 📚 总结

Kitex 提供的完整服务治理能力帮助我们构建稳定可靠的微服务系统：

- **注册发现**：自动管理服务实例，支持多种注册中心
- **负载均衡**：智能分散流量，支持多种策略和自定义扩展
- **熔断降级**：快速隔离故障，防止级联故障
- **限流控制**：保护服务过载，支持分级限流
- **超时重试**：合理控制请求生命周期
- **可观测性**：通过指标、日志、链路追踪全面监控

在生产环境中，正确运用这些功能能显著提升系统的可用性和用户体验。

---

## 📖 参考资源

- [Kitex 官方文档](https://www.cloudwego.io/zh/docs/kitex/)
- [etcd 注册中心集成](https://github.com/kitex-contrib/registry-etcd)
- [Kitex 熔断器设计](https://www.cloudwego.io/zh/docs/kitex/tutorials/service-governance/circuit-breaker/)
- [分布式追踪最佳实践](https://opentelemetry.io/docs/instrumentation/go/)

{{< notice tip >}}
在实际项目中，建议根据业务特点调整服务治理参数。定期监控关键指标，及时发现和处理潜在问题。
{{< /notice >}}
