---
date : '2026-08-18T08:00:00+08:00'
draft : false
title : 'Eino的基础组件（三）工具定义与使用'
image : ""
categories : ["Eino框架"]
tags : []
description : "掌握 Eino 框架中工具（Tool）的定义、推理和执行机制，深入理解 BaseTool、ToolInfo、InvokableTool、InferTool，以及在 ChatModel 和 ToolsNode 中的实战应用"
---

## ⭐ 写在前面

当我们构建 Agent 或复杂的大模型应用时，经常需要让模型能够使用外部工具。模型可能需要查询天气、访问数据库、调用 API，但模型本身只能理解文本和生成文本——真正的工具执行必须由我们的代码来完成。这就引出了一个关键问题：模型如何知道有哪些工具可用？如何描述工具的功能和参数？模型选择了某个工具后，我们怎样解析它的请求并正确地执行工具？

Eino 对此做了非常清晰的分层设计。工具的定义、参数推理、生命周期管理都被精心组织，让你既能灵活定义各种工具，又能安全地集成到模型调用和 Graph 编排中。这篇文章会从接口设计讲起，结合实战代码，帮你理解整个工具体系——无论你是在做 function calling、RAG 应用还是自主 Agent，这些知识都会派上用场。

---

## 🧠 工具体系的分层

Eino 的工具体系分为三个明确的层次：

**第一层：工具的"身份证"**

`ToolInfo` 是工具的元信息，告诉模型这个工具是什么、做什么、有什么参数。模型看到的就是这个信息——Name、Description、Parameters Schema 等。这一层是**模型侧**，工具本身还没有执行。

**第二层：工具的"能力宣言"**

`BaseTool` 接口定义了工具必须具备的能力。最核心的是 `Info()` 方法，返回 `ToolInfo`，让框架知道这是什么工具。

**第三层：工具的"执行引擎"**

`InvokableTool` 和 `StreamableTool` 定义了工具的实际执行方式。当模型选择使用某个工具时，框架会调用这些接口把参数传进去，工具返回结果。这一层是**本地侧**，执行真实的业务逻辑。

这个分层有个重要意义：**模型只负责选择和描述工具，真正的执行在本地完全由你掌控**。这意味着：

- 参数校验、权限检查、敏感信息隐藏都在本地处理
- 工具执行的超时、重试、幂等性由你决定
- 模型永远不会直接调用你的代码，所有执行都经过你的工具定义

---

## 🏗️ 工具接口体系

### 🔑 BaseTool 接口

所有工具必须实现 `BaseTool` 接口：这个接口定义了"工具长什么样"

```go
// BaseTool is the base interface for tools.
// 
// All tool implementations must embed this interface to be recognized by Eino.
type BaseTool interface {
	// Info returns the metadata of this tool, telling the model what this tool can do.
	// The returned ToolInfo must be immutable — subsequent calls should return 
	// the same value.
	//
	// Info is called by the framework to gather tool metadata for:
	// 1. Model invocation — the model sees this to decide when to use the tool
	// 2. Tool selection — the framework uses Name to route to the correct tool
	// 3. Schema validation — used to validate and parse tool parameters
	Info(ctx context.Context) (*schema.ToolInfo, error)
}
```

关键点：

- **Info() 返回 ToolInfo**：这个方法极其关键。框架会调用它来了解工具的元信息。为了性能，通常应该缓存结果而不是每次都重新计算。模型根据这些元信息来判断什么时候该调用哪个工具。
- **Info 是不可变的**：一旦工具创建，它的 ToolInfo 不应该改变。这保证了整个流程的可预测性。

### 📖 ToolInfo 结构

`ToolInfo` 是工具的身份证，告诉模型这个工具是什么、有什么参数。当前 Eino 将参数模式封装在 `ParamsOneOf` 中，通常使用 `schema.NewParamsOneOfByJSONSchema` 创建：

```go
type ToolInfo struct {
    // 工具的唯一名称，用于清晰地表达其用途
    Name string
    // 用于告诉模型如何/何时/为什么使用这个工具
    // 可以在描述中包含少量示例
    Desc string
    // 工具接受的参数定义
    // 可以通过两种方式描述：
    // 1. 使用 ParameterInfo：schema.NewParamsOneOfByParams(params)
    // 2. 使用 OpenAPIV3：schema.NewParamsOneOfByOpenAPIV3(openAPIV3)
    *ParamsOneOf
}

info := &schema.ToolInfo{
	Name: "get_weather",
	Desc: "Get current weather for a location",
	ParamsOneOf: schema.NewParamsOneOfByJSONSchema(weatherParamsSchema),
}
```

上面的 `weatherParamsSchema` 是一个 JSON Schema。实际代码中应按所使用的 `eino-contrib/jsonschema` 版本构造它；不要把 `ParamsOneOf` 直接写成 `[]*jsonschema.Schema`。核心三个字段的含义：

- **Name**：工具的唯一标识符。模型会输出这个名字，框架据此找到对应的工具实现。约定用 `snake_case`，比如 `get_weather`、`query_order`。

- **Desc**：对工具功能的自然语言描述。模型会读这个描述来决定是否需要使用这个工具。好的描述应该包含工具的主要功能、输入输出等，比如："Get current weather and forecast for a location in temperature unit (C or F)"。

