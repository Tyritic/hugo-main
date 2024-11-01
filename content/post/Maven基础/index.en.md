---
date : '2024-11-01T15:28:45+08:00'
draft : false
title : 'Maven Basic Knowledge'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发"]
description : ""
lastmod : '2024-11-01T15:28:45+08:00'
---

## The role of Maven

- **Dependency management**:Manage dependencies quickly and easily

- **Unified project structure**:Provide a standard project structure

- **Project building**:Provides a standard way to build cross-platform projects

## The structure of the Maven project

```
Maven-name/
|--src（source code）
|	|--main（project resource）
|		|--java（java code）
|		|--resource（resource）
|	|--test（test）
|		|--java
|		|--resource
|--pom.xml（dependency management）
|--target（target file(.jar)）
```

<img src="Maven项目结构图.png" alt="Maven项目结构图" style="zoom:67%;" />

## The build process of the Maven project
