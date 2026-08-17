---
date : '2026-08-11T14:00:00+08:00'
draft : false
title : 'Eino 的基础组件（一）模型实例'
image : ""
categories : ["Eino框架"]
tags : []
description : "深入探讨 Eino 框架中两个核心组件 ChatModel 和 AgenticModel 的定义、接口设计、使用场景和区别，包含详细的代码示例和最佳实践"
---

## 🎯 写在前面

在开发大模型应用时，我发现 Eino 框架对模型交互做了非常优雅的抽象。最初接触时，看到 `ToolCallingChatModel` 和 `AgenticModel` 两个组件有点懵——它们看起来功能相似，但为什么要分开设计？经过一段时间的实践，我逐渐理解了它们的设计思路和各自的应用场景。

这篇文章会从接口设计讲起，结合实际代码示例，帮你理解这两个组件的本质区别和使用方法。如果你正在用 Eino 做 Agent 开发或者 RAG 应用，相信这篇文章会对你有帮助。

---

## 🏗️ 接口层次设计

### 📐 基础泛型接口

Eino 的设计非常简洁，核心就是一个泛型接口 `BaseModel[M any]`：

```go
type BaseModel[M any] interface {
    Generate(ctx context.Context, input []M, opts ...Option) (M, error)
    Stream(ctx context.Context, input []M, opts ...Option) (*schema.StreamReader[M], error)
}

type BaseChatModel = BaseModel[*schema.Message] // 传统消息模型接口

type ToolCallingChatModel interface { // 推荐工具调用接口
    BaseChatModel
    WithTools(tools []*schema.ToolInfo) (ToolCallingChatModel, error)
}

type ChatModel interface { // 旧版工具调用接口（已废弃）
    BaseChatModel  
    // BindTools 绑定工具到模型，注意：非原子操作，存在并发安全问题
    BindTools(tools []*schema.ToolInfo) error
}

type AgenticModel = BaseModel[*schema.AgenticMessage] // 智能体模型接口
```

这个设计带来的好处非常明显：

**1. 实现可替换**

业务代码只依赖接口，不依赖具体实现。`eino-ext` 提供了 OpenAI、Ark、Claude、Ollama 等多种实现，切换模型只需要改一行构造代码，其他地方完全不用动。

**2. 编排可组合**

Agent、Graph、Chain 等编排层只依赖 Component 接口。你可以把 OpenAI 换成 Ark，编排代码无需改动。这对于多模型切换和 A/B 测试场景特别有用。

**3. 测试可 Mock**

接口天然支持 mock，写单元测试时不需要真实调用模型，可以大大提升测试效率。

---

## 🗂️ 接口继承关系

理解清楚接口的继承关系，有助于我们选择合适的组件：

```
BaseModel[M messageType]              // 泛型基础接口
    ├── BaseChatModel                 // 类型别名（传统消息）
    │   ├── ChatModel                 // 接口（已废弃，有并发安全问题）
    │   └── ToolCallingChatModel      // 接口（推荐，并发安全）
    └── AgenticModel                  // 类型别名（智能体消息）
```

**重点提示**：`ChatModel` 接口已经废弃，新项目请使用 `ToolCallingChatModel`。废弃的原因是 `BindTools` 方法不是原子操作，存在并发安全问题。而 `ToolCallingChatModel` 的 `WithTools` 方法返回新实例，避免了这个问题。

---

## 🧩 实现层结构

具体的实现类型分布在 `eino-ext` 的各个子包中：

```
github.com/cloudwego/eino-ext/components/model/
    ├── openai/
    │   ├── ChatModel (struct)        // ✅ 实现 ToolCallingChatModel
    │   └── AgenticChatModel (struct) // ✅ 实现 AgenticModel
    ├── ark/
    │   ├── ChatModel (struct)        // ✅ 实现 ToolCallingChatModel
    │   └── AgenticChatModel (struct) // ✅ 实现 AgenticModel
    └── qwen/
        └── ChatModel (struct)        // ✅ 实现 ToolCallingChatModel
```

