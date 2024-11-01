---
date : '2024-11-01T15:28:45+08:00'
draft : false
title : 'Maven基础'
image : "https://picsum.photos/800/600.webp?random={{ substr (md5 (.Date)) 4 8 }}"
categories : ["SpringBoot"]
tags : ["后端开发"]
description : ""
lastmod : '2024-11-01T15:28:45+08:00'
---

## Maven的作用

- 依赖管理：方便快捷地管理依赖

- 统一项目结构：提供标准的项目结构

- 项目构建：提供了标准的跨平台项目构建方式

## Maven项目的结构

```
Maven-name/
|--src（源代码）
|	|--main（项目实际资源）
|		|--java（java代码）
|		|--resource（资源文件）
|	|--test（测试代码资源）
|		|--java
|		|--resource
|--pom.xml（依赖配置文件）
|--target（打包后的jar包存放地）
```

<img src="Maven项目结构图.png" alt="Maven项目结构图" style="zoom:67%;" />

## Maven项目的构建过程