- **ParamsOneOf**：参数模式的封装对象，描述工具接受的 JSON 参数结构。通常使用 `schema.NewParamsOneOfByJSONSchema` 从 JSON Schema 构造；需要支持多种调用方式时，可以在这个封装对象中表达多个参数模式。

在大模型的 function call 调用过程中，由大模型生成需要调用的 function call 的参数，这就要求大模型能理解生成的参数是否符合约束。在 Eino 中，根据开发者的使用习惯和领域标准两方面因素，提供了 `params map[string]*ParameterInfo` 和 `*jsonschema.Schema` 两种参数约束的表达方式。

**方式 1 - map[string]\*ParameterInfo**

在很多开发者的直观习惯中，对于参数的描述方式可以用一个 map 来表示，key 即为参数名，value 则是这个参数的详细约束。Eino 中定义了 ParameterInfo 来表示一个参数的描述，如下：

```go
// 结构定义详见: https://github.com/cloudwego/eino/blob/main/schema/tool.go
type ParameterInfo struct {
    Type DataType    // The type of the parameter.
    ElemInfo *ParameterInfo    // The element type of the parameter, only for array.
    SubParams map[string]*ParameterInfo    // The sub parameters of the parameter, only for object.
    Desc string    // The description of the parameter.
    Enum []string    // The enum values of the parameter, only for string.
    Required bool    // Whether the parameter is required.
}
```

比如，一个表示 User 的参数可以表示为：

```go
map[string]*schema.ParameterInfo{
    "name": &schema.ParameterInfo{
        Type: schema.String,
        Required: true,
    },
    "age": &schema.ParameterInfo{
        Type: schema.Integer,
    },
    "gender": &schema.ParameterInfo{
        Type: schema.String,   
        Enum: []string{"male", "female"},
    },
}
```

**方式 2 - JSON Schema**

