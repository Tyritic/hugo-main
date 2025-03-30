---
date : '2024-11-15T23:03:07+08:00'
draft : false
title : 'Java中的StringBuffer'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## StringBuffer的定义

`StringBuffer` 是 Java 中用于创建可变字符串的类，提供了一个与 `StringBuilder` 类似的功能。它们都用于处理可变的字符串数据，不同之处在于 `StringBuffer` 是线程安全的，而 `StringBuilder` 不是。

## StringBuffer 的特点

- **可变字符串：** `StringBuffer` 提供了修改字符串内容的方法，避免了每次修改字符串时创建新的 `String` 对象，从而提高了性能。
- **线程安全：** `StringBuffer` 是线程安全的，意味着它可以在多个线程间安全地共享和操作。`StringBuffer` 中的方法通常都被同步（使用 `synchronized`），确保多线程环境下的线程安全。
- **效率较低：** 由于线程安全的特性，`StringBuffer` 的性能通常比 `StringBuilder` 略差，因为 `StringBuffer` 的方法被加锁，而 `StringBuffer` 的方法没有锁定。

## StringBuffer的构造函数

- `public StringBuffer()` ：默认构造，初始化容量为 16
- `public StringBuffer(String str)` ：以指定字符串初始化
- `public StringBuffer(int capacity)`：以指定初始容量初始化

## StringBuffer的常见操作

### 追加数据

- `public StringBuffer append(String str)`：将字符串`str`追加到 `StringBuffer` 对象的末尾。
- `public StringBuffer append(int i)`：将 `i` 转换为字符串并追加到 `StringBuffer` 对象的末尾。
- `public StringBuffer append(char c)`：将 `c` 转换为字符串并追加到 `StringBuffer` 对象的末尾。

**作用**

- `append()` 方法用于在 `StringBuffer` 对象的末尾追加指定的内容。
- 支持多种类型的参数，包括 `String`、`int`、`char` 等。调用时会将传入的内容转换为字符串后附加到原字符串的后面。

**示例**

```java
StringBuffer sb = new StringBuffer("Hello");
sb.append(" World").append(123).append('!');
System.out.println(sb); // 输出：Hello World123!
```

### 插入内容

- `public StringBuffer insert(int offset, String str)`
- `public StringBuffer insert(int offset, int i)`
- `public StringBuffer insert(int offset, char c)`

**作用**

- `insert()` 方法将指定的内容插入到 `StringBuffer` 对象中指定位置。
- `offset` 参数表示插入的位置，内容会从这个位置开始插入。

**示例**

```java
StringBuffer sb = new StringBuffer("Hello!");
sb.insert(5, " Java");
System.out.println(sb); // 输出：Hello Java!
```

### 删除内容

- `public StringBuffer delete(int start, int end)`

**作用：**

- `delete()` 方法删除 `StringBuffer` 中从 `start` 到 `end-1` 位置的字符。
- 删除的是一个字符范围，`start` 是包含的起始位置，`end` 是不包含的结束位置。

**示例：**

```java
StringBuffer sb = new StringBuffer("Hello Java!");
sb.delete(5, 10);
System.out.println(sb); // 输出：Hello!
```

### 替换子串

- `public StringBuffer replace(int start, int end, String str)`

**作用：**

- `replace()` 方法将指定范围`（start，end-1）`内的字符替换为给定的字符串。
- `start` 到 `end` 范围的字符被替换为 `str`。

**示例：**

```java
StringBuffer sb = new StringBuffer("Hello World!");
sb.replace(6, 11, "Java");
System.out.println(sb); // 输出：Hello Java!
```

### 反转字符串

- `public StringBuffer reverse()`

**作用：**

- `reverse()` 方法将 `StringBuffer` 中的字符序列反转。
- 例如，`Hello` 会变成 `olleH`。

**示例：**

```java
StringBuffer sb = new StringBuffer("Hello");
sb.reverse();
System.out.println(sb); // 输出：olleH
```

### 获取属性

- `public int length()`：获取字符串长度
- `public int capacity()`：获取容量

### 操作指定位置的字符

- `public char charAt(int index)`：获取指定位置的字符
- `public void setCharAt(int index, char ch)`：设置指定位置的字符

### 截取子串

- `public String substring(int start)`
- `public String substring(int start, int end)`

**作用：**

- `substring()` 方法返回 `StringBuffer` 中指定位置的子字符串。
- 如果只有 `start` 参数，则返回从 `start` 到最后的子字符串。
- 如果提供了 `start` 和 `end`，则返回该范围内的子字符串。

**示例**

```java
StringBuffer sb = new StringBuffer("Hello World");
System.out.println(sb.substring(6));      // 输出：World
System.out.println(sb.substring(0, 5));   // 输出：Hello
```

### 查找子串

- `public int indexOf(String str)`
- `public int indexOf(String str, int fromIndex)`

**作用：**

- `indexOf()` 方法返回指定子字符串首次出现的位置。如果子字符串不存在，则返回 `-1`。
- 可以通过 `fromIndex` 参数指定从哪个位置开始查找。

**示例**

```java
StringBuffer sb = new StringBuffer("Hello World");
System.out.println(sb.indexOf("World"));      // 输出：6
System.out.println(sb.indexOf("o", 5));       // 输出：7
```

### 总体使用

```java
public class StringBufferExample {
    public static void main(String[] args) {
        // 创建一个 StringBuffer 对象
        StringBuffer sb = new StringBuffer("Hello");
        
        // 使用 append() 方法追加内容
        sb.append(" World!");
        System.out.println(sb); // 输出：Hello World!
        
        // 使用 insert() 方法插入内容
        sb.insert(5, ",");
        System.out.println(sb); // 输出：Hello, World!
        
        // 使用 delete() 方法删除内容
        sb.delete(5, 6); // 删除从索引 5 到 6 的字符
        System.out.println(sb); // 输出：Hello World!
        
        // 使用 reverse() 方法反转字符串
        sb.reverse();
        System.out.println(sb); // 输出：!dlroW olleH
        
        // 将 StringBuffer 转换为 String
        String str = sb.toString();
        System.out.println(str); // 输出：!dlroW olleH
        
        // 获取 StringBuffer 的长度
        System.out.println(sb.length()); // 输出：13
        
        // 获取 StringBuffer 的容量
        System.out.println(sb.capacity()); // 输出：27 (因为默认容量是16，加上追加的内容后，容量自动扩展)
    }
}
```

## String，StringBuffer，StringBuilder的区别（面试题）

**String**

- **不可变**：`String` 是不可变类，字符串一旦创建，其内容无法更改。每次对 `String` 进行修改操作（如拼接、截取等），都会创建新的 `String` 对象。
- **适合场景**：`String` 适用于字符串内容不会频繁变化的场景，例如少量的字符串拼接操作或字符串常量。

**StringBuffer**

- **可变**：`StringBuffer` 是可变的，可以进行字符串的追加、删除、插入等操作。
- **线程安全**：`StringBuffer` 是线程安全的，内部使用了 `synchronized` 关键字来保证多线程环境下的安全性。
- **适合场景**：`StringBuffer` 适用于在多线程环境中需要频繁修改字符串的场景。

**StringBuilder**

- **可变**：`StringBuilder` 也是可变的，提供了与 `StringBuffer` 类似的操作接口。
- **非线程安全**：`StringBuilder` 不保证线程安全，性能比 `StringBuffer` 更高。
- **适合场景**：`StringBuilder` 适用于单线程环境中需要大量修改字符串的场景，如高频拼接操作。
