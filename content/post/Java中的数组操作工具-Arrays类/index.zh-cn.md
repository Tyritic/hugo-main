---
date : '2025-01-15T17:32:46+08:00'
draft : false
title : 'Java中的数组操作工具 Arrays类'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

Arrays类是用于对数组进行操作的工具类

## 常见操作

### 排序

- `static void sort(int[] a)` 
- `static <T> void sort(T[] a, Comparator<? super T> c)` // 使用 Comparator 自定义排序

#### 示例

```java
int[] arr = {5, 2, 8, 1, 3};
Arrays.sort(arr);
System.out.println(Arrays.toString(arr)); // 输出：[1, 2, 3, 5, 8]

String[] strs = {"apple", "banana", "pear"};
Arrays.sort(strs, (s1, s2) -> s2.compareTo(s1)); // 按降序排序
System.out.println(Arrays.toString(strs)); // 输出：[pear, banana, apple]

```

###  二分查找

在已排序的数组中使用二分查找指定元素的索引。

- `static int binarySearch(int[] a, int key)`
- `static <T> int binarySearch(T[] a, T key, Comparator<? super T> c)`

#### 示例

```java
int[] arr = {1, 2, 3, 5, 8};
int index = Arrays.binarySearch(arr, 5);
System.out.println("元素 5 的索引：" + index); // 输出：元素 5 的索引：3
```

### 判断是否相等

判断两个数组是否相等（长度相同且对应元素相等）。

- `static boolean equals(int[] a, int[] a2)`
- `static <T> boolean equals(T[] a, T[] a2)`

#### 示例

```java
int[] arr1 = {1, 2, 3};
int[] arr2 = {1, 2, 3};
int[] arr3 = {1, 2, 4};
System.out.println(Arrays.equals(arr1, arr2)); // 输出：true
System.out.println(Arrays.equals(arr1, arr3)); // 输出：false
```

判断两个多维数组是否相等

- `static boolean deepEquals(Object[] a1, Object[] a2)`

### 批量赋值

将数组的所有元素赋值为指定值

- `static void fill(int[] a, int val)`
- `static <T> void fill(T[] a, T val)`

#### 示例

```java
int[] arr = new int[5];
Arrays.fill(arr, 9);
System.out.println(Arrays.toString(arr)); // 输出：[9, 9, 9, 9, 9]
```

### 复制数组

将指定数组复制到新的数组，返回一个新数组。

- `static int[] copyOf(int[] original, int newLength)`
- `static <T> T[] copyOf(T[] original, int newLength)`

#### 示例

```java
int[] arr = {1, 2, 3};
int[] newArr = Arrays.copyOf(arr, 5);
System.out.println(Arrays.toString(newArr)); // 输出：[1, 2, 3, 0, 0]
```



将指定数组的某个范围复制到新的数组。

- `static int[] copyOfRange(int[] original, int from, int to)`
- `static <T> T[] copyOfRange(T[] original, int from, int to)`

**示例**

```java
int[] arr = {1, 2, 3, 4, 5};
int[] newArr = Arrays.copyOfRange(arr, 1, 4); // [from, to)
System.out.println(Arrays.toString(newArr)); // 输出：[2, 3, 4]
```

### 数组转换为集合

- `static <T> List<T> asList(T... a)`

**示例**

```java
String[] strs = {"apple", "banana", "pear"};
List<String> list = Arrays.asList(strs);
System.out.println(list); // 输出：[apple, banana, pear]
```