另一种常用于表示参数约束的方式是 JSON Schema（[https://json-schema.org/draft/2020-12](https://json-schema.org/draft/2020-12)）。

JSON Schema 的标准中对参数的约束方式非常丰富。在实际的使用中，一般不由开发者自行构建此结构体，而是使用一些方法来生成。

Eino 提供了在结构体中通过 go tag 描述参数约束的方式，并提供了 GoStruct2ParamsOneOf 方法来生成一个 struct 的参数约束，其函数签名如下：

```go
func GoStruct2ParamsOneOf[T any](opts ...Option) (*schema.ParamsOneOf, error)
```

其中从 T 中提取参数的字段名称和描述，提取时所用的 Tag 如下：

- `jsonschema_description:"xxx"`[推荐] 或者`jsonschema:"description=xxx"`
  - description 中一般会有逗号，且 tag 中逗号是不同字段的分隔符，且不可被转义，强烈推荐使用 jsonschema_description 这个单独的 Tag 标签
- `jsonschema:"enum=xxx,enum=yyy,enum=zzz"`
- `jsonschema:"required"`
- `json:"xxx,omitempty"` => 可用 json tag 的 omitempty 代表非 required

```go
package main

import (
    "context"
    "github.com/cloudwego/eino/components/tool/utils"
)

type User struct {
    Name   string `json:"name" jsonschema_description:"the name of the user" jsonschema:"required"`
    Age    int    `json:"age" jsonschema_description:"the age of the user"`
    Gender string `json:"gender" jsonschema:"enum=male,enum=female"`
}

func main() {
    params, err := utils.GoStruct2ParamsOneOf[User]()
}
```

### 🔨 标准工具接口

标准工具接口返回字符串类型的结果：

```go
// InvokableTool represents a tool that can be invoked with JSON parameters.
//
// InvokableRun receives the arguments as a JSON string and must:
// 1. Parse the JSON according to your tool's expected structure
// 2. Validate the parameters
// 3. Execute the business logic
// 4. Return the result as a string
//
// The framework does NOT validate JSON against the schema — your tool must do it.
type InvokableTool interface {
	BaseTool
	
	// InvokableRun executes the tool with the given JSON-encoded arguments.
	//
	// Parameters:
	//   ctx: context for cancellation, timeout, and tracing
	//   argumentsInJSON: JSON string containing tool parameters
	//   opts: optional framework directives (rarely used)
	//
	// Returns:
	//   string: the tool's result (typically JSON or plain text)
	//   error: if execution fails (invalid JSON, missing params, business logic error, etc.)
	//
	// Important: Errors in InvokableRun will be caught by the framework and 
	// returned to the model, giving the model a chance to retry.
	InvokableRun(ctx context.Context, argumentsInJSON string, opts ...Option) (string, error)
}

// StreamableTool represents a tool that can return streaming results.
//
// StreamableRun is similar to InvokableRun but returns a StreamReader
// that yields chunks of data over time. Useful for long-running operations
// like database queries, file processing, or paginated API calls.
type StreamableTool interface {
	BaseTool
	StreamableRun(ctx context.Context, argumentsInJSON string, opts ...Option) (*schema.StreamReader[string], error)
}
```

注意几个重要点：

- **参数是 JSON 字符串**：模型输出 `{"location": "Beijing", "unit": "C"}` 这样的 JSON，你的工具需要解析它。
- **框架不做参数验证**：JSON 是否符合 Schema，参数是否完整——这些检查必须由你的工具负责。如果参数不对，返回 error。
- **结果是字符串**：通常是 JSON 序列化后的结果，或者纯文本。模型会读这个字符串作为工具的返回值。
- **Error 会反馈给模型**：如果你的工具返回 error，框架会把错误消息发给模型，模型可能会重新调用或使用其他工具。

#### ⚡ 增强型工具接口（Enhanced Tool）

增强型工具接口支持返回结构化的多模态结果（`*schema.ToolResult`），可以包含文本、图片、音频、视频和文件等多种类型的内容：

```go
// EnhancedInvokableTool 是支持返回结构化多模态结果的工具接口
// 与返回字符串的 InvokableTool 不同，此接口返回 *schema.ToolResult
// 可以包含文本、图片、音频、视频和文件
type EnhancedInvokableTool interface {
    BaseTool
    InvokableRun(ctx context.Context, toolArgument *schema.ToolArgument, opts ...Option) (*schema.ToolResult, error)
}

// EnhancedStreamableTool 是支持返回结构化多模态结果的流式工具接口
// 提供流式读取器以逐步访问多模态内容
type EnhancedStreamableTool interface {
    BaseTool
    StreamableRun(ctx context.Context, toolArgument *schema.ToolArgument, opts ...Option) (*schema.StreamReader[*schema.ToolResult], error)
}
```

相关的数据结构如下

```go
// ToolArgument 包含工具调用的输入信息
type ToolArgument struct {
    // TextArgument 包含 JSON 格式的工具调用参数
    TextArgument string
}

// ToolResult 表示工具执行的结构化多模态输出
// 当工具需要返回不仅仅是简单字符串时使用，
// 例如图片、文件或其他结构化数据
type ToolResult struct {
    // Parts 包含多模态输出部分。每个部分可以是不同类型的内容，
    // 如文本、图片或文件
    Parts []ToolOutputPart `json:"parts,omitempty"`
}

// ToolPartType 定义工具输出部分的内容类型
type ToolPartType string

const (
    ToolPartTypeText  ToolPartType = "text"   // 文本
    ToolPartTypeImage ToolPartType = "image"  // 图片
    ToolPartTypeAudio ToolPartType = "audio"  // 音频
    ToolPartTypeVideo ToolPartType = "video"  // 视频
    ToolPartTypeFile  ToolPartType = "file"   // 文件
)

// ToolOutputPart 表示工具执行输出的一部分
type ToolOutputPart struct {
    Type  ToolPartType     `json:"type"`            // 内容类型
    Text  string           `json:"text,omitempty"`  // 文本内容
    Image *ToolOutputImage `json:"image,omitempty"` // 图片内容
    Audio *ToolOutputAudio `json:"audio,omitempty"` // 音频内容
    Video *ToolOutputVideo `json:"video,omitempty"` // 视频内容
    File  *ToolOutputFile  `json:"file,omitempty"`  // 文件内容
    Extra map[string]any   `json:"extra,omitempty"` // 扩展信息
}

// 多媒体内容结构体，都包含 URL 或 Base64 数据以及 MIME 类型信息
type ToolOutputImage struct { MessagePartCommon }
type ToolOutputAudio struct { MessagePartCommon }
type ToolOutputVideo struct { MessagePartCommon }
type ToolOutputFile  struct { MessagePartCommon }
```

---

## 🔧 InferTool 与 NewTool：工具的两种创建方式

Eino 提供两种方式来创建工具，分别针对不同的使用场景：

- **InferTool**：从一个 Go 函数的签名**自动推断**参数 Schema 和执行逻辑。非常方便，但需要遵循特定的函数签名约束。

- **NewTool**：手工构造 `ToolInfo` 和执行函数，给你最大的灵活性。

两者都在 `github.com/cloudwego/eino/components/tool/utils` 包中。

### ⚙️ NewTool：手工构造工具

当一个函数满足下面这种函数签名时，就可以用 NewTool 把其变成一个 InvokableTool：

```go
type InvokeFunc[T, D any] func(ctx context.Context, input T) (output D, err error)
```

NewTool 的方法如下：

```go
// 代码见: github.com/cloudwego/eino/components/tool/utils/invokable_func.go
func NewTool[T, D any](desc *schema.ToolInfo, i InvokeFunc[T, D], opts ...Option) tool.InvokableTool
```

同理 NewStreamTool 可创建 StreamableTool。

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"

    "github.com/cloudwego/eino/components/tool/utils"
    "github.com/cloudwego/eino/schema"
)

// 工具的入参结构体
type WeatherRequest struct {
    City string `json:"city"`
}

// 工具的返回结构体
type WeatherResponse struct {
    City    string `json:"city"`
    Temp    string `json:"temp"`
    Weather string `json:"weather"`
}

// 工具的实际执行逻辑
func getWeather(ctx context.Context, req *WeatherRequest) (*WeatherResponse, error) {
    // 这里用硬编码模拟，实际项目中你会去调天气 API
    mockData := map[string]WeatherResponse{
       "北京": {City: "北京", Temp: "22°C", Weather: "晴"},
       "上海": {City: "上海", Temp: "26°C", Weather: "多云"},
       "深圳": {City: "深圳", Temp: "30°C", Weather: "阵雨"},
    }

    if data, ok := mockData[req.City]; ok {
       return &data, nil
    }
    return &WeatherResponse{City: req.City, Temp: "未知", Weather: "未知"}, nil
}

