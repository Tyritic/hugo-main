---
date : '2025-03-06T14:33:36+08:00'
draft : false
title : 'Langchain4j基础和架构设计'
image : ""
categories : ["LangChain4j"]
tags : ["后端开发"]
description : "记录识物探趣项目中对LLM的支持"
math : true
---

## LangChain4j

LangChain4j是LangChain的java版本，目的是简化将 LLM 集成到 Java 应用程序中的过程

### 核心功能

1. **统一API**：LangChain4j提供了标准化的API，使得可以方便地接入主流的LLM提供商，可以轻松切换不同的模型和存储，而无需重写代码。
2. **综合工具箱**：该框架包含多种工具，从低级的提示模板、聊天记忆管理到高级模式（如AI服务和RAG）。这些工具帮助开发者构建从聊天机器人到完整的数据检索管道等多种应用。
3. **多模态支持**：LangChain4j支持文本和图像作为输入，能够处理更复杂的应用场景。

## 架构设计

langchain4j的软件架构采用模块结构和层次结构

### 层次结构

从文档中可以看出langchain4j提供了两个层次：**`Low level`** 和 **`high level`** 。框架在两个抽象层次上运行，允许开发者根据需要选择低级或高级API进行开发，从而提高灵活性和可用性。

- **`low level`** ：在这一抽象层次。可以最自由地访问所有低级组件，这些是 LLM 支持的应用程序的 “基元”。 可以完全控制如何组合它们，但您需要编写更多的代码。
- **`high level`** : 在这一抽象层次，使用 **`AIService`** 等高级 API 与 LLM 进行交互。 隐藏了所有的复杂性和样板，以声明方式可以灵活地调整和微调行为。

### 模块结构

- `langchain4j-core`  模块，定义了核心抽象 
- 主模块：包含有用的工具，如文档加载器、聊天内存实现以及 AIService等高级特性。
- 一系列的`langchain4j-{integration}` 模块 ：每个提供与各种LLM的集成，并将存储嵌入到LangChain4j中。
  

## 基础使用

- 本项目以在本地Ollama部署的deepseek-r1模型作为基础LLM模型。Ollama本身作为基础LLM模型的抽象层

- 在maven项目中导入相关依赖

  - 在SpringBoot框架中引入langchain4j-ollama支持

    ```xml
    <dependency>
            <groupId>dev.langchain4j</groupId>
            <artifactId>langchain4j-ollama</artifactId>
            <version>1.0.0-beta1</version>
    </dependency>
    
    <dependency>
                <groupId>dev.langchain4j</groupId>
                <artifactId>langchain4j</artifactId>
                <version>1.0.0-beta1</version>
            </dependency>
    
    <!-- 如果要通过application.yml中自动配置Bean才引入 -->
    <dependency>
             <groupId>dev.langchain4j</groupId>
             <artifactId>langchain4j-ollama-spring-boot-starter</artifactId>
             <version>1.0.0-beta1</version>
    </dependency>
    ```

    

  - 引入langchain4j的高级抽象层

    ```xml
    <dependency>
           <groupId>dev.langchain4j</groupId>
           <artifactId>langchain4j-spring-boot-starter</artifactId>
           <version>1.0.0-beta1</version>
    </dependency>
    ```

  - 引入RAG的相关支持

    ```xml
    <dependency>
                <groupId>dev.langchain4j</groupId>
                <artifactId>langchain4j-easy-rag</artifactId>
                <version>1.0.0-beta1</version>
            </dependency>
    ```

    

- 在application.yml中设置ollama模型的元信息，包括模型名称，ollama服务的url等等

