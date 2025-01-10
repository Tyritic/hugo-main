---
date : '2024-11-03T11:35:06+08:00'
draft : false
title : 'Java中的基本数学操作'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## Math类的简介

Java在Math类中封装了相关的数学函数，位于Java.lang包中

构造方法是`private`的，且所有方法都是静态方法，可以不依赖实例进行调用

## 静态常量

自然对数$e$：`Math.E`（double数据类型）

圆周率$π$：`Math.PI`（double数据类型）

## 三角函数

- `Math.toRadians()`：角度 --> 弧度
- `Math.toDegrees()`：弧度 --> 弧度
- 正切值：`Math.sin()`
- 余弦值：`Math.cos()`
- 反正弦值：`Math.asin()`
- 反余弦值：`Math.acos()`
- 正切值：`Math.tan()`
- 反正切值：`Math.atan()` 

示例代码

```java
/* 三角函数 */
// 角度 --> 弧度 toRadians()
double x = 45; // 45°  45° -->  PI / 4
System.out.println("45°转换为弧度：" + Math.toRadians(x));
System.out.println(Math.PI / 4);
 
double y = 180;
System.out.println("180°转换为弧度：" + Math.toRadians(y));
System.out.println(Math.PI);
 
// 弧度 --> 弧度 toDegrees()
double z = 0.7853981633974483; // PI / 4 -->  45°
System.out.println("0.7853981633974483转换为角度" + Math.toDegrees(z));
 
// 正弦函数sin()
double degrees = 45.0;
double radians = Math.toRadians(degrees);
System.out.println("45° 的正弦值: " + Math.sin(radians));
 
// 余弦函数cos()
System.out.println("45° 的余弦值: " + Math.cos(radians));
 
// 反正弦值asin()
System.out.println("45° 的反正弦值: " + Math.asin(radians));
 
// 反余弦值acos()
System.out.println("45° 的反余弦值: " + Math.acos(radians));
 
// 正切值tan()
System.out.println("45° 的正切值: " + Math.tan(radians));
 
// 反正切值atan() atan2()
double m = 45;
double n = 30;
System.out.println("45° 的反正切值1: " + Math.atan(radians)); // atan()
System.out.println("反正弦值2: " + Math.atan2(m, n)); // atan2() 坐标系表示角的反正切值
```

## 指数函数

- `Math.exp()`：自然对数e的幂函数
- `Math.pow()`：幂函数
- `Math.sqrt()`：平方根
- `Math.cbrt()`：立方根
- `Math.log()`：ln函数
- `Math.log 10()`：log_10函数

示例代码

```java
/* 指数函数 */
double p = 8;
double q = 3;
 
// exp()
System.out.println("e的6次幂: " + Math.exp(p)); // e^8
 
// pow()
System.out.println("8的3次幂: " + Math.pow(p, q)); // 8^3
 
// sqrt()
System.out.println("8的平方根: " + Math.sqrt(p));
 
// cbrt()
System.out.println("8的立方根: " + Math.cbrt(p)); // 2
 
// log()
System.out.println("ln(8): " + Math.log(p)); // ln(8)
 
// log10()
System.out.println("log10(8): " + Math.log10(p)); // log10(8)
```

## 取整函数

- `Math.ceil()`：上取整
- `Math.floor()`：下取整
- `Math.rint()`：最近的整数，0.5返回0
- `Math.round()`：四舍五入的整数，0.5返回1

示例代码

```
/* 取整 */
double d = 100.675;
double e = 100.500;
 
// >=的整数  ceil()
System.out.println("ceil(100.675): " + Math.ceil(d));
 
// <=的整数  floor()
System.out.println("floor(100.675): " + Math.floor(d));
 
// 最近的整数  rint()
System.out.println("rint(100.675): " + Math.rint(d));
System.out.println("rint(100.500): " + Math.rint(e));
 
// 四舍五入的整数  round()
System.out.println("round(100.675): " + Math.round(d));
System.out.println("round(100.500): " + Math.round(e));
```

## 比较函数

- `Math.min()`：最小值
- `Math.max()`：最大值
- `Math.abs()`：绝对值

示例代码

```java
/* 其他 */
// min() 最小
System.out.println("min(): " + Math.min(2, 10));
 
// max() 最大
System.out.println("max(): " + Math.max(2, 10));
 
// abs() 绝对值
System.out.println("abs(): " + Math.abs(-5));
```

## 随机数生成

- `Math.random()`：随机产生一个数 random()，随机数范围为 0.0 =< Math.random < 1.0

`a+Math.random()+b`生成[a,a+b)