完整的类型关系可以用下图表示：

```
┌─────────────────────────────────────────────────────────────┐
│                     接口层 (Interface)                       │
│                github.com/cloudwego/eino                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BaseModel[M]                                               │
│      ├── BaseChatModel = BaseModel[*schema.Message]         │
│      │   ├── ChatModel (interface, deprecated)              │
│      │   └── ToolCallingChatModel (interface)               │
│      └── AgenticModel = BaseModel[*schema.AgenticMessage]   │
│                                                             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ 实现 (implements)
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                   实现层 (Concrete Types)                    │
│              github.com/cloudwego/eino-ext                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  openai.ChatModel (struct)                                  │
│      └── 实现 ToolCallingChatModel                          │
│                                                             │
│  openai.AgenticChatModel (struct)                           │
│      └── 实现 AgenticModel                                   │
│                                                             │
│  ark.ChatModel (struct)                                     │
│      └── 实现 ToolCallingChatModel                           │
│                                                             │
│  qwen.ChatModel (struct)                                    │
│      └── 实现 ToolCallingChatModel                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💬 ToolCallingChatModel 深入理解

### 🎨 设计理念

在我看来，`ToolCallingChatModel` 就是你的程序和大模型之间的那座桥。不管你后面要做 Agent、RAG 还是复杂的多步骤编排，底层都绕不开它。

Eino 对 ChatModel 的抽象包含了以下核心理念：

- **标准化接口**：无论使用哪个大模型提供商（OpenAI、Anthropic、本地模型等），调用方式完全一致
- **类型安全**：通过 Go 的泛型和强类型系统，提供编译时的类型检查，减少运行时错误
- **灵活配置**：支持温度、最大 token 数、系统提示等常见参数的灵活配置
- **完善的错误处理**：明确的错误类型和处理机制，方便问题排查
- **双模式支持**：同时支持一次性获取完整响应（Generate）和流式获取回复（Stream）

---

### 🔌 接口定义详解

Eino 的 `ToolCallingChatModel` 接口设计得很简洁：

```go
// ChatModel 是与大模型交互的核心接口
type ChatModel interface {
    // Generate 调用模型生成响应（非流式）
    Generate(ctx context.Context, messages []*Message) (*Message, error)
    
    // Stream 调用模型生成响应（流式）
    Stream(ctx context.Context, messages []*Message) (<-chan *Message, error)
}

type ToolCallingChatModel interface {
    BaseChatModel
    WithTools(tools []*schema.ToolInfo) (ToolCallingChatModel, error)
}
```

具体的实现关系为：

```
               [接口层]
         
         BaseModel[*schema.Message]
                    ▲
                    │ 类型别名
            BaseChatModel
                    ▲
         ┌──────────┴──────────┐
         │                     │
    ChatModel          ToolCallingChatModel
   (已废弃)                  (推荐)
         ▲                     ▲
         │                     │
         └─────────┬───────────┘
                   │ 实现
            [具体实现层]
                   │
           openai.ChatModel
           (具体结构体)
