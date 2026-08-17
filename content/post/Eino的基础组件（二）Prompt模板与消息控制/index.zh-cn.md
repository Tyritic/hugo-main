---
date : '2026-08-16T16:00:00+08:00'
draft : false
title : 'Eino的基础组件（二）Prompt模板与消息控制'
image : ""
categories : ["Eino框架"]
tags : []
description : "深入了解 Eino 框架中的 ChatTemplate 和 AgenticChatTemplate 组件，掌握 Prompt 模板的定义、变量替换、消息占位符等核心功能"
---

## 🎯 写在前面

在开发大模型应用时，构造合适的 Prompt 是个反复打磨的过程。每次调用模型，消息列表都是在代码里硬编码的。System Prompt 写死了，用户输入写死了，如果要改一个字就得改代码重新编译。更麻烦的是，当你想在不同的业务场景中复用同一套 Prompt 结构（只是具体内容不同），硬编码就变成了复制粘贴——这在工程上是不可接受的。

Eino 的 `ChatTemplate` 就是用来解决这个问题的。它把消息列表变成了一个模板，里面可以放变量占位符，运行时再填入实际值。更巧妙的是，它还支持 `MessagesPlaceholder`——你可以在模板的某个位置"留一个插槽"，运行时往里塞一组动态消息，比如历史对话记录。这两个能力组合起来，就让你的 Prompt 从"硬编码的字符串"变成了"可复用、可配置的结构化模板"。

这篇文章会详细介绍 `ChatTemplate` 和 `AgenticChatTemplate` 两个核心组件，帮你理解如何优雅地管理和复用 Prompt。如果你正在用 Eino 构建对话系统、Agent 或 RAG 应用，这篇文章会对你有帮助。

---

## 🏗️ Prompt 组件的设计理念

### 📖 核心职责

Eino 的 Prompt 组件本质上是一个**模板处理器**，负责将运行时的变量值填充到预定义的消息模板中，生成标准的 `Message` 列表供模型使用。

它的核心职责包括：

1. **变量替换**：将 `map[string]any` 中的值替换到模板中的占位符
2. **消息组装**：按照预定义的顺序组装 System、User、Assistant 等不同角色的消息
3. **历史注入**：通过 `MessagesPlaceholder` 在固定位置插入动态的对话历史
4. **类型安全**：通过接口约束，确保生成的消息格式符合模型要求

---

## 💬 ChatTemplate 

### 🔌 接口设计

`ChatTemplate` 是面向传统 `*schema.Message` 的 Prompt 组件：

```go
// ChatTemplate formats a variables map into a list of messages for a ChatModel.
//
// Format substitutes the values from vs into the template's message list and
// returns the resulting []*schema.Message. The exact substitution syntax
// (FString, GoTemplate, Jinja2) is determined at construction time.
//
// Variable keys present in the template but absent from vs produce a runtime
// error — there is no compile-time safety. Prefer consistent variable naming
// across templates and callers.
//
// In a Graph or Chain, ChatTemplate typically precedes ChatModel. Use
// compose.WithOutputKey to convert the prior node's output into the map[string]any
// that Format expects.
type ChatTemplate interface {
    Format(ctx context.Context, vs map[string]any, opts ...Option) ([]*schema.Message, error)
}
```

关键点：

- **输入**：`map[string]any` 类型的变量映射
- **输出**：`[]*schema.Message` 标准消息列表
- **错误处理**：如果模板中的变量在 `vs` 中不存在，会产生运行时错误（无编译时检查）
- **编排位置**：通常在 Chain 或 Graph 中位于 ChatModel 之前

Eino 提供了 `DefaultChatTemplate` 作为内置实现：

```go
type DefaultChatTemplate struct {
    // templates is the templates for the chat template.
    templates []schema.MessagesTemplate
    // formatType is the format type for the chat template.
    formatType schema.FormatType
}

// FromMessages creates a new DefaultChatTemplate from the given templates and format type.
func FromMessages(formatType schema.FormatType, templates ...schema.MessagesTemplate) *DefaultChatTemplate {
    return &DefaultChatTemplate{
        templates:  templates,
        formatType: formatType,
    }
}

// Format formats the chat template with the given context and variables.
func (t *DefaultChatTemplate) Format(ctx context.Context,
    vs map[string]any, _ ...Option) (result []*schema.Message, err error) {
    // 添加 callback 追踪
    ctx = callbacks.EnsureRunInfo(ctx, t.GetType(), components.ComponentOfPrompt)
    ctx = callbacks.OnStart(ctx, &CallbackInput{
        Variables: vs,
        Templates: t.templates,
    })
    defer func() {
        if err != nil {
            _ = callbacks.OnError(ctx, err)
        }
    }()

    // 遍历所有模板，依次填充变量
    result = make([]*schema.Message, 0, len(t.templates))
    for _, template := range t.templates {
        msgs, err := template.Format(ctx, vs, t.formatType)
        if err != nil {
            return nil, err
        }
        result = append(result, msgs...)
    }

    _ = callbacks.OnEnd(ctx, &CallbackOutput{
        Result:    result,
        Templates: t.templates,
    })

    return result, nil
}
```

