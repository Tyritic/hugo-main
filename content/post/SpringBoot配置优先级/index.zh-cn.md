---
date : '2024-11-08T16:37:30+08:00'
draft : false
title : 'SpringBoot配置优先级'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发","框架原理"]
description : "SpringBoot配置方式及其优先级"
---

## 配置方式

### 文件配置

- properties文件
- yml文件
- yaml文件

### Java系统属性

#### 设置方法

1. 执行maven打包指令package

2. 执行java指令，运行jar包，在执行java命令时添加参数

3. 参数格式

   ```
   -Dxxx=xxx
   ```

   

### 命令行参数

1. 执行maven打包指令package

2. 执行java指令，运行jar包，在执行java命令时添加参数

3. 参数格式

   ```
   --xxx=xxx
   ```

   

## 配置优先级

优先级从低到高

- application.yam](忽略)
- application.yml
- application.properties
- java系统属性(-Dxxx=xxx)
- 命令行参数(--xxx=xxx)