```

---

### 📦 Message 结构体

`Message` 是模型交互的核心数据结构：

```go
// Message 代表对话中的一条消息
type Message struct {
    // Role 表示消息的角色（system/user/assistant/tool）
    Role RoleType
    // Content 是消息的文本内容
    Content string
    // UserInputMultiContent 用来存储用户输入的多模态数据
    // 支持文本、图片、音频、视频、文件
    // 使用此字段时限制模型角色为User
    UserInputMultiContent []MessageInputPart
    // AssistantGenMultiContent 用来承接模型输出的多模态数据
    // 支持文本、图片、音频、视频
    // 使用此字段时限制模型角色为Assistant
    AssistantGenMultiContent []MessageOutputPart
    // Name 是消息的发送者名称
    Name string
    // ToolCalls 是 assistant 消息中的工具调用信息
    ToolCalls []ToolCall
    // ToolCallID 是 tool 消息的工具调用 ID
    ToolCallID string
    // ResponseMeta 包含响应的元信息
    ResponseMeta *ResponseMeta
    // Extra 用于存储额外信息
    Extra map[string]any
}
```

Message 结构体的关键特性：

**1. 角色系统**

`Role` 字段标识消息的角色，Eino 定义了四个标准角色：
- `schema.System`：系统提示词
- `schema.User`：用户输入
- `schema.Assistant`：模型回复
- `schema.Tool`：工具执行结果

在实际使用中，正确设置角色非常重要。特别是在多轮对话和 Agent 推理循环中，模型需要通过角色来理解对话的结构。

**2. 多模态支持**

Eino 对多模态内容做了精细的设计：
- `UserInputMultiContent`：用户输入的多模态数据（文本、图片、音频、视频、文件）
- `AssistantGenMultiContent`：模型输出的多模态数据（文本、图片、音频、视频）

这样的设计区分了输入和输出，类型更加清晰。

**3. 工具调用**

`ToolCalls` 字段承载了模型的工具调用请求，`ToolCallID` 则用于工具执行结果的关联。这是实现 Function Calling 的核心字段。

---

### 🛠️ 工具绑定机制

`WithTools` 方法的设计体现了函数式编程的思想：

```go
// ToolCall 表示模型要调用的工具
type ToolCall struct {
    ID       string                 // 工具调用的唯一 ID
    Name     string                 // 工具名称
    Input    map[string]interface{} // 工具输入参数
}
```

`WithTools` 方法接收一组工具描述信息（`[]*schema.ToolInfo`），返回一个**新的** `ToolCallingChatModel` 实例。这里"新的"两个字很关键——`WithTools` 不会修改原来的实例，而是创建一个绑定了工具的副本返回。

这个设计是为了并发安全：在实际项目中，你可能有一个全局的 ChatModel 实例，不同的请求需要绑定不同的工具集。如果 `WithTools` 修改了原实例，并发场景下就会出问题。通过返回新实例，每个请求都有自己独立的工具上下文，完全避免了并发冲突。

---

### ⚙️ 请求级配置选项

组件提供了一组公共 Option 用于灵活配置模型行为：

```go
type Options struct {
    // Temperature 控制输出的随机性（0-2，值越大越随机）
    Temperature *float32
    // Model 指定使用的模型名称
    Model *string
    // TopP 控制输出的多样性
    TopP *float32
    // Tools 定义模型当前可以调用的工具列表
    Tools []*schema.ToolInfo
    // DeferredTools 注册可被模型内置 tool search 延迟加载的工具
    // 不要同时放入Tools
    DeferredTools []*schema.ToolInfo
    // ToolSearchTool 用于搜索/发现 DeferredTools 的工具
    ToolSearchTool *schema.ToolInfo
    // MaxTokens 控制生成的最大 token 数量
    MaxTokens *int
    // Stop 指定停止生成的条件（停止词）
    Stop []string
    
    // Options only available for chat model.
    
    // ToolChoice 模型应该如何选择工具
    ToolChoice *schema.ToolChoice
    // AllowedToolNames 当前请求允许模型调用哪些 Tool
    AllowedToolNames []string
    
    // Options only available for agentic model.
    
    // AgenticToolChoice 控制Agentic Model 如何进行工具调用
    AgenticToolChoice *schema.AgenticToolChoice
}
```

---

### 💡 核心方法详解

**Generate 方法**

```go
Generate(ctx context.Context, input []*schema.Message, opts ...model.Option) (*schema.Message, error)
```

用于生成完整的模型响应，适合对话、问答等需要一次性获取完整结果的场景。

参数说明：
- `ctx`：上下文对象，用于传递请求级别的信息，同时也用于传递 Callback Manager
- `input`：输入消息列表
- `opts`：可选参数，用于配置模型行为

返回值：
- `*schema.Message`：模型生成的响应消息
- `error`：生成过程中的错误信息

**Stream 方法**

```go
Stream(ctx context.Context, input []*schema.Message, opts ...model.Option) (*schema.StreamReader[*schema.Message], error)
```

以流式方式生成模型响应，适合需要实时展示生成过程的场景（如聊天界面）。

参数与 Generate 方法相同。

返回值：
- `*schema.StreamReader[*schema.Message]`：模型响应的流式读取器
- `error`：生成过程中的错误信息

**WithTools 方法**

```go
WithTools(tools []*schema.ToolInfo) (ToolCallingChatModel, error)
```

为模型绑定可用的工具，返回新的 ChatModel 实例（不修改原实例）。

---

## 🧪 实战代码示例

### 🚀 基础调用示例

最简单的使用方式是直接调用 Generate 方法：

```go
package main