从实现可以看出：

1. **支持多模板组合**：`templates` 是一个数组，可以包含多个消息模板
2. **灵活的格式类型**：`formatType` 支持 FString、GoTemplate、Jinja2 等多种模板语法
3. **完整的 Callback 支持**：方便调试和追踪模板处理过程

---

### 🎨 模板语法支持

Eino 支持三种常见的模板语法：

#### 🔤 FString（推荐）

最简单直观的变量替换语法，使用 `{变量名}` 占位符：

```go
template := prompt.FromMessages(schema.FString,
    schema.SystemMessage("你是一个专业的 {role} 助手"),
    schema.UserMessage("请回答：{question}"),
)

msgs, err := template.Format(ctx, map[string]any{
    "role":     "Go 语言",
    "question": "什么是 channel？",
})
```

生成的消息：
```
System: 你是一个专业的 Go 语言 助手
User: 请回答：什么是 channel？
```

#### 🔧 GoTemplate

支持 Go 标准库 `text/template` 的完整语法，可以使用条件、循环等控制结构：

```go
template := prompt.FromMessages(schema.GoTemplate,
    schema.SystemMessage("你是一个{{.role}}助手"),
    schema.UserMessage(`请回答以下问题：
{{range .questions}}
- {{.}}
{{end}}`),
)

msgs, err := template.Format(ctx, map[string]any{
    "role": "技术",
    "questions": []string{
        "什么是 goroutine？",
        "什么是 channel？",
    },
})
```

#### 🐍 Jinja2

支持 Jinja2 模板语法（常见于 Python 生态）：

```go
template := prompt.FromMessages(schema.Jinja2,
    schema.SystemMessage("你是 {{ role }} 助手"),
    schema.UserMessage("{{ question }}"),
)
```

{{< notice tip >}}
大多数场景下，FString 就够用了。只有在需要复杂的条件判断或循环时，才考虑使用 GoTemplate 或 Jinja2。
{{< /notice >}}

---

### 🚀 基础用法

- `prompt.FromMessages()` ：用于把多个 message 变成一个 ChatTemplate。
- `schema.Message{}` ：schema.Message 是实现了 Format 接口的结构体，因此可直接构建 `schema.Message{}` 作为 template
- `schema.SystemMessage()` ：此方法是构建 role 为 “system” 的 message 快捷方法
- `schema.AssistantMessage()` ：此方法是构建 role 为 “assistant” 的 message 快捷方法
- `schema.UserMessage()` ：此方法是构建 role 为 “User” 的 message 快捷方法
- `schema.ToolMessage()` ：此方法是构建 role 为 “tool” 的 message 快捷方法
- `schema.MessagesPlaceholder()` ：可用于把一个 `[]*schema.Message` 插入到 message 列表中，常用于插入历史对话

#### 📋 创建模板

```go
import (
    "github.com/cloudwego/eino/components/prompt"
    "github.com/cloudwego/eino/schema"
)

// 创建模板
template := prompt.FromMessages(schema.FString,
    schema.SystemMessage("你是一个{role}。"),
    schema.MessagesPlaceholder("history_key", false),
    &schema.Message{
        Role:    schema.User,
        Content: "请帮我{task}。",
    },
)

// 准备变量
variables := map[string]any{
    "role": "专业的助手",
    "task": "写一首诗",
    "history_key": []*schema.Message{{Role: schema.User, Content: "告诉我油画是什么?"}, {Role: schema.Assistant, Content: "油画是xxx"}},
}

// 格式化模板
messages, err := template.Format(context.Background(), variables)
```

#### 🔄 模板格式化和模型调用结合

模板本身只负责生成消息列表，要让模型真正回答，还得把生成的消息喂给 ChatModel。下面这个例子展示了完整的流程：

