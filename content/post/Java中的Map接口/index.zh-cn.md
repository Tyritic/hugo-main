---
date : '2024-11-26T10:44:24+08:00'
draft : false
title : 'Java中的Map接口'
image : ""
categories : ["Java集合","互联网面试题"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## Map接口的定义

`Map` 接口是 Java 集合框架中的一部分，用于存储键值对（`key-value`）的映射关系。`Map` 中的键是唯一的，而值可以重复。

## Map集合的特点

- **键值对存储**：
  - 每个元素由一个键（`key`）和一个值（`value`）组成。
  - 键必须唯一，但值可以重复。
- **键的唯一性**：
  - 键的唯一性是通过调用键的 `hashCode()` 和 `equals()` 方法来保证的。
- **允许的值**：
  - 键和值都可以为 null，但实现类的行为可能不同：
    - `HashMap`：允许一个 `null` 键和多个 `null` 值。
    - `TreeMap`：不允许 `null` 键。
    - `Hashtable`：不允许 `null` 键或 `null` 值。
- **无序或有序**：
  - `HashMap` 是无序的。
  - `LinkedHashMap` 按插入顺序或访问顺序存储。
  - `TreeMap` 按键的自然顺序或自定义排序存储。
- **线程安全性**：
  - `HashMap` 和 `TreeMap` 是非线程安全的。
  - `Hashtable` 和 `ConcurrentHashMap` 是线程安全的。

## Map接口的实现类

- **`HashMap`**：
  - 基于哈希表实现，允许一个 `null` 键和多个 `null` 值。
  - 无序。
- **`LinkedHashMap`**：
  - 基于哈希表和双向链表，维护插入顺序或访问顺序。
- **`TreeMap`**：
  - 基于红黑树实现，按自然顺序或自定义比较器排序键。
- **`Hashtable`**：
  - 线程安全，但性能较差，不允许 `null` 键或值。
- **`ConcurrentHashMap`**：
  - 线程安全，支持高并发。

## Map 接口常用方法

### 添加键值对

```java
V put(K key, V value)
```

- 添加或更新键值对。如果键已存在，返回旧值；否则返回 `null`。

```java
default V putIfAbsent(K key, V value)
```

- 如果键不存在，添加键值对。

### 获取值

```java
V get(Object key)
```

- 根据键获取对应的值。如果键不存在，返回 `null`

```java
default V getOrDefault(Object key, V defaultValue)
```

- 如果键存在，返回对应的值；否则返回 `defaultValue`。

### 删除键值对

```java
V remove(Object key)
```

- 移除指定键的键值对，返回被移除的值。如果键不存在，返回 `null`。

```java
void clear()
```

- 清空所有键值对。

```java
default boolean remove(Object key, Object value)
```

- 如果键存在且值匹配，则移除该键值对。

### 检查键值对

```java
boolean containsKey(Object key)
```

- 检查是否包含指定的键。

```java
boolean containsValue(Object value)
```

- 检查是否包含指定的值。

### 替换键值对

```java
default boolean replace(K key, V oldValue, V newValue)
```

- 如果键的当前值等于 `oldValue`，则替换为 `newValue`。

```java
default V replace(K key, V value)
```

- 替换键对应的值（如果键存在）。

### 集合视图

```java
Set<Map.Entry<K, V>> entrySet()
```

- 返回所有键值对的集合。

```java
Collection<V> values()
```

- 返回所有值的集合。

```java
Set<K> keySet()
```

- 返回所有键的集合。