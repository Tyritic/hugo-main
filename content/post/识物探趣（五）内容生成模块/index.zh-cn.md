---
date : '2025-03-15T20:49:08+08:00'
draft : false
title : '识物探趣（五）内容生成模块'
image : ""
categories : ["个人项目"]
tags : ["后端开发"]
description : ""
math : true
---

## RAG技术的应用

检索增强生成（Retrieval-Augmented Generation，RAG）是一种结合大型语言模型（LLM）和外部知识库的技术，旨在提高生成文本的准确性和相关性。 RAG的核心思想是通过引入外部知识源来增强LLM的输出能力。传统的LLM通常基于其训练数据生成响应，但这些数据可能过时或不够全面。RAG允许模型在生成答案之前，从特定的知识库中检索相关信息，从而提供更准确和上下文相关的回答。展馆提供了相关的文档

## 模型和向量数据库选择

- LLM：**qwen2.5:32b**
- Embedding Model：**bge-small-zh-v1.5**（向量维度为 **512** ）
- 向量数据库：**Qdrant**

## RAG实现方案

本项目使用langchain4j来实现RAG功能，langchain4j提供了构建RAG管道的解决方案

### RAG管道的构建

#### 总体构建流程

- 加载并解析文档：从文件系统中加载本地知识库的文件，使用 **`ApachePoiDocumentParser`** 解析本地知识库的文件
- 转换文档：文件比较简单，暂时不需要进行清理和增强
- 拆分文档：根据文档特点选择，将文档拆分为小片段
- 嵌入文档：配置摄取器将被拆分后的文档进行向量化后存储在向量数据库中
- 检索相关内容：配置检索增强器来增强检索效果
- 聚合注入内容：在检索增强器中配置注入器来优化用户查询

#### 加载转换文档

本地知识库由以下部分构成

- 展馆方提供的展品资料文档，存储在文件系统中。本地知识库中大部分为docx文件
- 网络上的相关资料

对于本地文件系统的文档，使用 **`FileSystemDocumentLoader`** 作为文件加载器，使用 **`ApachePoiDocumentParser`** 作为文件解析器

#### 拆分文档

根据对本地知识库的文档进行分析，文档具有以下特点

- 段落结构明显
- 每个段落描述完整的思想单元

因此文档的划分策略选择为 **按照段落进行划分** ，使用的文档划分器为 **`DocumentByParagraphSplitter`**

#### 嵌入文档

根据本地文档的大小选择嵌入模型为 **bge-small-zh-v1.5** ，该嵌入模型可以将文本块转换为维度为 **512** ，同时选择 **Qdrant** 作为向量数据库。通过配置摄取器将本地文档嵌入到向量知识库中

```java
// 摄取器
@Bean
    public EmbeddingStoreIngestor embeddingStoreIngestor(EmbeddingModel embeddingModel, InMemoryEmbeddingStore<TextSegment> embeddingStore) {
        return EmbeddingStoreIngestor.builder()
               .embeddingModel(embeddingModel)
               .embeddingStore(embeddingStore)
               .documentSplitter(new DocumentByParagraphSplitter(300,0))
                .build();
    }
// 向量数据库的配置
@Bean
public EmbeddingStore<TextSegment> embeddingStore() {
    return QdrantEmbeddingStore.builder()
            .host("xxx")
            .port(6334)
            .collectionName("xxx")
            .build();
}

// 配置嵌入模型
@Bean
public EmbeddingModel embeddingModel() {
     return OllamaEmbeddingModel.builder()
            .baseUrl("http://127.0.0.1:11434")
            .modelName("quentinz/bge-small-zh-v1.5")
            .build();
    }

```

#### 检索内容

知识库有多个数据源，因此需要为不同的数据源构建 **内容检索器** ，同时也要为不同的内容源配置 **查询路由器** 。

内容检索器的配置中定义

- 设置 **最大检索结果数量**，最多返回 2条匹配内容。
- 设置 **最小匹配分数**，只有相似度大于 `0.75` 的内容才会返回。
- 设置 **动态过滤器** ，确保只是检索当前用户的资料

其中本地文档的内容检索器和网络资源的内容检索器定义如下

```java
// 本地文档的内容检索器
@Bean
    public EmbeddingStoreContentRetriever contentRetriever(EmbeddingModel embeddingModel, InMemoryEmbeddingStore<TextSegment> embeddingStore){
        return EmbeddingStoreContentRetriever.builder()
                .embeddingStore(embeddingStore)
                .embeddingModel(embeddingModel)
                .dynamicFilter(query -> {
                    String userId = getUserId(query.metadata().chatMemoryId());
                    return metadataKey("userId").isEqualTo(userId);
                })
                .minScore(0.75)
                .maxResults(2)
                .build();
    }
// 网络资源的内容检索器
@Bean
    public WebSearchEngine webSearchEngine(){
        return TavilyWebSearchEngine.builder()
                .apiKey("XXX")
                .build();
    }
    
    @Bean
    public WebSearchContentRetriever webSearchContentRetriever(WebSearchEngine webSearchEngine) {
        return WebSearchContentRetriever.builder()
                .webSearchEngine(webSearchEngine)
                .maxResults(3)
                .build();
    }
```

