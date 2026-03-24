---
date : '2025-03-07T10:05:10+08:00'
draft : false
title : 'LangChain4j实现RAG系统'
image : ""
categories : ["LangChain4j"]
tags : ["后端开发"]
description : "RAG基础以及基于langchain4j的实现方式"
math : true
---

## 🤖 RAG 概述

**RAG**（Retrieval-Augmented Generation，检索增强生成）是一种将**信息检索**与**文本生成**结合的技术，其核心思想是：在回答用户问题前，先从私有的知识库或文档库中检索出相关的文本片段，再把这些片段连同用户问题一起送给 **LLM**，让模型可以基于这些"额外上下文"给出更准确、更有依据的回答。

使用 **RAG** 主要可以解决以下问题：

- **知识时效性**：**LLM** 的训练数据有截止日期，无法知道训练后的新知识；通过 **RAG** 可以动态检索最新文档。
- **私有/领域知识**：企业内部文档、特定领域的资料一般不会出现在公开训练数据中，需要 **RAG** 把这些信息"带给"模型。
- **减少幻觉**：有了检索到的上下文作为参考，模型更容易"有据可依"，降低瞎编的概率。

---

## 🏗️ RAG 的典型流程

在 langchain4j 中实现 **RAG**，通常可以分为以下几个步骤：

1. **文档加载与解析（Loading）**：读取 PDF、TXT、Word、HTML 等格式的文档，并提取出文本内容。
2. **文本切分（Splitting）**：把长文本切分成若干大小合适的"块（chunk）"或"文本段（text segment）"。
3. **向量化与存储（Embedding & Storing）**：把每个文本片段通过 **Embedding** 模型转换成向量，并存入向量数据库（Embedding Store）。
4. **检索（Retrieval）**：当用户提问时，把问题也转成向量，在向量库中检索出最相似的若干文本片段。
5. **增强生成（Augmented Generation）**：把用户问题 + 检索到的相关片段组装成提示，发送给 **LLM**，让模型根据这些信息回答问题。

<div align="center">
  <img src="image.png" alt="RAG流程图" width="82%">
</div>

---

## 📦 文档加载（Document Loading）

langchain4j 提供了 `Document` 类以及多种 `DocumentLoader` 实现，用于从不同来源加载文档：

- `FileSystemDocumentLoader`：从本地文件系统加载；
- `UrlDocumentLoader`：通过 URL 加载；
- `PdfDocumentLoader`（部分模块）：用于解析 PDF；
- 你也可以自己实现 `DocumentParser` 来定制解析逻辑。

### 示例：加载一个简单的文本文件

```java
Path filePath = Paths.get("path/to/your-document.txt");
Document document = FileSystemDocumentLoader.loadDocument(filePath);

// 或者一次加载目录下多个文件
List<Document> documents = FileSystemDocumentLoader.loadDocuments(
    Paths.get("path/to/your/docs"),
    new TextDocumentParser() // 或其他解析器，如 PdfDocumentParser
);
```

每个 `Document` 包含文本内容（`text()`）和元数据（`metadata()`），比如文件名、URL 等。

---

## ✂️ 文本切分（Document Splitting）

由于大多数 **Embedding** 模型对输入长度有限制，且太长的文本段也不利于精准检索，我们通常需要把文档切分成更短的片段。

langchain4j 提供了 `DocumentSplitter`，常见实现有 `DocumentSplitters` 工具类里的分段器：

```java
DocumentSplitter splitter = DocumentSplitters.recursive(
    500,    // 每个 segment 最多 500 字符/Token
    50       // 重叠 50 字符/Token，避免上下文被切断
);

List<TextSegment> segments = splitter.split(document);
```

- 第一个参数是**最大 segment 大小**，可以按字符数或 **Token** 数（取决于你使用的 splitter）控制；
- 第二个参数是**重叠大小**，让相邻片段有一些重叠，减少信息在切分处丢失的风险。

切分后得到的是 `TextSegment` 列表，每个 `TextSegment` 包含一段文本及其对应元数据。

---

## 🔢 向量化与存储（Embedding & Storing）

