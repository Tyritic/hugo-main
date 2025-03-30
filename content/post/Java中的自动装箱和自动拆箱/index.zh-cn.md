---
date : '2025-01-02T14:29:54+08:00'
draft : false
title : 'Java中的自动装箱和自动拆箱'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "Java中的自动装箱和自动拆箱机制"
math : true
---

## 回答重点

**自动装箱（Autoboxing）**：指的是 Java 编译器自动将基本数据类型转换为它们对应的包装类型。比如，将 `int` 转换为 `Integer`。

**自动拆箱（Unboxing）**：指的是 Java 编译器自动将包装类型转换为基本数据类型。比如，将 `Integer` 转换为 `int`。

**主要作用**：

- 它在 Java 5 中引入，主要是为了提高代码的可读性，减少手动转换操作，简化了代码编写，开发者可以更方便地在基本类型和包装类型之间进行转换。

**常见于**：

- 集合类如 `List<Integer>` 中无法存储基本类型，通过自动装箱，可以将 `int` 转换为 `Integer` 存入集合。

  ```java
  int i = 99;                 //声明基础数据类型int变量
  ArrayList list = new ArrayList();
  list.add(i);                //触发自动装箱，int类型自动转换成 Integer 
  System.out.println(list);
  ```

- 自动装箱和拆箱经常在算术运算中出现，尤其是包装类型参与运算时。

## 拓展知识

### 底层实现

自动装箱和拆箱并不是通过语法糖实现的，它是通过调用包装类型的 `valueOf()` 和 `xxxValue()` 方法实现的。

- 自动装箱调用：`Integer.valueOf(int i)`
- 自动拆箱调用：`Integer.intValue()`

**示例**：

```java
Integer a = Integer.valueOf(10);  // 自动装箱
int b = a.intValue();             // 自动拆箱
```

### 注意点

#### **性能影响**

自动装箱和拆箱虽然简化了编码，但在频繁使用的场景，可能导致性能开销，尤其是在循环中频繁发生装箱或拆箱时，容易引入不必要的对象创建和垃圾回收。

所以尽量避免在性能敏感的代码中频繁使用自动装箱和拆箱。例如：

```java
Integer sum = 0;
for (int i = 0; i < 10000; i++) {
    sum += i;  // sum 是包装类型，导致多次装箱和拆箱
}
```

#### NullPointerException

在进行拆箱操作时，如果包装类对象为 null，会抛出 NullPointerException。

```java
Integer num = null;
int n = num;  // 抛出 NullPointerException
```