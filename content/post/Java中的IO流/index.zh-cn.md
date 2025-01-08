---
date : '2025-01-03T16:32:57+08:00'
draft : false
title : 'Java中的IO流'
image : ""
categories : ["互联网面试题"]
tags : ["JavaSE"]
description : "Java中的IO流"
math : true
---

## 回答重点

Java 的 I/O（输入/输出）流是用于处理输入和输出数据的类库。通过流，程序可以从各种输入源（如文件、网络）读取数据，或将数据写入目标位置（如文件、控制台）。

I/O 流分为两大类：**字节流** 和 **字符流**，分别用于处理字节级和字符级的数据：

- **字节流**：处理 8 位字节数据，适合于处理二进制文件，如图片、视频等。主要类是 `InputStream` 和 `OutputStream` 及其子类。
- **字符流**：处理 16 位字符数据，适合于处理文本文件。主要类是 `Reader` 和 `Writer` 及其子类。

## 回答重点

Java 的 I/O（输入/输出）流是用于处理输入和输出数据的类库。通过流，程序可以从各种输入源（如文件、网络）读取数据，或将数据写入目标位置（如文件、控制台）。

I/O 流分为两大类：**字节流** 和 **字符流**，分别用于处理字节级和字符级的数据：

- **字节流**：处理 8 位字节数据，适合于处理二进制文件，如图片、视频等。主要类是 `InputStream` 和 `OutputStream` 及其子类。
- **字符流**：处理 16 位字符数据，适合于处理文本文件。主要类是 `Reader` 和 `Writer` 及其子类。

## 扩展知识

### 输入流与输出流

输入流（Input Stream）：用于读取数据的流。

输出流（Output Stream）：用于写入数据的流。

按照处理的数据类型，基于这两种输入输出的类型进行分类：

**字节流**（Byte Streams）：

输入流：InputStream，常用以下几个输入流：

- FileInputStream：从文件中读取字节数据。
- BufferedInputStream：为输入流提供缓冲功能，提高读取性能。
- DataInputStream：读取基本数据类型的数据。

输出流：OutputStream，常用以下几个输出流：

- FileOutputStream：将字节数据写入文件。
- BufferedOutputStream：为输出流提供缓冲功能，提高写入性能。
- DataOutputStream：写入基本数据类型的数据。

**字符流**（Character Streams）：

输入流：Reader，常用以下几个输入流：

- FileReader：从文件中读取字符数据。
- BufferedReader：为字符输入流提供缓冲功能，提高读取性能。
- InputStreamReader：将字节流转换为字符流。

输出流：Writer，常用以下几个输出流：

- FileWriter：将字符数据写入文件。
- BufferedWriter：为字符输出流提供缓冲功能，提高写入性能。
- OutputStreamWriter：将字符流转换为字节流。

### **缓冲流**：

缓冲流是对基础流的包装，可以显著提高 I/O 性能。常见的缓冲流有 `BufferedInputStream`、`BufferedOutputStream`、`BufferedReader` 和 `BufferedWriter`，它们通过**内部缓冲区减少实际 I/O 操作的次数**。

在处理大文件或频繁 I/O 操作时，使用缓冲流可以有效提高性能。