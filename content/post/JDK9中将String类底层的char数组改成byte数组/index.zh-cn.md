---
date : '2025-01-14T22:32:10+08:00'
draft : false
title : 'JDK9中将String类底层的char数组改成byte数组'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "为什么JDK9中将String类底层的char数组改成byte数组"
math : true
---

## 回答重点

主要是为了**节省内存空间，提高内存利用率**。

在 JDK 9 之前，String 类是基于 `char[]` 实现的，内部采用 UTF-16 编码，每个字符占用两个字节。但是，如果当前的字符仅需一个字节的空间，这就造成了浪费。例如一些 `Latin-1` 字符用一个字节即可表示。

因此 JDK 9 做了优化采用 `byte[]` 数组来实现，ASCII 字符串（单字节字符）通过 `byte[]` 存储，仅需 1 字节，减小了内存占用。

并引入了 coder 变量来标识编码方式（Latin-1 或 UTF-16）。如果字符串中只包含 Latin-1 范围内的字符（如 ASCII），则使用单字节编码，否则使用 UTF-16。这种机制在保持兼容性的同时，又减少了内存占用。
