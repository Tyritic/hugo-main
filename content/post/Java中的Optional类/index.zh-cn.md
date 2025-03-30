---
date : '2025-01-16T20:56:03+08:00'
draft : false
title : 'Java中的Optional类'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "JDK 8的新特性"
math : true
---

## `Optional`类的定义

`Optional` 类是 Java 8 引入的一个容器类，用来解决可能出现的 **NullPointerException** 问题。它表示一个值可能存在也可能不存在，提供了一种优雅的方式来避免显式的 `null` 检查。

## 核心思想

- **避免显式使用 `null`**：
  使用 `Optional` 代替直接返回 `null`，从而避免潜在的空指针异常。
- **增强代码可读性**：
  提供清晰的 API，表示值的存在或缺失，并能安全处理缺失的值。
- **函数式编程支持**：
  支持链式调用和流式操作，更适合在函数式编程中使用

## 创建对象方法

- **`Optional.empty()`**：创建一个空的 `Optional` 对象。

```java
Optional<String> emptyOpt = Optional.empty();
```

- **`Optional.of(value)`**：根据非空值创建一个 `Optional` 对象。

```java
Optional<String> nameOpt = Optional.of("John");
```

**注意**：传入 `null` 值会抛出 `NullPointerException`。

- **`Optional.ofNullable(value)`**：根据值创建 `Optional`，值可以是 `null`。

```java
Optional<String> nullableOpt = Optional.ofNullable(null);
```

## 判断值是否存在

- **`isPresent()`**：值存在返回 `true`，否则返回 `false`。
- **`isEmpty()`**：值不存在返回 `true`（Java 11 引入）。

## 获取值

**`get()`**：返回值，如果值不存在会抛出 `NoSuchElementException`。

```java
String name = nameOpt.get();
```

**`orElse(defaultValue)`**：值存在则返回值，否则返回默认值。

```java
String name = nullableOpt.orElse("Default Name");
```

## 操作值

- **`ifPresent(Consumer<? super T>)`**：值存在时执行给定的动作。

- **`map(Function<? super T, ? extends U>)`**：值存在时对值进行映射操作。
