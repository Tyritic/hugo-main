
---
date : '2025-03-06T15:40:51+08:00'
draft : false
title : 'langchain4j实现模型交互'
image : ""
categories : ["LangChain4j"]
tags : ["后端开发"]
description : "LangChain4j中对语言和聊天能力的支持"
math : true
---

## 🤖 模型交互核心抽象

### 1️⃣ `ChatLanguageModel` / `StreamingChatLanguageModel`

`ChatLanguageModel` 是 langchain4j 中最核心的接口之一，定义了与对话类模型（如 gpt-3.5-turbo、gpt-4 等）交互的统一方法。

#### 主要方法

- `String generate(String userMessage)`：发送单条用户消息，同步返回模型响应文本。
- `Response&lt;ChatResponse&gt; generate(ChatMessage... messages)`：发送多条消息（如系统消息、用户消息、助手消息），可获取包含 Token 用量、finish reason 等更丰富信息的响应对象。
- `Response&lt;ChatResponse&gt; generate(List&lt;ChatMessage&gt; messages, List&lt;ToolSpecification&gt; toolSpecifications)`：在生成时提供工具/函数定义，供模型选择调用。

如果你需要**流式**返回（一边生成一边输出），可以使用 `StreamingChatLanguageModel`，用法类似，但通过回调 `StreamingResponseHandler` 来逐步接收 Token：

```java
StreamingChatLanguageModel model = OpenAiStreamingChatModel.builder()
    .apiKey(apiKey)
    .modelName("gpt-3.5-turbo")
    .build();

model.generate("讲一个长一点的科幻故事", new StreamingResponseHandler() {
    @Override
    public void onNext(String token) {
        System.out.print(token);
    }

    @Override
    public void onError(Throwable error) {
        error.printStackTrace();
    }
});
```

---

### 2️⃣ 消息类型（`ChatMessage` 体系）

在 langchain4j 中，对话消息被抽象成了不同类型的 `ChatMessage`，常见的有：

- `SystemMessage`：系统消息，用于设定助手的人设、行为准则等。
- `UserMessage`：用户消息，包含用户输入的内容，也可以附加图片等多媒体（部分模型支持）。
- `AiMessage`：AI 助手消息，代表模型上一次的返回。
- `ToolExecutionResultMessage`：工具执行结果消息，用于在 Function Calling / Tool Use 流程中把工具返回值传回模型。

你可以通过 `SystemMessage.from(...)`、`UserMessage.from(...)` 等工厂方法方便地构造它们：

```java
List&lt;ChatMessage&gt; messages = new ArrayList&lt;&gt;();
messages.add(SystemMessage.from("你是一个乐于助人的 Java 专家，请用简洁清晰的方式回答问题。"));
messages.add(UserMessage.from("请解释什么是 Strategy 设计模式？"));

Response&lt;ChatResponse&gt; response = chatLanguageModel.generate(messages);
AiMessage aiMessage = response.content().aiMessage();
System.out.println(aiMessage.text());
```

---

## 💾 对话记忆管理（ChatMemory）

为了实现多轮对话，langchain4j 提供了 `ChatMemory` 接口以及若干开箱即用的实现，用于保存和管理历史消息。

### 1️⃣ `MessageWindowChatMemory`

基于**消息数量**的滑动窗口记忆：

```java
ChatMemory chatMemory = MessageWindowChatMemory.withMaxMessages(10);
```

- 会自动保留最近的 10 条消息，超过时会“挤掉”最早的消息。
- 使用非常简单，适合消息条数不多且 Token 占用可控的场景。

---

### 2️⃣ `TokenWindowChatMemory`

基于 **Token 数量**的滑动窗口记忆：

```java
ChatMemory chatMemory = TokenWindowChatMemory.builder()
    .maxTokens(1000)
    .chatMemory(MessageWindowChatMemory.withMaxMessages(1000)) // 用于兜底的存储
    .tokenizer(new OpenAiTokenizer())
    .build();
```

- 更精细地控制对话历史的 Token 占用，避免超过模型上下文窗口限制。
- 需要提供一个 `Tokenizer`（如 `OpenAiTokenizer`），用于估算文本 Token 数。

---

### 3️⃣ 在交互中使用 ChatMemory

你可以手动将消息添加到 `ChatMemory`，或结合 `ConversationalChain` / `AiServices` 自动管理：

