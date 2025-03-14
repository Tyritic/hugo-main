---
date : '2025-01-05T16:02:40+08:00'
draft : false
title : '识物探趣（二）项目架构和技术选型'
image : ""
categories : ["个人项目"]
tags : [""]
description : "软著项目留档和开发过程描述"
math : true
---

## 项目总体架构

### 表现层（前端）

- Web 前端
- 移动端

### 业务逻辑层

- 建筑识别模块
  - 模块直接调用内部封装的 AI 模型接口，将识别结果传递给后续业务逻辑。
- 推荐系统模块
  - 根据建筑识别结果和用户行为数据，利用实现个性化内容推荐。
- 社交互动模块
  - 包括文章发布、评论、点赞、分享等功能，实现类似小红书的社交生态。
  - 同时支持 UGC 内容的展示与互动反馈。
- 内容管理模块
  - 管理端：为展馆的管理方提供对发布内容的管理
  - 用户端：提供对自己发布内容的管理


###  数据访问层

- 关系型数据库
  - 存储用户信息、文章、评论等结构化数据。
- 缓存系统
  - 缓存热点数据、用户会话和部分推荐结果，提升系统响应速度。
- 消息队列
  - 异步更新数据，保证主业务操作的速度

## 技术选型

### 业务逻辑层

- 总体框架
  - SpringBoot+Mybatis
- 建筑识别模块
  - yolo模型
- 推荐系统模块
  - Langchain4j进行对话管理和RAG处理
  - Ollama部署私有LLM

### 数据访问层

- 关系型数据库
  - MySQL
- 缓存系统
  - Redis作为L2级别缓存
  - Caffeine作为L1级别缓存
- 消息队列
  - Kafka