```go
package main

import (
        "context"
        "fmt"
        "log"
        "os"

        "github.com/cloudwego/eino-ext/components/model/openai"
        "github.com/cloudwego/eino/components/prompt"
        "github.com/cloudwego/eino/schema"
)

func main() {
        ctx := context.Background()

        // 创建 ChatModel
        cm, err := openai.NewChatModel(ctx, &openai.ChatModelConfig{
                BaseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
                APIKey:  os.Getenv("DASHSCOPE_API_KEY"),
                Model:   "qwen-plus",
        })
        if err != nil {
                log.Fatal(err)
        }

        // 定义一个翻译模板
        template := prompt.FromMessages(schema.FString,
                schema.SystemMessage("你是一个专业的{src_lang}到{dst_lang}翻译官，只输出翻译结果，不做解释。"),
                schema.UserMessage("请翻译：{text}"),
        )

        // 场景一：中译英
        messages, _ := template.Format(ctx, map[string]any{
                "src_lang": "中文",
                "dst_lang": "英文",
                "text":     "今天天气真好，适合写代码。",
        })
        resp, _ := cm.Generate(ctx, messages)
        fmt.Println("中译英:", resp.Content)

        // 场景二：英译日（同一个模板，不同的变量）
        messages, _ = template.Format(ctx, map[string]any{
                "src_lang": "English",
                "dst_lang": "日本語",
                "text":     "Go is a statically typed, compiled language.",
        })
        resp, _ = cm.Generate(ctx, messages)
        fmt.Println("英译日:", resp.Content)
}
```

---

### 🎭 MessagesPlaceholder 动态消息注入

在多轮对话场景中，我们需要在固定的位置插入动态的对话历史。`MessagesPlaceholder` 就是为此设计的：

```go
// MessagesPlaceholder 示例
template := prompt.FromMessages(schema.FString,
    schema.SystemMessage("你是一个有帮助的助手"),
    schema.MessagesPlaceholder("history", true),  // 插入历史消息
    schema.UserMessage("{question}"),
)

// 调用时传入历史消息
msgs, err := template.Format(ctx, map[string]any{
    "question": "上次我们聊到哪了？",
    "history": []*schema.Message{
        schema.UserMessage("Go 的并发模型是什么？"),
        schema.AssistantMessage("Go 使用 goroutine 和 channel 实现并发..."),
        schema.UserMessage("能详细说说 channel 吗？"),
        schema.AssistantMessage("Channel 是 Go 中用于 goroutine 间通信的管道..."),
    },
})
```

生成的消息顺序：
```
1. System: 你是一个有帮助的助手
2. User: Go 的并发模型是什么？
3. Assistant: Go 使用 goroutine 和 channel 实现并发...
4. User: 能详细说说 channel 吗？
5. Assistant: Channel 是 Go 中用于 goroutine 间通信的管道...
6. User: 上次我们聊到哪了？
```

{{< notice warning >}}
`MessagesPlaceholder` 的第二个参数 `optional` 如果设为 `true`，则当 `history` 变量不存在时不会报错。如果设为 `false`，则 `history` 必须提供。
{{< /notice >}}

---

## 🤖 AgenticChatTemplate 

### 🧠 接口设计

`AgenticChatTemplate` 是面向 `*schema.AgenticMessage` 的 Prompt 组件，专为复杂的 Agent 场景设计：用于把 `map[string]any` 中的变量填充到 agentic message 模板中，并输出 `[]*schema.AgenticMessage` 供 `AgenticModel` 或后续编排节点使用。

```go
// AgenticChatTemplate formats variables into a list of agentic messages according to a prompt schema.
type AgenticChatTemplate interface {
    Format(ctx context.Context, vs map[string]any, opts ...Option) ([]*schema.AgenticMessage, error)
}
```

核心区别：

| 特性           | ChatTemplate                     | AgenticChatTemplate                 |
| -------------- | -------------------------------- | ----------------------------------- |
| 输出类型       | `[]*schema.Message`              | `[]*schema.AgenticMessage`          |
| 适用场景       | 传统对话、RAG、简单 Agent        | 复杂 Agent、Reasoning、多模态       |
| 消息结构       | 扁平的 Role + Content            | 结构化的 ContentBlock 列表          |
| 工具调用       | ToolCalls 字段                   | FunctionToolCall ContentBlock       |
| Reasoning 支持 | 不支持                           | 原生支持 Reasoning ContentBlock     |
| 多模态支持     | 有限支持                         | 完整支持输入输出多模态 ContentBlock |

