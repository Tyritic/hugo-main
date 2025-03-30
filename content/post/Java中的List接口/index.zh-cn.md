---
date : '2024-11-11T15:34:52+08:00'
draft : false
title : 'Java中的List接口'
image : ""
categories : ["Java集合"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## List集合的定义

在 Java 中，**`List`** 是一个接口，继承自 **`Collection`** 接口，表示一个有序的元素集合。**`List`** 集合中的元素是按插入顺序排列的，允许元素重复。

## List集合的特点

- 集合中允许重复元素
- 集合中的元素是按插入顺序排列
- 集合支持动态扩容
- 只能存储引用数据类型，基本数据类型要转化成包装类

## List接口的实现类

- **`ArrayList`**：基于动态数组实现，支持快速随机访问，插入和删除操作效率相对较低，适用于查询频繁的场景。
- **`LinkedList`**：基于双向链表实现，支持快速插入和删除，查询效率较低，适用于频繁修改的场景。
- **`Vector`**：与 **`ArrayList`** 类似，但它是同步的，线程安全的，适用于多线程并发的场景（但现在不常用）。
- **`Stack`**：继承自 **`Vector`**，实现了栈的功能，支持后进先出（LIFO）操作。

## List接口的常用方法

### 增加元素

- **`boolean add(E e)`**：将指定的元素添加到列表的末尾
- **`void add(int index, E element)`**：将指定的元素插入到列表的指定位置
- **`boolean addAll(Collection<? extends E> c)`**：将指定集合中的所有元素添加到当前列表的末尾
- **`boolean addAll(int index, Collection<? extends E> c)`**：将指定集合中的所有元素插入到当前列表的指定位置。

### 删除元素

- **`void clear()`**：删除全部元素
- **`E remove(int index)`**：删除列表中指定位置的元素
- **`boolean remove(Object o)`**：删除列表中第一次出现的指定元素。如果列表中没有该元素，则不做任何操作。
- **`boolean removeAll(Collection<?> c)`**：删除当前列表中所有与指定集合中的元素相同的元素
- **`void removeRange(int from,int to)`**：删除索引[from，to）之间的元素

### 判断元素

- **`boolean contains(Object o)`**：判断列表中是否包含指定的元素
- **`boolean containsAll(Collection<?> c)`**：判断列表是否包含指定集合中的所有元素

### 修改元素

- **`E set(int index, E element)`**：用指定的元素替换列表中指定位置的元素

### 访问元素

- **`E get(int index)`**：返回指定位置的元素
- **`int indexOf(Object o)`**：返回指定元素在列表中的第一次出现位置的索引。如果列表中没有该元素，则返回 **`-1`**
- **`int lastIndexOf(Object o)`**：返回指定元素在列表中的最后一次出现位置的索引。如果列表中没有该元素，则返回 **`-1`**

### 获取大小

- **`int size()`**：返回列表中元素的数量
- **`boolean isEmpty()`**：判断列表是否为空