由于知识库有多个数据源，可以实现结构重排，在 **内容聚合器** 上有两种策略可以选择

- 默认实现：使用RRF策略进行结果重排
- **`ReRankingContentAggregator`** ：使用重排序进行结果重排

在策略的选择方面，通过查阅资料可知

- **RRF** 策略更加适合多数据源的融合排序，但是会对语义匹配略有损失
- **Rerank** 策略基于深度学习模型需要足够大的知识库进行结果重排，同时在长文本的匹配上具有优势

经过对比选择默认的 **RRF** 策略进行内容聚合

为了将内容聚合后的结果注入到用户查询中，需要配置 **内容注入器** ，内容注入器采用默认策略即可

同时根据项目中上下文的场景，配置 **查询转换器** ，使用LLM来压缩查询和对话上下文，提高查询的质量

由此可以构建出一个完整的检索增强器

```java
@Bean
    public DefaultRetrievalAugmentor defaultRetrievalAugmentor(EmbeddingStoreContentRetriever embeddingStoreContentRetriever,OllamaChatModel ollamaChatModel,WebSearchContentRetriever webSearchContentRetriever){
        return DefaultRetrievalAugmentor.builder()
                // 配置压缩查询转换器:使用ollamaChatModel压缩查询
                .queryTransformer(new CompressingQueryTransformer(ollamaChatModel))
                // 配置内容注入器:默认实现
                .contentInjector(new DefaultContentInjector())
                // 配置内容聚合器:采用默认实现的RRF策略进行结果重排
                .contentAggregator(new DefaultContentAggregator())
                // 配置查询路由器:采用默认实现
                .queryRouter(new DefaultQueryRouter(embeddingStoreContentRetriever, webSearchContentRetriever))
               .build();
    }
```

## 流式响应的实现方案

出于对用户使用体验的考虑，使用流式响应比一次性响应在用户体验上表现更好。

langchain4j提供了实现流式响应的方法，**`Flux<String> chat(@V("question") String question)`**

可以使用Flux流式响应+SSE协议实现

```java
@RestController
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
@RequestMapping("/common")
public class DemoController {
    @Autowired
    private final StreamChatAssistant chatAssistant;

    @Autowired
    EmbeddingStore<TextSegment> embeddingStore;

    @Autowired
    EmbeddingModel embeddingModel;
    @GetMapping(value="/chat",produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> chat(@RequestParam("message") String message) {
        Document document = FileSystemDocumentLoader.loadDocument("xxxxxx");
        EmbeddingStoreIngestor.ingest(document, embeddingStore);
        return chatAssistant.chat(message);
    }
}
```

## 多用户的上下文隔离和持久化的解决方案

langchain4j提供多用户的上下文隔离和持久化方案。上下文隔离使用langchain4j提供的 **`MessageWindowChatMemory`** 。它采用滑动窗口的方式,保留最新的N条消息,并淘汰旧消息。同时使用 **`ChatMemoryProvider`** 实现多用户的上下文隔离

本项目的用户上下文的持久化采用Redis。、

具体实现

```java
// 上下文隔离
@Bean
    public ChatMemoryProvider chatMemory(){
        return  memoryId -> MessageWindowChatMemory.builder()
                .id(memoryId)// 指定ID
                .maxMessages(10) // 保存10条上下文消息
                .chatMemoryStore(store) // 上下文持久化
                .build();
    }
```



## 并发问题的解决方案

### 初步解决方案

通过查阅网上资料，ollama的自身支持多模型加载和并发请求。

可以通过调整环境变量初步解决并发问题

- 最多同时加载到内存中模型的数量：**`OLLAMA_MAXLoaded_MODELS`**
- 请求处理的并发数量： **`OLLAMA_NUM_PARALLEL`**

但是受限于算力有限，假设前端传过来的请求数过大，可能会导致后端服务应付不过来了。

### 目前的解决方案

经过和师兄和老师的研讨，初次迭代考虑采用限流算法实现”削峰填谷“的作用。目前常用的限流算法有以下两种

- **令牌桶算法** ：维护一个固定容量的令牌桶，每秒钟会向令牌桶中放入一定数量的令牌。当有请求到来时，如果令牌桶中有足够的令牌，则请求被允许通过并从令牌桶中消耗一个令牌，否则请求被丢弃
- **漏桶算法** ：对于每个到来的请求，都将其加入到漏桶中，并检查漏桶中当前的水量是否超过了漏桶的容量。如果超过了容量，就将多余的数据包丢弃。如果漏桶中还有水，就以一定的速率从桶底输出请求，保证输出的速率不超过预设的速率，从而达到限流的目的。

经过权衡之后决定选择令牌桶算法

令牌桶算法使用基于Guava的实现，Guava提供了限速器，支持设置预热时间和每秒产生的令牌数。在过滤器中实现令牌桶算法的主要逻辑