func main() {
    ctx := context.Background()

    // 用 NewTool 创建 InvokableTool
    weatherTool := utils.NewTool(
       &schema.ToolInfo{
          Name: "get_weather",
          Desc: "查询指定城市的实时天气信息，包括温度和天气状况",
          ParamsOneOf: schema.NewParamsOneOfByParams(map[string]*schema.ParameterInfo{
             "city": {
                Type:     schema.String,
                Desc:     "要查询天气的城市名称，如：北京、上海、深圳",
                Required: true,
             },
          }),
       },
       getWeather,
    )

    // 验证工具信息
    info, _ := weatherTool.Info(ctx)
    fmt.Printf("工具名: %s\n", info.Name)
    fmt.Printf("工具描述: %s\n", info.Desc)

    // 模拟模型生成的工具调用参数（JSON 字符串）
    args := `{"city": "北京"}`

    // 执行工具
    result, err := weatherTool.InvokableRun(ctx, args)
    if err != nil {
       log.Fatal(err)
    }

    fmt.Printf("执行结果: %s\n", result)

    // 解析结果
    var resp WeatherResponse
    json.Unmarshal([]byte(result), &resp)
    fmt.Printf("城市: %s, 温度: %s, 天气: %s\n", resp.City, resp.Temp, resp.Weather)
}
```

### 🧪 InferTool：自动推断工具

从 NewTool 中可以看出，构建一个 tool 的过程需要分别传入 ToolInfo 和 InvokeFunc，其中，ToolInfo 中包含 ParamsOneOf 的部分，这代表着函数的入参约束，同时，InvokeFunc 的函数签名中也有 input 的参数，这就意味着：ParamsOneOf 的部分和 InvokeFunc 的 input 参数需要保持一致。

当一个函数完全由开发者自行实现的时候，就需要开发者手动维护 input 参数和 ParamsOneOf 以保持一致。更优雅的解决方法是 “参数约束直接维护在 input 参数类型定义中”，可参考上方 GoStruct2ParamsOneOf 的介绍。

当参数约束信息包含在 input 参数类型定义中时，就可以使用 InferTool 来实现，函数签名如下：

```go
func InferTool[T, D any](toolName, toolDesc string, i InvokeFunc[T, D], opts ...Option) (tool.InvokableTool, error)
```

```go
import (
    "github.com/cloudwego/eino/components/tool"
    "github.com/cloudwego/eino/components/tool/utils"
    "github.com/cloudwego/eino/schema"
)

type User struct {
    Name   string `json:"name" jsonschema:"required,description=the name of the user"`
    Age    int    `json:"age" jsonschema:"description=the age of the user"`
    Gender string `json:"gender" jsonschema:"enum=male,enum=female"`
}

type Result struct {
    Msg string `json:"msg"`
}

func AddUser(ctx context.Context, user *User) (*Result, error) {
    // some logic
}