接下来我们需要：
1. 为每个 `TextSegment` 生成向量（embedding）；
2. 将"向量 + 原始文本 + 元数据"一起存入 `EmbeddingStore`。

### 1️⃣ 选择 EmbeddingModel

langchain4j 对 **Embedding** 模型也做了统一抽象，常见实现有：

- `OpenAiEmbeddingModel`：使用 **OpenAI** 的 embedding 接口；
- `AzureOpenAiEmbeddingModel`：**Azure OpenAI** 版本；
- `HuggingFaceEmbeddingModel`（需引入对应模块）：可以使用 **HuggingFace** 上的模型。

示例：

```java
EmbeddingModel embeddingModel = OpenAiEmbeddingModel.builder()
    .apiKey(apiKey)
    .modelName("text-embedding-ada-002") // 或其他 embedding 模型
    .build();
```

---

### 2️⃣ 选择并初始化 EmbeddingStore

`EmbeddingStore` 是向量存储的抽象，你可以选择：

- `InMemoryEmbeddingStore`：纯内存实现，适合原型、测试和数据量不大的场景；
- 第三方实现：如 `PineconeEmbeddingStore`、`ChromaEmbeddingStore`、`RedisEmbeddingStore` 等（需引入 langchain4j 对应模块）。

这里以 `InMemoryEmbeddingStore` 为例：

```java
EmbeddingStore<TextSegment> embeddingStore = new InMemoryEmbeddingStore<>();
```

---

### 3️⃣ 把切好的片段向量化并入库

一种方式是手动遍历并存储：

```java
for (TextSegment segment : segments) {
    Embedding embedding = embeddingModel.embed(segment).content();
    embeddingStore.add(embedding, segment);
}
```

也可以使用 langchain4j 提供的工具或 `EmbeddingStoreIngestor` 简化这一步：

```java
EmbeddingStoreIngestor ingestor = EmbeddingStoreIngestor.builder()
    .documentSplitter(splitter)
    .embeddingModel(embeddingModel)
    .embeddingStore(embeddingStore)
    .build();

ingestor.ingest(documents); // 一键完成切分、向量化、存储
```

---

## 🔍 检索（Retrieval）

当用户发来一个问题时，我们需要：
1. 把问题也用同样的 `EmbeddingModel` 转成向量；
2. 在 `EmbeddingStore` 中做相似度搜索，取回最相关的若干 `TextSegment`。

```java
String userQuery = "如何在 langchain4j 中实现 RAG？";
Embedding queryEmbedding = embeddingModel.embed(userQuery).content();

List<EmbeddingMatch<TextSegment>> relevantMatches = embeddingStore.findRelevant(
    queryEmbedding,
    3,       // 返回最相关的 3 个片段
    0.7      // 相似度阈值（可选，低于该值的结果会被过滤）
);

// 把匹配到的文本片段拼成一个字符串，用于后续传给 LLM
List<String> relevantSegments = relevantMatches.stream()
    .map(EmbeddingMatch::embedded)
    .map(TextSegment::text)
    .collect(Collectors.toList());

String context = String.join("\n\n", relevantSegments);
```

---

## 💬 增强生成（Augmented Generation）

拿到检索出来的相关片段后，我们需要把它们和用户问题一起组织成 Prompt，然后发给 **LLM** 生成回答。

### 1️⃣ 使用 `PromptTemplate` 组装提示

```java
PromptTemplate promptTemplate = PromptTemplate.from(
    "请根据下面的上下文回答用户问题。如果无法从上下文中得到答案，请说明你不知道。\n\n" +
    "上下文：\n{{context}}\n\n" +
    "用户问题：{{question}}"
);

Prompt prompt = promptTemplate.apply(
    Map.of(
        "context", context,
        "question", userQuery
    )
);

ChatLanguageModel chatLanguageModel = OpenAiChatModel.builder()
    .apiKey(apiKey)
    .modelName("gpt-3.5-turbo")
    .build();

String answer = chatLanguageModel.generate(prompt.text());
System.out.println("最终回答：" + answer);
```

---

### 2️⃣ 开箱即用的 `RetrievalChain`