import (
    "context"
    "fmt"
    "github.com/cloudwego/eino/flow/chat"
)

func main() {
    // 创建一个 OpenAI ChatModel 实例
    model, err := chat.NewOpenAIChatModel(context.Background(), &chat.OpenAIConfig{
        APIKey: "your-api-key",
        Model:  "gpt-4",
    })
    if err != nil {
        panic(err)
    }

    // 构造对话消息
    messages := []*chat.Message{
        {
            Role:    "user",
            Content: "请解释什么是函数式编程",
        },
    }

    // 调用模型生成响应
    response, err := model.Generate(context.Background(), messages)
    if err != nil {
        panic(err)
    }

    // 输出响应
    fmt.Println("模型回复:", response.Content)
}
```

---

### 🌊 流式调用示例

当需要实时获取模型回复时（比如做聊天界面），流式调用就派上用场了：

```go
package main

import (
    "context"
    "fmt"
    "github.com/cloudwego/eino/flow/chat"
)

func main() {
    model, err := chat.NewOpenAIChatModel(context.Background(), &chat.OpenAIConfig{
        APIKey: "your-api-key",
        Model:  "gpt-4",
    })
    if err != nil {
        panic(err)
    }

    messages := []*chat.Message{
        {
            Role:    "user",
            Content: "写一个关于 Go 语言并发模式的短文",
        },
    }

    // 调用流式方法获取消息通道
    msgChan, err := model.Stream(context.Background(), messages)
    if err != nil {
        panic(err)
    }

    // 迭代处理流式消息
    for msg := range msgChan {
        if msg != nil {
            fmt.Print(msg.Content) // 逐块打印回复内容
        }
    }
    fmt.Println() // 打印换行符
}
```

---

### 🎛️ 参数控制技巧

Eino 的 ToolCallingChatModel 有两个层面的参数控制：

**1. 创建实例时设置默认参数**

```go
cm, err := openai.NewChatModel(ctx, &openai.ChatModelConfig{
    BaseURL:     "https://dashscope.aliyuncs.com/compatible-mode/v1",
    APIKey:      os.Getenv("DASHSCOPE_API_KEY"),
    Model:       "qwen-plus",     // 默认模型
    Temperature: ptr(float32(0.7)), // 默认温度
    MaxTokens:   ptr(2048),        // 默认最大 Token 数
    TopP:        ptr(float32(0.9)), // 默认 Top-P
    Timeout:     30 * time.Second,  // 请求超时时间
})

// 辅助函数，快速创建指针
func ptr[T any](v T) *T { return &v }
```

创建时设置的参数会对这个实例的所有后续调用生效。

**2. 通过 Option 临时覆盖**

有时候同一个 ChatModel 实例在不同场景下需要不同的参数。比如你的 Agent 在分析阶段需要低 Temperature（稳定输出），但在生成最终回答时需要稍高的 Temperature（更自然的表达）：

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "github.com/cloudwego/eino-ext/components/model/openai"
    "github.com/cloudwego/eino/components/model"
    "github.com/cloudwego/eino/schema"
)

func main() {
    ctx := context.Background()

    cm, err := openai.NewChatModel(ctx, &openai.ChatModelConfig{
        BaseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
        APIKey:  os.Getenv("DASHSCOPE_API_KEY"),
        Model:   "qwen-plus",
    })
    if err != nil {
        log.Fatal(err)
    }

    messages := []*schema.Message{
        schema.UserMessage("用一句话描述春天"),
    }

    // 低 Temperature：输出稳定、确定性高
    fmt.Println("Temperature=0（确定性输出）：")
    for i := 0; i < 3; i++ {
        resp, _ := cm.Generate(ctx, messages, model.WithTemperature(0))
        fmt.Printf("  第%d次: %s\n", i+1, resp.Content)
    }

    // 高 Temperature：输出多样、有创意
    fmt.Println("\nTemperature=1.0（多样性输出）：")
    for i := 0; i < 3; i++ {
        resp, _ := cm.Generate(ctx, messages, model.WithTemperature(1.0))
        fmt.Printf("  第%d次: %s\n", i+1, resp.Content)
    }

    // 动态切换模型：用 qwen-turbo 来做轻量快速的任务
    fmt.Println("\n用 qwen-turbo 模型：")
    resp, _ := cm.Generate(ctx, messages, model.WithModel("qwen-turbo"))
    fmt.Printf("  %s\n", resp.Content)
}
```