func createTool() (tool.InvokableTool, error) {
    return utils.InferTool("add_user", "add user", AddUser)
}
```

**InferTool 的优势**：

1. **类型安全**：参数和返回值都有类型检查，避免了 JSON 解析的错误
2. **自动 Schema 生成**：框架从结构体的字段和标签自动生成 JSON Schema
3. **代码简洁**：不需要手写参数验证和 JSON 序列化
4. **错误处理清晰**：Go 的 error 返回机制自然支持

**InferTool 的约束**：

函数必须符合以下签名：
```go
func(ctx context.Context, params T) (D, error)
```

- 第一个参数必须是 `context.Context`
- 第二个参数的类型必须与 `InferTool` 的第一个类型参数 `T` 完全一致；常见写法是使用参数结构体指针
- 返回值为两个：返回数据和 error
- 参数结构体的字段名 **必须是 public 的**（大写开头）

### 🆚 InferTool vs NewTool 选择标准

| 场景 | 推荐 | 理由 |
|------|------|------|
| 参数和返回值有明确的结构体 | InferTool | 代码简洁，类型安全 |
| 参数可选或灵活 | NewTool | InferTool 无法灵活处理 |
| 需要自定义参数校验逻辑 | NewTool | 可以在执行函数中自定义 |
| 需要多种调用方式（ParamsOneOf 多个 Schema） | NewTool | InferTool 只生成一个 Schema |
| 快速原型、Demo | InferTool | 效率高 |

---

## 📋 关键方法

- **Info 方法**

  - 功能：获取工具的描述信息

  - 参数：
    - ctx：上下文对象

  - 返回值：
    - `*schema.ToolInfo`：工具的描述信息
    - error：获取信息过程中的错误

- **InvokableRun 方法（标准工具）**

  - 功能：同步执行工具

  - 参数：
    - ctx：上下文对象，用于传递请求级别的信息，同时也用于传递 Callback Manager
    - `argumentsInJSON`：JSON 格式的参数字符串
    - opts：工具执行的选项

  - 返回值：
    - string：执行结果
    - error：执行过程中的错误

- **InvokableRun 方法（增强型工具）**

  - 功能：同步执行工具，返回多模态结果

  - 参数：
    - ctx：上下文对象
    - `toolArgument`：包含 JSON 格式参数的 `*schema.ToolArgument`
    - opts：工具执行的选项

  - 返回值：
    - `*schema.ToolResult`：包含多模态内容的执行结果
    - error：执行过程中的错误

- **StreamableRun 方法（标准工具）**

  - 功能：以流式方式执行工具

  - 参数：
    - ctx：上下文对象
    - `argumentsInJSON`：JSON 格式的参数字符串
    - opts：工具执行的选项

  - 返回值：
    - `*schema.StreamReader[string]`：流式执行结果
    - error：执行过程中的错误

- **StreamableRun 方法（增强型工具）**

  - 功能：以流式方式执行工具，返回多模态结果流

  - 参数：
    - ctx：上下文对象
    - `toolArgument`：包含 JSON 格式参数的 `*schema.ToolArgument`
    - opts：工具执行的选项

  - 返回值：
    - `*schema.StreamReader[*schema.ToolResult]`：流式多模态执行结果
    - error：执行过程中的错误

---

## ♻️ 工具执行的生命周期

### 🔄 从模型输出到工具执行

整个流程是这样的：

1. **模型选择工具**：模型读了你提供的 `ToolInfo` 列表，决定要使用 `get_weather` 工具
2. **模型生成工具调用**：模型输出类似 `{"name": "get_weather", "arguments": "{\"location\": \"Beijing\", \"unit\": \"C\"}"}`
3. **框架解析和路由**：框架从输出中提取工具名和参数，根据名字找到对应的 `InvokableTool` 实现
4. **工具执行**：调用 `InvokableTool.InvokableRun(ctx, argumentsInJSON)`，工具：
   - 解析 JSON 参数
   - 验证参数完整性和有效性
   - 执行业务逻辑
   - 返回结果（成功或错误）
5. **结果反馈给模型**：框架把工具的输出重新发给模型，模型可以：
   - 理解工具的输出，生成最终回复
   - 发现工具调用失败，选择重试或其他工具
   - 继续链式调用其他工具

### 🎯 关键的生命周期回调

当 InvokableTool 执行时，框架支持通过 Context 的回调机制追踪执行过程：

- **执行前**：框架可以通过 Context 记录日志、进行权限检查、启动性能追踪
- **执行中**：工具的实际执行发生在 `InvokableRun` 调用中
- **执行后**：框架可以记录结果、更新指标、进行敏感信息脱敏

这些机制对于：
- **生产环境的可观测性**：追踪每个工具调用的输入、输出、耗时
- **权限和安全检查**：在工具执行前检查是否有权限调用
- **敏感信息隐藏**：在工具完成后对结果进行脱敏，防止敏感信息被模型看到
- **监控和告警**：检测工具调用的异常模式

---

## 🛠️ 与 ChatModel 绑定工具

### 🧩 模型侧 vs 本地侧

这是 Eino 工具设计中最容易误解的地方。必须清楚：**模型永远不会直接执行工具**。

**模型侧（Model-Side）**：
- 模型看到 ToolInfo 列表
- 模型根据用户问题**决定**是否使用某个工具，以及用什么参数
- 模型输出 tool calling 格式的响应（工具名 + 参数）
- 模型**不执行**工具代码

**本地侧（Local-Side）**：
- 你的代码接收模型的 tool calling 输出
- 你的代码**真正执行**工具的 InvokableRun
- 你的代码负责所有的参数校验、权限检查、超时、重试
- 你的代码把工具结果反馈给模型（可能模型继续调用其他工具）

### 🔐 WithTools：绑定工具到模型

```go
import (
	"context"
	"github.com/cloudwego/eino-ext/components/model/openai"
	"github.com/cloudwego/eino/components/tool/utils"
	"github.com/cloudwego/eino/schema"
)

// 创建模型实例
model, err := openai.NewChatModel(ctx, &openai.ChatModelConfig{
	APIKey: os.Getenv("OPENAI_API_KEY"),
	Model:  "gpt-4-turbo",
})
if err != nil {
	log.Fatal(err)
}

// 创建工具
weatherTool, err := utils.InferTool[*GetWeatherRequest, *GetWeatherResponse](
	"get_weather",
	"Get weather for a location",
	GetWeatherImpl,
)

// 🎯 关键步骤：用 WithTools 把工具绑定到模型
// 注意：WithTools 返回一个新的模型实例，不修改原始模型
toolInfo, err := weatherTool.Info(ctx)
if err != nil {
	log.Fatal(err)
}
modelWithTools, err := model.WithTools([]*schema.ToolInfo{toolInfo})
if err != nil {
	log.Fatal(err)
}

// 现在 modelWithTools 知道有 weather 工具可用
// 当你用 modelWithTools 调用模型时，如果模型决定用工具，它会返回 tool calling 格式
```

### 🔁 Tool Calling 循环

典型的工具调用循环是这样的：

```go
// 用户的问题
messages := []*schema.Message{
	schema.UserMessage("北京现在天气如何？"),
}

// 第一轮：问模型
resp, err := modelWithTools.Generate(ctx, messages)
if err != nil {
	log.Fatal(err)
}