```java
ChatLanguageModel model = OpenAiChatModel.builder().apiKey(apiKey).build();
ChatMemory chatMemory = MessageWindowChatMemory.withMaxMessages(10);

// 方式一：手动管理
chatMemory.add(SystemMessage.from("你是一个 Python 导师。"));
chatMemory.add(UserMessage.from("什么是列表推导式？"));

Response&lt;ChatResponse&gt; response = model.generate(chatMemory.messages());
AiMessage aiMessage = response.content().aiMessage();
chatMemory.add(aiMessage);

System.out.println("AI: " + aiMessage.text());

// 下一轮对话
chatMemory.add(UserMessage.from("能不能再举个例子？"));
Response&lt;ChatResponse&gt; response2 = model.generate(chatMemory.messages());
// ...
```

---

## 🛠️ 提示模板（Prompt Template）

很多时候我们需要复用一套提示结构，只替换部分变量（如用户问题、上下文片段等）。langchain4j 提供了 `PromptTemplate`、`ChatPromptTemplate` 来满足这种需求。

### 1️⃣ 简单文本提示模板

```java
PromptTemplate promptTemplate = PromptTemplate.from(
    "请对以下文本进行总结，控制在 50 字以内：\n{{text}}"
);

Prompt prompt = promptTemplate.apply(
    Map.of("text", "这里是很长很长的一段待总结文本...")
);

String userMessage = prompt.text();
String response = chatLanguageModel.generate(userMessage);
```

使用 `{{变量名}}` 在模板中占位，然后通过 `Map` 传入实际值。

---

### 2️⃣ 对话提示模板（ChatPromptTemplate）

如果你需要按角色（System/User/Assistant）组织提示，可以使用 `ChatPromptTemplate`：

```java
ChatPromptTemplate chatPromptTemplate = ChatPromptTemplate.from(
    SystemMessage.from("你是一个文档小助手，参考下面的上下文回答用户问题。"),
    UserMessage.from("上下文：\n{{context}}\n\n用户问题：{{question}}")
);

List&lt;ChatMessage&gt; messages = chatPromptTemplate.applyMessages(
    Map.of(
        "context", "某某框架的主要特性有：A、B、C...",
        "question", "这个框架的主要特性是什么？"
    )
);

Response&lt;ChatResponse&gt; response = chatLanguageModel.generate(messages);
```

---

## 🔌 使用 Chain 封装常用流程

langchain4j 提供了 `Chain` 接口以及多个开箱即用的实现，帮你把“记忆 + 提示 + 模型 + 输出解析”等步骤封装成一条可以复用的链。

### 1️⃣ `ConversationalChain`

适用于带记忆的多轮对话：

```java
ChatLanguageModel model = OpenAiChatModel.builder().apiKey(apiKey).build();
ChatMemory chatMemory = MessageWindowChatMemory.withMaxMessages(10);

ConversationalChain chain = ConversationalChain.builder()
    .chatLanguageModel(model)
    .chatMemory(chatMemory)
    // 可选：自定义 system message
    .promptTemplate(ChatPromptTemplate.from(SystemMessage.from("你是一个导游。")))
    .build();

String answer1 = chain.execute("推荐一下北京好玩的地方。");
System.out.println("AI: " + answer1);

String answer2 = chain.execute("那其中哪个最适合带小孩去？");
System.out.println("AI: " + answer2);
```

---

### 2️⃣ `RetrievalChain` / `DefaultRetrievalChain`

用于结合向量检索做 RAG（检索增强生成），我们会在后面专门介绍。

---

## 🏷️ AiServices：更高级的服务封装

如果你希望以“调用 Java 接口方法”的方式和 LLM 交互，而不手动组织消息和记忆，可以使用 `AiServices`。

### 1️⃣ 定义接口

```java
interface CustomerService {
    String chat(String userMessage);
}
```

---

### 2️⃣ 通过 `AiServices` 生成代理并使用

```java
ChatLanguageModel model = OpenAiChatModel.builder().apiKey(apiKey).build();
ChatMemory chatMemory = MessageWindowChatMemory.withMaxMessages(10);

CustomerService service = AiServices.builder(CustomerService.class)
    .chatLanguageModel(model)
    .chatMemory(chatMemory)
    .build();

String reply1 = service.chat("你好，我想查一下我的订单。");
String reply2 = service.chat("算了，帮我转人工吧。");
```

