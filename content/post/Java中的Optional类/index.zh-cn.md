---
date : '2025-01-16T20:56:03+08:00'
draft : false
title : 'Java中的Optional类'
image : ""
categories : ["Java"]
tags : ["Java基础"]
description : "JDK 8的新特性"
---

## 📦 `Optional`类的定义

`Optional` 类是 Java 8 引入的一个容器类，用来解决可能出现的 **NullPointerException** 问题。它表示一个值可能存在也可能不存在，提供了一种优雅的方式来避免显式的 `null` 检查。

---

## 💎 核心思想

- **避免显式使用 `null`**：
  使用 `Optional` 代替直接返回 `null`，从而避免潜在的空指针异常。
- **增强代码可读性**：
  提供清晰的 API，表示值的存在或缺失，并能安全处理缺失的值。
- **函数式编程支持**：
  支持链式调用和流式操作，更适合在函数式编程中使用

---

## 🎯 创建对象方法

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

---

## ✅ 判断值是否存在

- **`isPresent()`**：值存在返回 `true`，否则返回 `false`。
- **`isEmpty()`**：值不存在返回 `true`（Java 11 引入）。

---

## 💡 获取值

**`get()`**：返回值，如果值不存在会抛出 `NoSuchElementException`。

```java
String name = nameOpt.get();
```

**`orElse(defaultValue)`**：值存在则返回值，否则返回默认值。

```java
String name = nullableOpt.orElse("Default Name");
```

---

## 🔧 操作值

### 💫 条件执行

- **`ifPresent(Consumer<? super T>)`**：值存在时执行给定的动作。

```java
nameOpt.ifPresent(name -> System.out.println("Name: " + name));
```

- **`ifPresentOrElse(Consumer<? super T>, Runnable)`**：值存在执行第一个操作，否则执行第二个操作（Java 9 引入）。

```java
nameOpt.ifPresentOrElse(
  name -> System.out.println("Name: " + name),
  () -> System.out.println("Name is empty")
);
```

### 🔄 映射与转换

- **`map(Function<? super T, ? extends U>)`**：值存在时对值进行映射操作，返回新的 `Optional`。

```java
Optional<Integer> lengthOpt = nameOpt.map(String::length);
```

- **`flatMap(Function<? super T, ? extends Optional<? extends U>>)`**：值存在时对值进行映射操作，返回 `Optional`（避免嵌套）。

```java
Optional<String> upperOpt = nameOpt.flatMap(name -> 
  Optional.of(name.toUpperCase())
);
```

### 🛡️ 过滤与默认值

- **`filter(Predicate<? super T>)`**：值存在且满足条件则返回原 `Optional`，否则返回空 `Optional`。

```java
Optional<String> validName = nameOpt.filter(name -> name.length() > 3);
```

- **`orElseThrow()`**：值存在返回值，否则抛出 `NoSuchElementException`（Java 10 引入）。

```java
String name = nameOpt.orElseThrow();
```

- **`orElseThrow(Supplier<? extends X>)`**：值存在返回值，否则抛出自定义异常。

```java
String name = nameOpt.orElseThrow(() -> new IllegalArgumentException("Name is required"));
```

---

## 📝 实践建议

- 优先使用 `orElse(defaultValue)` 处理默认值情况
- 使用 `map()` 和 `filter()` 进行函数式操作
- 避免在业务逻辑中频繁使用 `get()`，容易引发异常
- 充分利用 `ifPresent()` 和 `ifPresentOrElse()` 进行条件处理