`DefaultAgenticChatTemplate` 的实现与 `DefaultChatTemplate` 非常相似：

```go
type DefaultAgenticChatTemplate struct {
    templates  []schema.AgenticMessagesTemplate
    formatType schema.FormatType
}

// FromAgenticMessages creates a new DefaultAgenticChatTemplate from the given templates and format type.
func FromAgenticMessages(formatType schema.FormatType, templates ...schema.AgenticMessagesTemplate) *DefaultAgenticChatTemplate {
    return &DefaultAgenticChatTemplate{
        templates:  templates,
        formatType: formatType,
    }
}

func (t *DefaultAgenticChatTemplate) Format(ctx context.Context, vs map[string]any, opts ...Option) (result []*schema.AgenticMessage, err error) {
    ctx = callbacks.EnsureRunInfo(ctx, t.GetType(), components.ComponentOfAgenticPrompt)
    ctx = callbacks.OnStart(ctx, &AgenticCallbackInput{
        Variables: vs,
        Templates: t.templates,
    })
    defer func() {
        if err != nil {
            _ = callbacks.OnError(ctx, err)
        }
    }()

    result = make([]*schema.AgenticMessage, 0, len(t.templates))
    for _, template := range t.templates {
        msgs, err := template.Format(ctx, vs, t.formatType)
        if err != nil {
            return nil, err
        }
        result = append(result, msgs...)
    }

    _ = callbacks.OnEnd(ctx, &AgenticCallbackOutput{
        Result:    result,
        Templates: t.templates,
    })

    return result, nil
}
```

---

### 🎪 构造方式

```go
func FromAgenticMessages(formatType schema.FormatType, templates ...schema.AgenticMessagesTemplate) *DefaultAgenticChatTemplate
```

`FromAgenticMessages` 不返回 `error`。它接收模板格式和一组 `schema.AgenticMessagesTemplate`，返回默认实现 `*DefaultAgenticChatTemplate`。

实例代码

```go
template := prompt.FromAgenticMessages(schema.FString,
    schema.SystemAgenticMessage("You are a {role}."),
    schema.AgenticMessagesPlaceholder("history", true),
    schema.UserAgenticMessage("Please help me {task}."),
)

messages, err := template.Format(ctx, map[string]any{
    "role": "concise assistant",
    "task": "summarize the following requirement",
    "history": []*schema.AgenticMessage{
        schema.UserAgenticMessage("Previous question"),
    },
})
if err != nil {
    return err
}
```

| 构造方式                                           | 说明                                                |
| -------------------------------------------------- | --------------------------------------------------- |
| `&schema.AgenticMessage{...}`                      | `AgenticMessage`自身实现了`AgenticMessagesTemplate` |
| `schema.SystemAgenticMessage(text)`                | 构造`system`role 消息                               |
| `schema.UserAgenticMessage(text)`                  | 构造`user`role 消息                                 |
| `schema.AgenticMessagesPlaceholder(key, optional)` | 从变量表中插入一组历史 agentic messages             |

和ChatTemplate一样支持以下 FormatType

| 格式       | 常量                | 占位符示例   | 适用场景                         |
| ---------- | ------------------- | ------------ | -------------------------------- |
| FString    | `schema.FString`    | `{role}`     | 简单变量替换                     |
| GoTemplate | `schema.GoTemplate` | `{{.role}}`  | 需要 Go`text/template`能力的场景 |
| Jinja2     | `schema.Jinja2`     | `{{ role }}` | 需要 Jinja2 语法的场景           |

---

## 🧪 实战代码示例

### 💡 基础用法：简单问答

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/cloudwego/eino/components/prompt"
    "github.com/cloudwego/eino/schema"
)