- 可以在接口方法上通过 `@SystemMessage`、`@UserMessage` 等注解自定义提示模板；
- 也可以结合 `@Tool` 注解让模型在需要时自动调用你的工具方法。

---

## 🔧 工具调用（Tool / Function Calling）

很多模型（如 gpt-3.5-turbo、gpt-4）支持 function calling / tool use。langchain4j 提供了多种方式让你把 Java 方法暴露给模型调用。

### 1️⃣ 使用 `@Tool` 注解

```java
class WeatherTools {
    @Tool("查询指定城市的当前天气，入参为城市名，如“北京”、“上海”")
    String getCurrentWeather(String city) {
        // 这里仅做模拟，实际可对接天气 API
        if ("北京".equals(city)) {
            return "北京：晴，15°C";
        } else if ("上海".equals(city)) {
            return "上海：多云，20°C";
        }
        return "暂无该城市天气信息。";
    }
}
```

---

### 2️⃣ 在交互中让模型选择并执行工具

#### 方式一：使用 `ChatLanguageModel` + `ToolSpecification`

```java
ChatLanguageModel model = OpenAiChatModel.builder().apiKey(apiKey).build();

// 构造工具定义（也可以用 Tools.toolDefinitionsFrom(...) 从带 @Tool 的对象自动生成）
List&lt;ToolSpecification&gt; toolSpecs = Tools.toolSpecificationsFrom(new WeatherTools());

List&lt;ChatMessage&gt; messages = new ArrayList&lt;&gt;();
messages.add(UserMessage.from("北京今天天气怎么样？"));

Response&lt;ChatResponse&gt; response = model.generate(messages, toolSpecs);
ChatResponse chatResponse = response.content();

AiMessage aiMessage = chatResponse.aiMessage();
if (aiMessage.hasToolExecutionRequests()) {
    for (ToolExecutionRequest toolExecutionRequest : aiMessage.toolExecutionRequests()) {
        // 这里可以根据 toolExecutionRequest.name() 和 arguments() 手动调用你的方法，
        // 也可以使用 Tools.execute(...) 等工具方法
        Object result = Tools.execute(toolExecutionRequest, new WeatherTools());
        messages.add(aiMessage);
        messages.add(ToolExecutionResultMessage.from(toolExecutionRequest, result));
    }
    // 再次请求模型，让它根据工具执行结果生成最终回答
    Response&lt;ChatResponse&gt; secondResponse = model.generate(messages, toolSpecs);
    System.out.println("最终回答：" + secondResponse.content().aiMessage().text());
}
```

---

#### 方式二：使用 `AiServices` + `@Tool`，自动处理

```java
interface WeatherAssistant {
    String chat(String userMessage);
}

// ...

WeatherAssistant assistant = AiServices.builder(WeatherAssistant.class)
    .chatLanguageModel(model)
    .tools(new WeatherTools()) // 直接把带 @Tool 的对象传进去
    .build();

String answer = assistant.chat("上海今天天气如何？");
System.out.println(answer);
```

- `AiServices` 会自动识别工具调用请求、执行对应方法、把结果返回给模型并获取最终回答，无需你手动管理中间步骤。

---

## 📌 总结

- **模型交互**：通过 `ChatLanguageModel` / `StreamingChatLanguageModel` 统一同步和流式对话的调用方式；
- **消息体系**：使用 `SystemMessage`、`UserMessage`、`AiMessage`、`ToolExecutionResultMessage` 等来组织多轮对话和工具调用流程；
- **对话记忆**：`MessageWindowChatMemory` 基于条数、`TokenWindowChatMemory` 基于 Token 来管理历史消息，避免超限；
- **提示模板**：`PromptTemplate` / `ChatPromptTemplate` 帮助你复用提示结构，减少重复代码；
- **Chain 与 AiServices**：`ConversationalChain`、`RetrievalChain` 等封装常见流程；`AiServices` 允许你用接口方法的形式与 LLM 交互，同时也能方便地集成 `@Tool`；
- **工具调用**：可以使用 `@Tool` + `Tools` 工具类，也可以通过 `AiServices` 自动处理，让模型能够调用你的业务方法。