// 模型返回了什么？
if len(resp.ToolCalls) > 0 {
	// ✅ 模型决定使用工具
	for _, toolCall := range resp.ToolCalls {
		// 模型输出了：{"name": "get_weather", "arguments": "{\"location\": \"Beijing\", \"unit\": \"C\"}"}
		
		// 找到对应的工具并执行
		result, err := weatherTool.InvokableRun(ctx, toolCall.Arguments)
		if err != nil {
			// ❌ 工具执行失败
			// 把失败消息加入对话，让模型知道
			messages = append(messages, &schema.Message{
				Role:    schema.Assistant,
				Content: resp.Content, // 模型的原始输出
			})
			messages = append(messages, &schema.Message{
				Role:    schema.Tool,
				Content: fmt.Sprintf("Tool call failed: %v", err),
				ToolCallID: toolCall.ID,
			})
		} else {
			// ✅ 工具执行成功
			messages = append(messages, &schema.Message{
				Role:    schema.Assistant,
				Content: resp.Content,
			})
			messages = append(messages, &schema.Message{
				Role:    schema.Tool,
				Content: result, // 工具的输出
				ToolCallID: toolCall.ID,
			})
		}
	}

	// 第二轮：把工具结果反馈给模型，让模型继续
	resp, err = modelWithTools.Generate(ctx, messages)
	if err != nil {
		log.Fatal(err)
	}
	
	// 继续检查模型是否还要调用工具...
	// 通常需要一个循环来处理多轮的工具调用
} else {
	// ✅ 模型直接回答了，不需要工具
	fmt.Println("模型回复:", resp.Content)
}
```

完整的工具循环框架通常被集成到 `compose.ToolsNode` 中，下一节会详细讲。

---

## 📦 ToolsNode：在编排中使用工具

### 🏛️ 什么是 ToolsNode

`ToolsNode` 是 Eino 的编排层组件，它负责：

1. **执行当前输入中的工具调用**：读取消息中的 ToolCalls 并调用对应工具
2. **并发工具执行**：可以同时执行多个工具调用
3. **错误处理**：根据配置决定工具失败后的行为
4. **与 Graph 集成**：作为 Graph 的一个节点

`ToolsNode` 负责当前节点中的工具执行，不等于自动完成完整的“模型调用 -> 工具执行 -> 再次调用模型”循环。完整循环通常需要通过 Graph 或代码显式编排。

### 🎛️ ToolsNodeConfig

```go
import (
	"github.com/cloudwego/eino/compose"
	"github.com/cloudwego/eino/components/tool"
)

type ToolsNodeConfig struct {
	// Tools 是可用的工具列表
	// ToolsNode 会把这些工具提供给模型
	Tools []tool.BaseTool

	// MaxConcurrency 是并发执行工具的最大数量
	// 如果设置为 1，工具会顺序执行
	// 如果设置为 0 或负数，表示无限并发（一次同时执行所有工具调用）
	// 默认值取决于实现，通常是合理的值如 4 或 8
	MaxConcurrency int

	// ContinueOnError 决定当一个工具失败时是否继续执行其他工具
	// 如果为 true：其他工具会继续执行，失败的工具只是把错误反馈给模型
	// 如果为 false：任何工具失败都会中断整个 ToolsNode 的执行
	ContinueOnError bool

	// ParallelRun 决定是否让所有工具同时发起调用
	// 如果为 true，框架会同时调用所有工具（受 MaxConcurrency 限制）
	// 如果为 false，工具会按某种顺序依次调用（默认行为）
	ParallelRun bool
}
```

**MaxConcurrency 的选择**：

- **MaxConcurrency = 1**：适合工具之间有依赖关系，或者某些工具的并发调用有限制（如 API 限流）
- **MaxConcurrency = 4-8**：通常的默认选择，平衡吞吐量和资源使用
- **MaxConcurrency = 0**：谨慎使用，可能导致资源爆炸

**ContinueOnError 的选择**：

- **ContinueOnError = true**：一个工具查询失败不影响其他工具，适合工具之间独立的场景（如查天气同时查空气质量）
- **ContinueOnError = false**：适合工具有依赖关系，一个失败后整个流程无法继续

---

## 🎬 完整实战：天气查询 Agent

### 🎨 场景说明

构建一个 Agent，能够：
1. 接收用户问题（如"北京今天天气怎样？")
2. 调用 `get_weather` 工具查询天气
3. 基于工具返回的数据生成回复

### 💾 完整代码示例

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/cloudwego/eino-ext/components/model/openai"
	"github.com/cloudwego/eino/components/tool/utils"
	"github.com/cloudwego/eino/schema"
)

// 工具参数结构
type GetWeatherRequest struct {
	Location string `json:"location" description:"City or region name"`
	Unit     string `json:"unit" description:"Temperature unit: C or F"`
}

// 工具返回结构
type GetWeatherResponse struct {
	Location    string  `json:"location"`
	Temperature float64 `json:"temperature"`
	Condition   string  `json:"condition"`
	Unit        string  `json:"unit"`
}

// 工具的实现
func GetWeatherImpl(ctx context.Context, req *GetWeatherRequest) (*GetWeatherResponse, error) {
	if req.Location == "" {
		return nil, fmt.Errorf("location is required")
	}

	// 模拟天气数据库
	weatherData := map[string]float64{
		"Beijing":    18.0,
		"Shanghai":   25.0,
		"Guangzhou":  28.0,
	}

	temp, ok := weatherData[req.Location]
	if !ok {
		return nil, fmt.Errorf("location not found: %s", req.Location)
	}

	if req.Unit == "F" {
		temp = temp*9.0/5.0 + 32.0
	}

	return &GetWeatherResponse{
		Location:    req.Location,
		Temperature: temp,
		Condition:   "Partly Cloudy",
		Unit:        req.Unit,
	}, nil
}

func main() {
	ctx := context.Background()

	// 1️⃣ 创建模型
	model, err := openai.NewChatModel(ctx, &openai.ChatModelConfig{
		APIKey: os.Getenv("OPENAI_API_KEY"),
		Model:  "gpt-4-turbo",
	})
	if err != nil {
		log.Fatal(err)
	}

	// 2️⃣ 创建工具
	weatherTool, err := utils.InferTool[*GetWeatherRequest, *GetWeatherResponse](
		"get_weather",
		"Get current weather for a given location in temperature unit (C or F)",
		GetWeatherImpl,
	)
	if err != nil {
		log.Fatal(err)
	}

	// 3️⃣ 绑定工具到模型
	toolInfo, err := weatherTool.Info(ctx)
	if err != nil {
		log.Fatal(err)
	}
	modelWithTools, err := model.WithTools([]*schema.ToolInfo{toolInfo})
	if err != nil {
		log.Fatal(err)
	}

	// 4️⃣ 工具调用循环
	messages := []*schema.Message{
		schema.UserMessage("北京和上海现在各是什么天气？用摄氏度表示"),
	}

	maxIterations := 5 // 防止死循环
	for i := 0; i < maxIterations; i++ {
		fmt.Printf("\n=== 第 %d 轮 ===\n", i+1)

		// 调用模型
		resp, err := modelWithTools.Generate(ctx, messages)
		if err != nil {
			log.Fatal(err)
		}

		// 检查模型是否使用了工具
		if len(resp.ToolCalls) == 0 {
			// ✅ 模型给出了最终回复
			fmt.Println("模型回复:", resp.Content)
			break
		}

		// ⚙️ 执行工具调用
		fmt.Printf("模型选择使用工具: %d 个\n", len(resp.ToolCalls))

		// 添加模型的输出到消息历史
		assistantMsg := &schema.Message{
			Role:      schema.Assistant,
			Content:   resp.Content,
			ToolCalls: resp.ToolCalls,
		}
		messages = append(messages, assistantMsg)

		// 执行每个工具调用
		for _, tc := range resp.ToolCalls {
			fmt.Printf("  - 工具: %s, 参数: %s\n", tc.Name, tc.Arguments)

			// 解析参数并执行工具
			result, err := weatherTool.InvokableRun(ctx, tc.Arguments)
			if err != nil {
				fmt.Printf("    ❌ 执行失败: %v\n", err)
				// 把错误反馈给模型
				messages = append(messages, &schema.Message{
					Role:       schema.Tool,
					Content:    fmt.Sprintf("Error: %v", err),
					ToolCallID: tc.ID,
				})
			} else {
				fmt.Printf("    ✅ 结果: %s\n", result)
				// 把结果反馈给模型
				messages = append(messages, &schema.Message{
					Role:       schema.Tool,
					Content:    result,
					ToolCallID: tc.ID,
				})
			}
		}
	}
}
```

