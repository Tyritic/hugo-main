---
date : '2025-01-02T12:10:06+08:00'
draft : false
title : 'JDK和JRE的关系'
image : ""
categories : ["互联网面试题"]
tags : ["JavaSE"]
description : "Java运行的底层环境和工具包"
math : true
---

## JRE

**JRE**全称**（Java Runtime Environment）**是Java运行时环境，包含了 **JVM**, Java核心类库和其他支持Java程序的文件

### 组成部分

- **JVM**（Java Virtual Machine）：执行由源代码编译后得到的Java字节码，提供了Java程序的运行环境
- 核心类库：标准的类库（java.lang,java.utils）供Java程序使用
- 其他文件：配置文件，库文件，支持JVM的运行

## JDK

**JDK**全称 **（Java Development Kit）** 可以视为 JRE 的超集，是用于开发Java 程序的完整开发环境，**它包含了JRE**，以及用于开发、调试和监控 Java 应用程序的工具。

### 组成部分

- **JRE**：**JDK**包含了完整的JRE，可以运行java程序
- 开发工具：包含编译器（**javac**），打包工具（**jar**）
- 附加库和文件：支持开发，文档生成

## 拓展工具

- javac：Java 编译器，用于将 Java 源代码（.java 文件）编译成字节码（.class 文件）。
- java：Java 应用程序启动器，用于运行 Java 应用程序。
- javadoc：文档生成器，用于从 Java 源代码中提取注释并生成 HTML 格式的 API 文档。
- jar：归档工具，用于创建和管理 JAR（**Java Archive**）文件。
- **jdb**：Java 调试器，用于调试 Java 程序。
- jps：Java 进程状态工具，用于列出当前所有的 Java 进程。
- jstat：JVM 统计监视工具，用于监视 JVM 统计信息。
- jstatd：JVM 统计监视守护进程，用于在远程监视 JVM 统计信息。
- **jmap**：内存映射工具，用于生成堆转储（**heap dump**）、查看内存使用情况。
- **jhat**：堆分析工具，用于分析堆转储文件。
- **jstack**：线程栈追踪工具，用于打印 Java 线程的栈追踪信息。
- javap：类文件反汇编器，用于反汇编和查看 Java 类文件。
- jdeps：Java 类依赖分析工具，用于分析类文件或 JAR 文件的依赖关系