langchain4j 提供了 `DefaultRetrievalChain` 或 `RetrievalChain`，帮你把"检索 + 组装提示 + 调用模型"封装在一起：

```java
ContentRetriever contentRetriever = EmbeddingStoreContentRetriever.builder()
    .embeddingStore(embeddingStore)
    .embeddingModel(embeddingModel)
    .maxResults(3)
    .minScore(0.7)
    .build();

RetrievalChain retrievalChain = DefaultRetrievalChain.builder()
    .chatLanguageModel(chatLanguageModel)
    .contentRetriever(contentRetriever)
    // 可选：自定义 prompt template
    // .promptTemplate(...)
    .build();

ChainInput input = ChainInput.from(userQuery);
ChainOutput output = retrievalChain.execute(input);
String answer = output.content().text();
```

---

## 🏷️ 使用 `AiServices` 简化 RAG

如果你喜欢更简洁的方式，可以结合 `AiServices` 和 `ContentRetriever`，让 **RAG** 的使用和普通对话一样简单：

```java
interface RagAssistant {
    @SystemMessage("你是一个文档助手，请参考提供的上下文回答用户问题。")
    String chat(@UserMessage String userMessage);
}

ContentRetriever contentRetriever = EmbeddingStoreContentRetriever.builder()
    .embeddingStore(embeddingStore)
    .embeddingModel(embeddingModel)
    .maxResults(3)
    .build();

RagAssistant assistant = AiServices.builder(RagAssistant.class)
    .chatLanguageModel(chatLanguageModel)
    .contentRetriever(contentRetriever) // 这里接入你的 RAG 检索器
    .build();

String answer = assistant.chat("如何在 langchain4j 中使用 EmbeddingStore？");
System.out.println(answer);
```

- 加上 `contentRetriever` 后，`AiServices` 会自动在每次调用前进行检索，并把相关片段插入到上下文中。

---

## 🌟 常见优化与进阶方向

**RAG** 的效果受很多因素影响，以下是一些常见的优化思路：

1. **Embedding 模型与分段策略**：
   - 尝试更强的 **Embedding** 模型（如 text-embedding-3-small/large）；
   - 根据文档类型、语言特点调整切分大小和重叠窗口；
   - 可以在切分时保留文档结构（如标题层级），提升检索质量。

2. **检索质量**：
   - 除了相似度分数，也可以结合元数据过滤（Metadata Filtering）；
   - 对检索到的片段进行重排（Rerank），例如使用专门的 Reranker 模型或交叉编码器；
   - 尝试混合检索（Hybrid Search），把向量相似度和关键词检索结合。

3. **提示工程**：
   - 在 Prompt 中明确要求模型引用上下文来源，或注明"根据上下文回答"；
   - 若有多段检索结果，可以给它们编号或加上出处，让模型更容易组织答案。

4. **对话记忆与 RAG 结合**：
   如果你需要结合多轮对话历史进行 **RAG**，可以：
   - 使用 `ChatMemory` 记住历史消息；
   - 在检索前，先让模型基于历史和当前问题生成一个"更适合检索的查询"；
   - 或把最近几轮对话也作为 context 的一部分一起检索/生成。

---

## 📌 总结

- **RAG 能做什么**：通过检索私有/最新文档，让 **LLM** 回答更有时效性、更领域化，并减少幻觉。
- **langchain4j 中的核心组件**：
  - `Document` / `DocumentLoader`：加载文档；
  - `DocumentSplitter` / `TextSegment`：切分文本；
  - `EmbeddingModel`：把文本转为向量；
  - `EmbeddingStore`：存储和检索向量 + 文本；
  - `ContentRetriever` / `RetrievalChain` / `AiServices`：把前面的步骤串联起来，形成 **RAG** 流程。
- **使用建议**：
  - 初期可以用 `InMemoryEmbeddingStore` + `EmbeddingStoreIngestor` + `RetrievalChain` 或 `AiServices` 快速跑通原型；
  - 后续根据需要再替换成生产级向量库、优化切分与 **Embedding** 策略、引入重排等。