### 🔍 代码要点解析

**第一步：创建工具**

```go
weatherTool, err := utils.InferTool[*GetWeatherRequest, *GetWeatherResponse](
    "get_weather",
    "Get current weather for a given location in temperature unit (C or F)",
    GetWeatherImpl,
)
```

InferTool 自动生成了 ToolInfo（包括参数 Schema）。从 GetWeatherRequest 的结构和标签，框架推断出该工具接受 `location` 和 `unit` 两个参数。

**第二步：绑定到模型**

```go
toolInfo, err := weatherTool.Info(ctx)
modelWithTools, err := model.WithTools([]*schema.ToolInfo{toolInfo})
```

通过 `WithTools` 告诉模型有哪些工具可用。重点是 `toolInfo.Name` 应该是工具的唯一标识，模型会用这个名字选择工具。

**第三步：工具循环**

```go
if len(resp.ToolCalls) == 0 {
    // 模型没有调用工具，直接回复
} else {
    // 模型调用了工具，执行并反馈结果
}
```

这个循环持续到模型不再调用工具为止。每一轮：
1. 用 `modelWithTools.Generate` 调用模型
2. 检查模型的输出中是否有 `ToolCalls`
3. 如果有，逐个执行工具并把结果加回消息列表
4. 继续下一轮

---

## 🚨 常见陷阱与最佳实践

### 🛑 陷阱 1：参数验证遗漏

**问题**：

```go
// ❌ 错误做法
func BadWeatherImpl(ctx context.Context, req *GetWeatherRequest) (*GetWeatherResponse, error) {
	// 没有检查 req 是否为 nil 或字段是否为空
	temp := fetchTemperature(req.Location) // panic if req is nil
	return &GetWeatherResponse{Temperature: temp}, nil
}
```

**正确做法**：

```go
// ✅ 正确做法
func GoodWeatherImpl(ctx context.Context, req *GetWeatherRequest) (*GetWeatherResponse, error) {
	if req == nil {
		return nil, fmt.Errorf("request is nil")
	}
	if req.Location == "" {
		return nil, fmt.Errorf("location is required")
	}
	// ... 继续执行
}
```

**为什么重要**：模型可能不按预期提供参数。参数验证是工具的第一道防线。

### 🚫 陷阱 2：超时和上下文忽视

**问题**：

```go
// ❌ 错误做法：无视 context 超时
func SlowWeatherImpl(ctx context.Context, req *GetWeatherRequest) (*GetWeatherResponse, error) {
	resp, err := http.Get("https://weather-api.example.com/...")
	// 如果 ctx 被取消（超时或用户中止），Get 不会立即停止
	// 会继续等待 API 响应，浪费资源
}
```

**正确做法**：

