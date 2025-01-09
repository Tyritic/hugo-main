---
date : '2024-11-02T10:46:06+08:00'
draft : false
title : 'Java程序的编译执行过程'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记的转换"
math : true
---

## 执行过程

1. 开发者编写Java源代码（ **.java** 文件）
2. 编译源代码（**.java**文件）——使用`javac`命令将源代码转化成**字节码**（**.class**文件）
3. 在虚拟机（**JVM**）上运行字节码（**.class** 文件）

## 跨平台性

Java程序具有在任意操作系统平台上运行

### 实现原理

在运行Java程序程序的操作系统上安装一个与操作系统对应的Java虚拟机

## Java的运行环境

### JVM（Java虚拟机）

Java虚拟机用于解释Java源代码，加载Java程序。针对不同的操作系统设计有不同的Java虚拟机

### JRE（Java运行时环境）

**JRE**全称**（Java Runtime Environment）**是Java运行时环境，包含了 **JVM**, Java核心类库和其他支持Java程序的文件，但是**不包含任何开发工具**

#### 组成部分

- **JVM**（Java Virtual Machine）：执行由源代码编译后得到的Java字节码，提供了Java程序的运行环境
- 核心类库：标准的类库（java.lang,java.utils）供Java程序使用
- 其他文件：配置文件，库文件，支持JVM的运行

### JDK（Java开发包）

**JDK**全称 **（Java Development Kit）**是一组独立程序构成的集合，是用于开发Java 程序的完整开发环境，**它包含了JRE**，以及用于开发、调试和监控 Java 应用程序的工具。

#### 组成部分

- **JRE**：**JDK**包含了完整的JRE，可以运行java程序
- 开发工具：包含编译器（**javac**），打包工具（**jar**）
- 附加库和文件：支持开发，文档生成

#### 常见开发工具

- **javac** ：Java 编译器，用于将 Java 源代码（.java 文件）编译成字节码（.class 文件）。
- **java** ：Java 应用程序启动器，用于运行 Java 应用程序。
- javadoc：文档生成器，用于从 Java 源代码中提取注释并生成 HTML 格式的 API 文档。
- **jar** ：归档工具，用于创建和管理 JAR（**Java Archive**）文件。
- **jdb**：Java 调试器，用于调试 Java 程序。
- jps：Java 进程状态工具，用于列出当前所有的 Java 进程。
- jstat：JVM 统计监视工具，用于监视 JVM 统计信息。
- jstatd：JVM 统计监视守护进程，用于在远程监视 JVM 统计信息。
- **jmap**：内存映射工具，用于生成堆转储（**heap dump**）、查看内存使用情况。
- **jhat**：堆分析工具，用于分析堆转储文件。
- **jstack**：线程栈追踪工具，用于打印 Java 线程的栈追踪信息。
- javap：类文件反汇编器，用于反汇编和查看 Java 类文件。
- jdeps：Java 类依赖分析工具，用于分析类文件或 JAR 文件的依赖关系

### 相互关系

- JDK
  - JRE
    - JVM
    - 核心类库
  - 开发工具