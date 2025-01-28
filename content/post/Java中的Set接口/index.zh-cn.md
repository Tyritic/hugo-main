---
date : '2024-11-25T10:01:22+08:00'
draft : false
title : 'Java中的Set接口'
image : ""
categories : ["Java集合","互联网面试题"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## Set接口的定义

**`Set`** 是 Java 集合框架中的一个接口，位于 **`java.util`** 包中，表示一个**不包含重复元素**的集合。

## Set集合的特点

- **无重复元素**：
  - **`Set`** 不允许存储重复的元素。
  - 元素的唯一性是通过 **`equals()`** 方法来判断的。
- **无顺序保证**：
  - **`Set` 本身并不保证元素的顺序**。
  - 具体的实现类可能会对顺序有不同的处理，例如：
    - **`HashSet`**：无序。
    - **`LinkedHashSet`**：按插入顺序。
    - **`TreeSet`**：自然顺序或自定义排序。
- **允许存储 null**：
  - 大多数 **`Set`** 集合实现允许一个 **`null`** 元素（例如，`HashSet`）。
  - **`TreeSet`** 不允许存储 **`null`**，因为排序比较时会抛出 **`NullPointerException`**。
- **线程安全**：
  - **`Set`** 接口的实现类（如 **`HashSet`**）不是线程安全的。
  - 可以使用 **`Collections.synchronizedSet()`** 创建线程安全的 **`Set`**。

## Set接口的实现类

- **`HashSet`**：基于哈希表实现，无序，不保证顺序
- **`LinkedHashSet`**：基于哈希表和链表实现，按插入顺序存储。
- **`TreeSet`**：基于红黑树实现，按自然顺序或自定义排序存储
- **`ConcurrentSkipListSet`**：线程安全的 `Set`，按自然顺序或自定义排序存储，基于跳表实现

## Set接口的常用方法

### 添加元素

- **`boolean add(E e)`**：向集合中添加一个元素，如果已存在该元素，则返回 **`false`**。
- **`boolean addAll(Collection<? extends E> c)`**：将指定集合中的所有元素添加到当前集合

### 删除元素

- **`void clear()`**：清空集合中的所有元素
- **`boolean remove(Object o)`**：从集合中移除指定的元素

### 查询元素

- **`boolean contains(Object o)`**：判断集合中是否包含指定的元素

### 获取大小

- **`int size()`**：返回集合中的元素个数
- **`boolean isEmpty()`**：判空