```go
// ✅ 正确做法：尊重 context
func GoodWeatherImpl(ctx context.Context, req *GetWeatherRequest) (*GetWeatherResponse, error) {
	// 创建一个带超时的 HTTP 请求
	req, err := http.NewRequestWithContext(ctx, "GET", "https://...", nil)
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Do(req)
	
	// 定期检查 context 是否被取消
	select {
	case <-ctx.Done():
		return nil, ctx.Err()
	default:
		// 继续处理
	}
}
```

### 🔓 陷阱 3：敏感信息泄露

**问题**：

```go
// ❌ 错误做法：把数据库凭证返回给模型
func QueryUserImpl(ctx context.Context, req *QueryRequest) (*UserData, error) {
	// ...
	return &UserData{
		Name:             user.Name,
		Email:            user.Email,
		DatabasePassword: user.DBPassword, // ❌ 千万不要这样做
		APIKey:           user.APIKey,     // ❌ 敏感信息
	}, nil
}
```

**正确做法**：

```go
// ✅ 正确做法：只返回必要的信息
func GoodQueryUserImpl(ctx context.Context, req *QueryRequest) (*UserData, error) {
	// ...
	return &UserData{
		Name:  user.Name,
		Email: user.Email,
		// 不返回任何敏感信息
		// 如果模型需要验证用户身份，应该由后端单独处理
	}, nil
}
```

### ❗ 陷阱 4：不处理模型参数错误

**问题**：

模型可能生成无效的参数 JSON。例如，即使你在 ToolInfo 中定义了 `unit` 必须是 "C" 或 "F"，模型仍然可能输出 `"unit": "K"`。

```go
// ❌ 不检查：
func WeatherImpl(ctx context.Context, req *GetWeatherRequest) (*GetWeatherResponse, error) {
	// 直接使用 req.Unit，如果是 "K"，可能导致计算错误
}

// ✅ 检查：
func WeatherImpl(ctx context.Context, req *GetWeatherRequest) (*GetWeatherResponse, error) {
	if req.Unit != "C" && req.Unit != "F" {
		return nil, fmt.Errorf("invalid unit: %s, must be C or F", req.Unit)
	}
	// 继续
}
```

### 💡 最佳实践 1：使用 InferTool 而不是 NewTool（当可能时）

InferTool 从静态类型生成 Schema，能保证参数的类型安全性。NewTool 需要手工维护 Schema，容易出错。

### 🌟 最佳实践 2：给工具描述添加示例

```go
type WeatherRequest struct {
	Location string `json:"location" description:"City name, e.g., Beijing, Shanghai, Guangzhou"`
	Unit     string `json:"unit" description:"Temperature unit: 'C' for Celsius or 'F' for Fahrenheit. Defaults to C."`
}
```

好的描述帮助模型更准确地调用工具。

### ✨ 最佳实践 3：工具结果要简洁且清晰

```json
// ✅ 好的返回
{
    "location": "Beijing",
    "temperature": 18.0,
    "condition": "Partly Cloudy",
    "unit": "C"
}

// ❌ 不好的返回：太复杂
{
    "location": {
        "name": "Beijing",
        "coordinates": {...},
        "timezone": "GMT+8",
        ...
    },
    "detailed_forecast": [...100 条记录...],
    "raw_api_response": {...}
}
```

简洁的结果让模型更容易理解，也更不容易引入噪声。

### 📊 最佳实践 4：记录工具调用

```go
import "log/slog"

func GetWeatherImpl(ctx context.Context, req *GetWeatherRequest) (*GetWeatherResponse, error) {
	slog.InfoContext(ctx, "get_weather called",
		"location", req.Location,
		"unit", req.Unit,
	)
	
	// ... 执行工具
	
	result := &GetWeatherResponse{...}
	slog.InfoContext(ctx, "get_weather result",
		"location", result.Location,
		"temperature", result.Temperature,
	)
	return result, nil
}
```

生产环境中，工具调用日志对于调试和监控至关重要。

---

## 🎓 总结

Eino 的工具体系通过清晰的分层设计，让你既能灵活定义各种工具，又能安全地集成到模型调用流程中。核心要点：

1. **三层设计**：ToolInfo（身份证）→ BaseTool（能力）→ InvokableTool（执行）
2. **两种创建方式**：InferTool 用于简单工具（类型安全），NewTool 用于复杂工具（灵活性）
3. **模型只负责选择**：真正的执行、验证、权限控制都在本地
4. **工具循环是自动化的**：ToolsNode 处理多轮调用和并发执行
5. **安全第一**：参数验证、敏感信息隐藏、超时控制都不能省

掌握工具定义和使用，你就能构建强大的 Agent 和 RAG 系统，让大模型真正有能力改变外部世界。

---

## 📚 相关资源

- [Eino 框架概述](https://tyritic.github.io/posts/eino-framework-overview/) — 了解 Eino 的整体设计理念
- [Eino 的基础组件（一）模型实例](https://tyritic.github.io/posts/eino-base-components-1-model/) — ChatModel 和 AgenticModel 的详细讲解
- [Eino 的基础组件（二）Prompt 模板与消息控制](https://tyritic.github.io/posts/eino-base-components-2-prompt/) — ChatTemplate 和消息管理
- [Eino GitHub 仓库](https://github.com/cloudwego/eino) — 源代码和完整 API 参考
- [eino-ext 工具和模型实现](https://github.com/cloudwego/eino-ext) — OpenAI、Ark、Claude 等模型的具体实现