func main() {
    ctx := context.Background()

    // 创建 ChatTemplate
    tmpl := prompt.FromMessages(schema.FString,
        schema.SystemMessage("你是一个专业的 {role} 助手"),
        schema.UserMessage("请回答：{question}"),
    )

    // 填充变量
    msgs, err := tmpl.Format(ctx, map[string]any{
        "role":     "Go 语言",
        "question": "什么是 goroutine？",
    })
    if err != nil {
        log.Fatal(err)
    }

    // 打印生成的消息
    for _, msg := range msgs {
        fmt.Printf("[%s] %s\n", msg.Role, msg.Content)
    }
}
```

输出：
```
[system] 你是一个专业的 Go 语言 助手
[user] 请回答：什么是 goroutine？
```

---

### 🗣️ 多轮对话：带历史记录

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/cloudwego/eino/components/prompt"
    "github.com/cloudwego/eino/schema"
)

func main() {
    ctx := context.Background()

    // 创建带历史占位符的模板
    tmpl := prompt.FromMessages(schema.FString,
        schema.SystemMessage("你是一个有帮助的技术助手"),
        schema.MessagesPlaceholder("chat_history", true),
        schema.UserMessage("{user_input}"),
    )

    // 模拟多轮对话
    history := []*schema.Message{
        schema.UserMessage("Go 的并发模型是什么？"),
        schema.AssistantMessage("Go 使用 goroutine 和 channel 实现 CSP 并发模型。"),
    }

    // 新一轮对话
    msgs, err := tmpl.Format(ctx, map[string]any{
        "chat_history": history,
        "user_input":   "能举个例子吗？",
    })
    if err != nil {
        log.Fatal(err)
    }

    // 打印完整对话
    for i, msg := range msgs {
        fmt.Printf("%d. [%s] %s\n", i+1, msg.Role, msg.Content)
    }
}
```

输出：
```
1. [system] 你是一个有帮助的技术助手
2. [user] Go 的并发模型是什么？
3. [assistant] Go 使用 goroutine 和 channel 实现 CSP 并发模型。
4. [user] 能举个例子吗？
```

---

### 🧩 在 Chain 中使用

Prompt 组件通常作为 Chain 的第一个节点使用：

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "github.com/cloudwego/eino-ext/components/model/openai"
    "github.com/cloudwego/eino/components/prompt"
    "github.com/cloudwego/eino/compose"
    "github.com/cloudwego/eino/schema"
)

func main() {
    ctx := context.Background()

    // 创建 ChatModel
    cm, err := openai.NewChatModel(ctx, &openai.ChatModelConfig{
        APIKey: os.Getenv("OPENAI_API_KEY"),
        Model:  "gpt-4",
    })
    if err != nil {
        log.Fatal(err)
    }

    // 创建 ChatTemplate
    tmpl := prompt.FromMessages(schema.FString,
        schema.SystemMessage("你是一个 {role} 助手"),
        schema.UserMessage("{question}"),
    )

    // 构建 Chain：Prompt -> ChatModel
    chain := compose.NewChain[map[string]any, *schema.Message]()
    chain.AppendChatTemplate(tmpl)
    chain.AppendChatModel(cm)

    compiled, err := chain.Compile(ctx)
    if err != nil {
        log.Fatal(err)
    }

    // 运行 Chain
    result, err := compiled.Invoke(ctx, map[string]any{
        "role":     "Go 语言",
        "question": "什么是 context？",
    })
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println("模型回复:", result.Content)
}
```

---

### 🎛️ GoTemplate 高级用法

使用 GoTemplate 实现条件渲染和循环：

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/cloudwego/eino/components/prompt"
    "github.com/cloudwego/eino/schema"
)

func main() {
    ctx := context.Background()

    // 使用 GoTemplate 语法
    tmpl := prompt.FromMessages(schema.GoTemplate,
        schema.SystemMessage("你是一个{{.role}}专家"),
        schema.UserMessage(`请回答以下问题：
{{range $i, $q := .questions}}
{{add $i 1}}. {{$q}}
{{end}}

{{if .context}}
参考上下文：{{.context}}
{{end}}`),
    )

    // 填充变量
    msgs, err := tmpl.Format(ctx, map[string]any{
        "role": "Go 语言",
        "questions": []string{
            "什么是 goroutine？",
            "什么是 channel？",
            "如何避免死锁？",
        },
        "context": "这是 Go 并发编程的入门课程",
    })
    if err != nil {
        log.Fatal(err)
    }

    // 打印结果
    for _, msg := range msgs {
        fmt.Printf("[%s]\n%s\n\n", msg.Role, msg.Content)
    }
}
```

---

## ⚠️ 常见陷阱与最佳实践

### 🚨 变量缺失导致运行时错误

**错误示例**：

```go
tmpl := prompt.FromMessages(schema.FString,
    schema.UserMessage("请回答：{question}"),
)

// 忘记传入 question 变量
msgs, err := tmpl.Format(ctx, map[string]any{
    "role": "助手",  // 这个变量没有被使用
})
// 运行时错误：variable "question" not found
```

**正确做法**：

```go
// 确保所有模板中的变量都有对应的值
msgs, err := tmpl.Format(ctx, map[string]any{
    "question": "什么是 channel？",
})
```