注意 `model.WithModel("qwen-turbo")` 这个用法——你可以在运行时动态切换模型，不需要创建新的 ChatModel 实例。这在某些场景下非常实用，比如简单的意图分类用 `qwen-turbo`（便宜且快），复杂的推理任务用 `qwen-max`（能力更强但贵一些）。

---

### ⚠️ 使用注意事项

1. **Context 管理**：始终传入有效的 context，用于控制超时和取消操作
2. **错误处理**：Stream 方法的错误可能在消费通道时才发生，需要检查返回的消息是否为 nil
3. **消息历史**：每次调用都需要手动传入完整的对话历史，Eino 不会自动维护状态
4. **Token 成本**：每次调用都会产生 token 消耗，注意成本控制，特别是在循环调用时

---

## 🤖 AgenticModel 深入理解

### 🧠 设计初衷

`AgenticModel` 是 Eino 面向 agentic provider API 的模型组件抽象。它使用 `*schema.AgenticMessage` 作为消息载体，通过有序的 `ContentBlock` 表达文本、reasoning、多模态内容、函数工具调用、服务端内置工具调用、MCP 工具调用和审批结果。

与传统 `ChatModel` 相比，`AgenticModel` 更适合直接承接 OpenAI Responses API、Claude API、Gemini API 等 provider 原生的 agentic 能力：一次模型请求中可能包含多段 reasoning、多次工具调用、服务端工具结果或 MCP 审批信息。Eino 不再把这些内容压平成单一文本字段，而是保留为结构化块。

---

### 📋 核心架构

AgenticModel 的核心架构包括：

```go
// BaseModel is the generic base model interface parameterized by message type M.
type BaseModel[M any] interface {
    Generate(ctx context.Context, input []M, opts ...Option) (M, error)
    Stream(ctx context.Context, input []M, opts ...Option) (*schema.StreamReader[M], error)
}

// AgenticModel is a type alias for BaseModel specialized with
// *schema.AgenticMessage.
type AgenticModel = BaseModel[*schema.AgenticMessage]
```

---

### ⚖️ ToolCallingChatModel vs AgenticModel

两个组件看似相似，但有本质区别：

| 维度       | AgenticModel                                                 | ToolCallingChatModel                                         |
| ---------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 基础接口   | `model.BaseModel[*schema.AgenticMessage]`                    | `model.BaseModel[*schema.Message]`                           |
| 类型别名   | `type AgenticModel = BaseModel[*schema.AgenticMessage]`      | `type BaseChatModel = BaseModel[*schema.Message]`            |
| 消息结构   | `AgenticMessage.ContentBlocks`                               | `Message.Content`、`ToolCalls`、`ToolCallID`等字段           |
| 工具绑定   | 调用时通过`model.WithTools(...)`、`model.WithAgenticToolChoice(...)`传入 | `ToolCallingChatModel.WithTools(...)`或调用时 Option         |
| 表达能力   | reasoning、多模态输入输出、function tool、server tool、MCP tool、approval | 传统 chat completion 消息与 tool call                        |
| 下游执行器 | `compose.AgenticToolsNode`                                   | `compose.ToolsNode`                                          |

