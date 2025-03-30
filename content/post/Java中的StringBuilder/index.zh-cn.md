---
date : '2024-11-15T21:13:12+08:00'
draft : false
title : 'Java中的StringBuilder'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## StringBuilder的定义

`StringBuilder` 是 Java 中的一个 **可变字符序列类**，位于 `java.lang` 包中。它用于创建和操作可变的字符串（字符序列），与 `String` 不同，`StringBuilder` 的内容是 **可变的**，不会像 `String` 那样在每次修改时创建新的对象，从而提高了性能，尤其在需要频繁修改字符串时非常有用。

## StringBuilder的特点

- **可变性**：
  `StringBuilder` 维护一个可变的`char`数组，操作时直接修改这个数组，不会生成新的对象。
- **效率高**：
  在进行字符串拼接、插入、删除等操作时，相比 `String` 创建大量临时对象，`StringBuilder` 只需在原对象上进行操作，因此效率更高。
- **线程不安全**：
  与 `StringBuffer`（线程安全版本）不同，`StringBuilder` 不是线程安全的，但在单线程环境下效率更高。

## StringBuilder的构造方法

- **`StringBuilder()`**

  **无参构造函数**，创建一个初始容量为 **16** 的空 `StringBuilder` 对象。

- **`StringBuilder(int capacity)`**

  **指定初始容量的构造函数**，创建一个具有指定初始容量的 `StringBuilder` 对象，如果在追加字符时超出指定容量，`StringBuilder` 会自动扩容，扩容规则为：

  > 新容量 = (旧容量 * 2) + 2

- **`StringBuilder(String str)`**

  **以指定字符串内容为初始值的构造函数**，创建一个包含给定字符串内容的 `StringBuilder` 对象，同时容量为 `str.length() + 16`。

- **`StringBuilder(CharSequence seq)`**

  **以 `CharSequence` 接口实现类为初始内容的构造函数**，创建一个包含指定字符序列的 `StringBuilder` 对象。

**示例代码**

```java
public class Main {
    public static void main(String[] args) {
        // 无参构造
        StringBuilder sb1 = new StringBuilder();
        System.out.println("sb1 的初始容量：" + sb1.capacity()); // 输出：16

        // 指定容量构造
        StringBuilder sb2 = new StringBuilder(30);
        System.out.println("sb2 的初始容量：" + sb2.capacity()); // 输出：30

        // 以字符串为初始值的构造
        StringBuilder sb3 = new StringBuilder("Hello");
        System.out.println("sb3 的初始内容：" + sb3.toString()); // 输出：Hello
        System.out.println("sb3 的初始容量：" + sb3.capacity()); // 输出：21（5 + 16）

        // 以 CharSequence 为初始值的构造
        CharSequence seq = "World";
        StringBuilder sb4 = new StringBuilder(seq);
        System.out.println("sb4 的初始内容：" + sb4.toString()); // 输出：World
    }
}

```

## StringBuilder的常见操作

### 追加数据

- `public StringBuilder append(String str)`：将字符串`str`追加到 `StringBuilder` 对象的末尾。
- `public StringBuilder append(int i)`：将 `i` 转换为字符串并追加到 `StringBuilder` 对象的末尾。
- `public StringBuilder append(char c)`：将 `c` 转换为字符串并追加到 `StringBuilder` 对象的末尾。

**作用**

- `append()` 方法用于在 `StringBuilder` 对象的末尾追加指定的内容。
- 支持多种类型的参数，包括 `String`、`int`、`char` 等。调用时会将传入的内容转换为字符串后附加到原字符串的后面。

**示例**

```java
StringBuilder sb = new StringBuilder("Hello");
sb.append(" World").append(123).append('!');
System.out.println(sb); // 输出：Hello World123!
```

### 插入内容

- `public StringBuilder insert(int offset, String str)`
- `public StringBuilder insert(int offset, int i)`
- `public StringBuilder insert(int offset, char c)`

**作用**