{{< notice tip >}}
建议在开发阶段创建变量常量，避免拼写错误：
```go
const (
    VarQuestion = "question"
    VarRole     = "role"
    VarHistory  = "history"
)

tmpl := prompt.FromMessages(schema.FString,
    schema.UserMessage("{" + VarQuestion + "}"),
)
```
{{< /notice >}}

---

### 🔒 MessagesPlaceholder 的 Optional 参数

**场景**：首轮对话时没有历史记录

```go
// optional = false：history 必须提供，否则报错
tmpl := prompt.FromMessages(schema.FString,
    schema.SystemMessage("你是助手"),
    schema.MessagesPlaceholder("history", false),  // 严格模式
    schema.UserMessage("{question}"),
)

// 首轮对话没有 history，会报错
msgs, err := tmpl.Format(ctx, map[string]any{
    "question": "你好",
    // history 缺失，报错！
})
```

**推荐做法**：

```go
// optional = true：history 可选，不存在时自动跳过
tmpl := prompt.FromMessages(schema.FString,
    schema.SystemMessage("你是助手"),
    schema.MessagesPlaceholder("history", true),  // 可选模式
    schema.UserMessage("{question}"),
)

// 首轮对话不传 history 也不会报错
msgs, err := tmpl.Format(ctx, map[string]any{
    "question": "你好",
    // 不传 history 也没问题
})
```

---

### 📦 模板复用与组织

对于复杂项目，建议将常用模板抽取为函数或常量：

```go
package templates

import (
    "github.com/cloudwego/eino/components/prompt"
    "github.com/cloudwego/eino/schema"
)

// GetQATemplate 返回问答模板
func GetQATemplate() *prompt.DefaultChatTemplate {
    return prompt.FromMessages(schema.FString,
        schema.SystemMessage("你是一个专业的 {role} 助手"),
        schema.MessagesPlaceholder("history", true),
        schema.UserMessage("{question}"),
    )
}

// GetSummarizeTemplate 返回摘要模板
func GetSummarizeTemplate() *prompt.DefaultChatTemplate {
    return prompt.FromMessages(schema.FString,
        schema.SystemMessage("你是一个文本摘要助手"),
        schema.UserMessage("请对以下内容进行摘要：\n\n{content}"),
    )
}
```

使用时：

```go
tmpl := templates.GetQATemplate()
msgs, err := tmpl.Format(ctx, map[string]any{
    "role":     "Go 语言",
    "question": "什么是 interface？",
})
```

---

## 📝 总结

通过这篇文章，我们深入了解了 Eino 框架中的 Prompt 组件：

**ChatTemplate**：
- 面向传统 `*schema.Message`，适合对话、RAG、简单 Agent
- 支持 FString、GoTemplate、Jinja2 三种模板语法
- 通过 `MessagesPlaceholder` 灵活注入历史消息
- 通常作为 Chain 或 Graph 的第一个节点

**AgenticChatTemplate**：
- 面向 `*schema.AgenticMessage`，适合复杂 Agent 场景
- 支持 Reasoning、多模态、结构化工具调用
- 与 `AgenticModel` 配合使用

**最佳实践**：
- 优先使用 FString，复杂场景才考虑 GoTemplate
- `MessagesPlaceholder` 的 `optional` 参数根据场景选择
- 将常用模板抽取为函数，提高复用性
- 使用常量管理变量名，避免拼写错误

在下一篇文章中，我会详细介绍如何在 Graph 中使用 Prompt 组件，以及更高级的动态模板生成技巧。

---

## 🔗 相关资源

- [Eino 官方文档](https://github.com/cloudwego/eino)
- [Eino ChatTemplate User Guide](https://www.cloudwego.io/docs/eino/core_modules/components/chat_template_guide/)
- [Eino AgenticChatTemplate Guide](https://www.cloudwego.io/docs/eino/core_modules/components/agentic_chat_template_guide/)
- [Eino 框架概述](../Eino框架概述/)
- [Eino 的基础组件（一）ToolCallingChatModel 和 AgenticModel](../Eino的基础组件一ChatModel和AgenticModel/)

**Sources:**
- [Eino: ChatTemplate User Guide](https://www.cloudwego.io/docs/eino/core_modules/components/chat_template_guide/)
- [AgenticChatTemplate Guide [Beta]](https://www.cloudwego.io/docs/eino/core_modules/components/agentic_chat_template_guide/)
- [cloudwego/eino: The ultimate LLM/AI application development framework in Go.](https://github.com/cloudwego/eino)