{{< notice tip >}}
`AgenticModel` 没有 `WithTools` 方法。`WithTools` 是 `ToolCallingChatModel` 的实例方法；agentic 路径的工具信息通过 `model.WithTools(tools)` 作为请求级 Option 传入。
{{< /notice >}}

---

### 🔌 核心方法

**Generate 方法**

```go
Generate(ctx context.Context, input []*schema.AgenticMessage, opts ...model.Option) (*schema.AgenticMessage, error)
```

用于生成完整的模型响应。

参数说明：
- `ctx`：上下文对象，用于传递请求级别的信息，同时也用于传递 Callback Manager
- `input`：输入消息列表
- `opts`：可选参数，用于配置模型行为

返回值：
- `*schema.AgenticMessage`：模型生成的响应消息
- `error`：生成过程中的错误信息

**Stream 方法**

```go
Stream(ctx context.Context, input []*schema.AgenticMessage, opts ...model.Option) (*schema.StreamReader[*schema.AgenticMessage], error)
```

以流式方式生成模型响应。

参数与 Generate 方法相同。

返回值：
- `*schema.StreamReader[*schema.AgenticMessage]`：模型响应的流式读取器
- `error`：生成过程中的错误信息

---

### 📦 AgenticMessage 结构体

#### 🏛️ 总体结构

```go
type AgenticRoleType string

const (
    AgenticRoleTypeSystem    AgenticRoleType = "system"
    AgenticRoleTypeUser      AgenticRoleType = "user"
    AgenticRoleTypeAssistant AgenticRoleType = "assistant"
)

type AgenticMessage struct {
    Role          AgenticRoleType
    ContentBlocks []*ContentBlock
    ResponseMeta  *AgenticResponseMeta
    Extra         map[string]any
}
```

`AgenticMessage` 只有 `system`、`user`、`assistant` 三类 role。工具调用和工具结果不是独立 role，而是由 `ContentBlock` 表达。

---

#### 📊 ResponseMeta

```go
type AgenticResponseMeta struct {
    TokenUsage      *TokenUsage
    OpenAIExtension *openai.ResponseMetaExtension
    GeminiExtension *gemini.ResponseMetaExtension
    ClaudeExtension *claude.ResponseMetaExtension
    Extension       any
}
```

---

#### 🧱 ContentBlock

`ContentBlock` 是 `AgenticMessage` 的最小内容单元。一个 message 可以包含多个有序 block，用于表达一次响应中的多段 reasoning、文本、多模态输出和工具事件。

```go
type ContentBlock struct {
    Type ContentBlockType

    Reasoning *Reasoning

    UserInputText  *UserInputText
    UserInputImage *UserInputImage
    UserInputAudio *UserInputAudio
    UserInputVideo *UserInputVideo
    UserInputFile  *UserInputFile

    AssistantGenText  *AssistantGenText
    AssistantGenImage *AssistantGenImage
    AssistantGenAudio *AssistantGenAudio
    AssistantGenVideo *AssistantGenVideo

    FunctionToolCall   *FunctionToolCall
    FunctionToolResult *FunctionToolResult

    ToolSearchFunctionToolResult *ToolSearchFunctionToolResult

    ServerToolCall   *ServerToolCall
    ServerToolResult *ServerToolResult

    MCPToolCall             *MCPToolCall
    MCPToolResult           *MCPToolResult
    MCPListToolsResult      *MCPListToolsResult
    MCPToolApprovalRequest  *MCPToolApprovalRequest
    MCPToolApprovalResponse *MCPToolApprovalResponse

    StreamingMeta *StreamingMeta
    Extra         map[string]any
}
```

ContentBlock 支持的内容类型：