- `insert()` 方法将指定的内容插入到 `StringBuilder` 对象中指定位置。
- `offset` 参数表示插入的位置，内容会从这个位置开始插入。

**示例**

```java
StringBuilder sb = new StringBuilder("Hello!");
sb.insert(5, " Java");
System.out.println(sb); // 输出：Hello Java!
```

### 删除内容

- `public StringBuilder delete(int start, int end)`

**作用：**

- `delete()` 方法删除 `StringBuilder` 中从 `start` 到 `end-1` 位置的字符。
- 删除的是一个字符范围，`start` 是包含的起始位置，`end` 是不包含的结束位置。

**示例：**

```java
StringBuilder sb = new StringBuilder("Hello Java!");
sb.delete(5, 10);
System.out.println(sb); // 输出：Hello!
```

### 替换子串

- `public StringBuilder replace(int start, int end, String str)`

**作用：**

- `replace()` 方法将指定范围`（start，end-1）`内的字符替换为给定的字符串。
- `start` 到 `end` 范围的字符被替换为 `str`。

**示例：**

```java
StringBuilder sb = new StringBuilder("Hello World!");
sb.replace(6, 11, "Java");
System.out.println(sb); // 输出：Hello Java!
```

### 反转字符串

- `public StringBuilder reverse()`

**作用：**

- `reverse()` 方法将 `StringBuilder` 中的字符序列反转。
- 例如，`Hello` 会变成 `olleH`。

**示例：**

```java
StringBuilder sb = new StringBuilder("Hello");
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

- `substring()` 方法返回 `StringBuilder` 中指定位置的子字符串。
- 如果只有 `start` 参数，则返回从 `start` 到最后的子字符串。
- 如果提供了 `start` 和 `end`，则返回该范围内的子字符串。

**示例**

```java
StringBuilder sb = new StringBuilder("Hello World");
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
StringBuilder sb = new StringBuilder("Hello World");
System.out.println(sb.indexOf("World"));      // 输出：6
System.out.println(sb.indexOf("o", 5));       // 输出：7
```

## equals方法

`StringBuilder` 类中的 `equals()` 方法在默认情况下并不按内容比较两个 `StringBuilder` 对象，而是按 **引用** 比较，即两个 `StringBuilder` 对象是否指向相同的内存位置。

## StringBuilder的实现原理

### 大致核心实现

- 内部使用字符数组 (`char[] value`) 来存储字符序列
- 通过方法如 append()、insert() 等操作，直接修改内部的字符数组，而不会像 String 那样创建新的对象。
- 每次进行字符串操作时，如果当前容量不足，它会通过扩展数组容量来容纳新的字符，按 2 倍的容量扩展，以减少扩展次数，提高性能。

### 底层具体实现

-  `StringBuilder` 底层使用 `char` 数组 `value` 来存储字符，并且用 `count` 来记录存放的字符数
- 为了防止频繁地复制和申请内存，需要提供 `capacity` 参数来设置初始化数组的大小，这样可以减少数组的扩容次数，有效的提升效率！

### append()的具体实现

- int值转成 char 需要占数组的几位，然后计算一下现在的数组够不够放，如果不够就扩容，然后再把 int 转成 char 放进去，再更新现有的字符数。
- 扩容时调用 `Arrays.copyOf`，进行一波扩容加拷贝，扩容之后的数组容量为之前的两倍+2。

### insert()的具体实现

- 这里是把 数据 转成 `string` 
- 插入前先判断下数组长度足够，若不够就扩容。
- 移动字符，给待插入的位置腾出空间，然后往对应位置插入字符
- 最后更新 `StringBuilder` 已有的字符数

### 优化方法（JDK 11的优化）

char 数组是可以优化的，底层可以用 byte 数组+一个 coder 标志位来实现，这样更节省内存，因为 char 占用两个字节，这样对于 latin 系的字符来说，太大了，就很浪费，所以用 byte 数组，然后配备一个 coder 来标识所用的编码。
