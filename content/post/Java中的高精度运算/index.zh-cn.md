---
date : '2024-11-06T23:18:11+08:00'
draft : false
title : 'Java中的高精度运算'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## BigInteger类和BigDecimal类

BigInteger类支持任意精度的整数，表示任何大小的整数

BigDecimal类支持任意长度的小数

BigInteger类和BigDecimal都是不可变类，一旦创建其值无法更改，只要产生计算操作就会产生新的对象

## BigInteger创建方法

### 通过有参构造器

- `BigInteger(String val)`
- `BigInteger(byte[] val)`

### 通过valueOf()静态方法

`BigInteger.valueOf(long val)`

```java
import java.math.BigInteger;

public class BigIntegerExample {
    public static void main(String[] args) {
        // 从 long 值创建 BigInteger 对象
        BigInteger bigInt2 = BigInteger.valueOf(123456789L);

        System.out.println(bigInt2);  // 输出：123456789
    }
}

```

## BigDecimal创建方法

### 通过有参构造器

| 类               | 创建方式                     | 示例                           | 注意事项                           |
| ---------------- | ---------------------------- | ------------------------------ | ---------------------------------- |
| **`BigDecimal`** | `new BigDecimal(String val)` | `new BigDecimal("123.456789")` | 推荐通过字符串创建，精度不会丢失。 |
|                  | `new BigDecimal(double val)` | `new BigDecimal(123.456)`      | 精度可能丢失，尽量避免使用。       |
|                  | `new BigDecimal(long val)`   | `new BigDecimal(123)`          | 使用 `long` 值创建。               |
|                  | `new BigDecimal(int val)`    | `new BigDecimal(123)`          | 使用 `int` 值创建。                |
|                  | `new BigDecimal(byte[] val)` | `new BigDecimal(byteArray)`    | 用字节数组创建。                   |

### 通过静态方法valueOf()

```java
import java.math.BigDecimal;

public class BigDecimalExample {
    public static void main(String[] args) {
        // 从 long 值创建 BigDecimal 对象
        BigDecimal decimal1 = BigDecimal.valueOf(123456789L);
        System.out.println(decimal1);  // 输出：123456789
    }
}

```

创建 `BigDecimal` 时优先使用字符串类型的构造方法，以避免 `double` 转换时精度丢失。

## 计算方法

| 操作       | `BigInteger` 方法 | `BigDecimal` 方法 |
| ---------- | ----------------- | ----------------- |
| **加法**   | `add()`           | `add()`           |
| **减法**   | `subtract()`      | `subtract()`      |
| **乘法**   | `multiply()`      | `multiply()`      |
| **除法**   | `divide()`        | `divide()`        |
| **取余**   | `mod()`           | `remainder()`     |
| **幂运算** | `pow()`           | `pow()`           |
| **比较**   | `compareTo()`     | `compareTo()`     |
| **相反数** | `negate()`        | `negate()`        |

## BigDecimal保证精度不丢失的机制

BigDecimal 能够保证精度，是因为它使用了任意精度的**整数表示法**，而不是浮动的二进制表示。

BigDecimal 内部使用两个字段存储数字，一个是整数部分 `intVal`，另一个是用来表示小数点的位置 `scale`，避免了浮点数转化过程中可能的精度丢失。

计算时通过整数计算，再结合小数点位置和设置的精度与舍入行为，控制结果精度，避免了由默认浮点数舍入导致的误差。

源码展示

```java
public class BigDecimal extends Number implements Comparable<BigDecimal> {
    private final BigInteger intVal;  // 存储整数部分
    private final int scale;          // 存储小数点的位置

    public BigDecimal(String val) {
        // 使用 BigInteger 来表示数值
        intVal = new BigInteger(val.replace(".", ""));
        scale = val.contains(".") ? val.length() - val.indexOf(".") - 1 : 0;
    }
}

```

