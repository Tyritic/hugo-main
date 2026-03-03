---
date : '2025-03-06T14:33:36+08:00'
draft : false
title : 'langchain4j基础和架构设计'
image : ""
categories : ["langchain4j"]
tags : ["AI","Java"]
description : "langchain4j是一个旨在简化Java语言中AI应用开发的框架。"
---

## 🤖 langchain4j 介绍

langchain4j 是一个旨在简化 Java 语言中 **AI** 应用开发的框架。它提供了一套统一的接口来与各种 **LLM**（大型语言模型）、**embedding**（嵌入）模型、向量数据库和其他工具交互，让开发者可以快速构建和集成 AI 功能，而不必担心底层实现细节。

### 🎯 主要功能与特色

- **模型集成**：支持 **OpenAI**、**Azure OpenAI**、**Google Vertex AI**、**HuggingFace** 等多种主流 LLM；
- **链式调用与组合**：提供了类似 LangChain 的链式构造，方便构建复杂的提示、流程与记忆；
- **Embedding 与向量存储**：内置常见的 **Embedding** 模型 API，以及对接 **Pinecone**、**Chroma**、**Redis** 等向量数据库；
- **工具与函数调用**：支持 LLM 调用本地工具或函数（Function Calling / Tool Use）；
- **文档加载与解析**：支持 PDF、Word、TXT 等常见文档的加载、文本分割与向量化。

---

## 🏗️ 整体架构与核心概念

langchain4j 的设计围绕"模型抽象"、"链式处理"、"记忆管理"、"RAG"等核心概念展开。以下是主要组成部分及架构：

1. **ChatLanguageModel / LanguageModel**  
   最核心的接口，用于和 LLM 交互，同步/流式发送消息并获取响应。
   - `ChatLanguageModel`：用于多轮对话模型（Chat Completion）；
   - `LanguageModel`：用于文本补全（Text Completion）等场景。
   
2. **EmbeddingModel**  
   嵌入模型抽象，可将文本转换为向量，用于相似度计算或存入向量数据库。

3. **ChatMemory / ChatMemoryProvider**  
   - 用于维护多轮对话历史；
   - `MessageWindowChatMemory`、`TokenWindowChatMemory` 等实现可管理消息数量或 Token 窗口。

4. **Chain（链）**  
   - 用于组装各种处理步骤，如提示模板 + LLM + 输出解析等。
   - `ConversationalChain`：带记忆的对话链；
   - `RetrievalChain`：用于信息检索增强问答；
   - `TextSegmentRetriever`：在向量存储中检索相关片段。

5. **Document / Splitter / EmbeddingStore**  
   - 文档加载、文本分割、向量存储相关组件。
   - `Document`：表示一个文档（文本 + 元数据）；
   - `DocumentSplitter`：将文档切分成若干 `TextSegment`；
   - `EmbeddingStore`：向量存储抽象，可插入 `InMemoryEmbeddingStore` 或对接第三方向量数据库。

6. **Tool / Tools**  
   - 让 LLM 可以调用你定义的函数（Function Calling / Tool Use）。
   - `Tool` 接口 + `@Tool` 注解 + `Tools` 工具类，可以快速暴露 Java 方法供模型调用。

<div align="center">
  <img src="image.png" alt="langchain4j架构图" width="60%">
</div>

---

## ⚙️ 分层设计与典型使用流程

langchain4j 从"模型层"、"链/工作流层"、"应用集成层"三个层面来组织功能：

### 1️⃣ 模型层（Model Layer）

- 目标：统一各种模型的调用方式
- 主要接口：`ChatLanguageModel`、`StreamingChatLanguageModel`、`EmbeddingModel`
- 使用示例：
  ```java
  ChatLanguageModel model = OpenAiChatModel.builder()
      .apiKey(System.getenv("OPENAI_API_KEY"))
      .modelName("gpt-3.5-turbo")
      .build();

  String response = model.generate("你好，请用 Java 示例解释什么是 Strategy 模式。");
  ```

### 2️⃣ 链/工作流层（Chain / Workflow Layer）

- 目标：编排提示、记忆、输出解析、检索等组件
- 主要组件：
  - `ConversationalChain`：封装对话记忆和提示模板，方便多轮对话；
  - `RetrievalChain` / `DefaultRetrievalChain`：结合 Embedding + Vector Store，进行 RAG 问答；
  - `PromptTemplate` / `SystemMessage` / `UserMessage`：构造更结构化的 Prompt。

### 3️⃣ 应用集成层（Integration Layer）

- 目标：对接外部系统、文档源、向量数据库
- 主要组件：
  - `DocumentLoader`：加载 PDF、TXT、HTML 等文档；
  - `DocumentSplitter` / `TextSegment`：将文档切分为更适合 Embedding 的片段；
  - `EmbeddingStore`：内存版或第三方向量存储（Pinecone、Chroma、Redis 等）。

---

## 📦 主要模块与包结构

在 langchain4j 的源码和使用中，通常可以看到以下核心包/模块：

- **核心** (`dev.langchain4j.model`, `dev.langchain4j.model.chat`, `dev.langchain4j.model.embedding` 等)：
  - 各种模型接口与实现（OpenAI、Azure OpenAI、HuggingFace、LocalAI 等）。

- **记忆** (`dev.langchain4j.memory` 包)：
  - `ChatMemory`、`MessageWindowChatMemory`、`TokenWindowChatMemory` 等，用于维护对话历史。

- **链** (`dev.langchain4j.chain` 包)：
  - `ConversationalChain`、`RetrievalChain` 等开箱即用的链。

- **数据与检索** (`dev.langchain4j.data`, `dev.langchain4j.store.embedding` 等)：
  - `Document`、`TextSegment`、`Embedding` 以及 `EmbeddingStore` 及其实现。

- **工具** (`dev.langchain4j.service` 以及 `dev.langchain4j.tool` 包)：
  - `@Tool` 注解、`Tools` 工具类、`AiServices` 代理工具，方便定义和绑定 LLM 可调用的工具。

---

## 📌 设计理念与扩展点

- **面向接口**：核心能力均通过接口抽象（如 `ChatLanguageModel`、`EmbeddingModel`、`EmbeddingStore`），便于切换不同厂商实现；
- **Builder 模式**：多数组件（如模型客户端、Chain、Memory）都提供 `Builder`，方便链式配置；
- **可组合**：通过 `AiServices`、自定义 `Chain` 或自行组装 `ChatMemory` + `ChatLanguageModel`，可以灵活满足不同业务需求；
- **轻量无依赖侵入**：langchain4j 不会强制引入大量第三方依赖，你可以按需选择所需的模块。

---

## 🎯 总结

- **langchain4j 是什么**：Java 世界中用于构建 **LLM** 应用的一个框架，提供了与多种模型、向量数据库、文档源集成的统一抽象；
- **为什么用它**：可以让你用 Java 语言也能方便地实现多轮对话、**RAG**、Function Calling、文档向量化等功能，而不必纠结于每家 API 的细节；
- **如何入手**：从 `ChatLanguageModel` 发起一次简单对话开始，再逐步加入 `ChatMemory`、`PromptTemplate`、`Document` 与 `EmbeddingStore`，最终搭建自己的 AI 应用。