| 类型             | 常量                                                   | 对应字段                       | 说明                                           |
| ---------------- | ------------------------------------------------------ | ------------------------------ | ---------------------------------------------- |
| reasoning        | `ContentBlockTypeReasoning`                            | `Reasoning`                    | 模型 reasoning 摘要或原始 reasoning 文本       |
| 用户输入         | `ContentBlockTypeUserInputText/Image/Audio/Video/File` | `UserInput*`                   | 用户侧文本与多模态输入                         |
| 模型输出         | `ContentBlockTypeAssistantGenText/Image/Audio/Video`   | `AssistantGen*`                | 模型生成的文本或多模态内容                     |
| 函数工具调用     | `ContentBlockTypeFunctionToolCall`                     | `FunctionToolCall`             | provider 生成的本地 function tool call         |
| 函数工具结果     | `ContentBlockTypeFunctionToolResult`                   | `FunctionToolResult`           | 用户侧执行 function tool 后返回给模型的结果    |
| tool search 结果 | `ContentBlockTypeToolSearchResult`                     | `ToolSearchFunctionToolResult` | 客户端 tool search 发现并加载的工具定义        |
| 服务端工具       | `ContentBlockTypeServerToolCall/Result`                | `ServerToolCall/Result`        | provider 服务端执行的内置工具，例如 web search |
| MCP 工具         | `ContentBlockTypeMCPToolCall/Result/ListToolsResult`   | `MCP*`                         | provider 侧托管的 MCP 工具调用、结果与工具列表 |
| MCP 审批         | `ContentBlockTypeMCPToolApprovalRequest/Response`      | `MCPToolApproval*`             | MCP 工具执行前的人类审批请求和响应             |

---

## 🎭 应用场景分析

### 💬 ToolCallingChatModel 的应用场景

**1. 简单问答系统**

```go
// 用户问一个问题，模型回答
message := &Message{Role: "user", Content: "Go 的 defer 如何工作？"}
response, _ := chatModel.Generate(ctx, []*Message{message})
```

适合知识问答、技术咨询、客服机器人等场景。

**2. 内容生成**

```go
// 生成文案、文章、代码等
message := &Message{Role: "user", Content: "写一个 Go 的 HTTP 服务器"}
response, _ := chatModel.Generate(ctx, []*Message{message})
```

适合文案创作、代码生成、文档编写等场景。

**3. 翻译和转换**

```go
// 语言翻译、格式转换
message := &Message{Role: "user", Content: "将这段代码转换为 Python"}
response, _ := chatModel.Generate(ctx, []*Message{message})
```

适合多语言翻译、代码转换、格式转换等场景。

**4. 实时流式应用**

```go
// Web UI 实时显示模型输出
msgChan, _ := chatModel.Stream(ctx, messages)
for msg := range msgChan {
    // 将每块文本发送给前端
    SendToWebSocket(msg.Content)
}
```

适合聊天界面、实时问答、在线客服等需要流式输出的场景。

---

### 🤖 AgenticModel 的应用场景

**1. 自动化任务执行**

- 数据爬取和分析
- 报表生成
- 文件处理工作流

**2. 复杂推理任务**

- 问题分解和多步骤求解
- 知识库查询和综合
- 代码审查和优化建议

**3. AI 助手和机器人**

- 客服机器人（调用查询、下单等工具）
- 代码助手（调用代码检查、测试工具）
- 数据分析助手（调用数据查询工具）

**4. 工作流自动化**

- 根据用户请求自动调用一系列 API
- 动态生成执行计划并执行
- 错误恢复和重试逻辑

---

## 📝 总结

通过这篇文章，我们深入了解了 Eino 框架中的两个核心组件：

**ToolCallingChatModel**：适合传统的对话、问答、内容生成场景，接口简洁，易于上手。

**AgenticModel**：适合复杂的 Agent 应用，支持 reasoning、多模态、MCP 工具等高级特性。

选择哪个组件，取决于你的应用场景。如果只是做简单的对话或内容生成，`ToolCallingChatModel` 就足够了。如果要做复杂的 Agent，需要模型具备推理能力、工具调用能力，那 `AgenticModel` 会是更好的选择。

希望这篇文章能帮助你更好地理解和使用 Eino 框架！

---

## 🔗 相关资源

- [Eino 官方文档](https://github.com/cloudwego/eino)
- [Eino 框架概述](../Eino框架概述/)
