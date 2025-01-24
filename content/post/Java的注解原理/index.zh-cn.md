---
date : '2025-01-20T09:40:41+08:00'
draft : false
title : 'Java的注解原理'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "Java中注解的实现原理"
math : true
---

## 什么是注解

**注解（Annotation）** 是一种元数据，它为代码提供了附加的信息，注解本身不直接影响代码的逻辑执行，但可以通过工具、编译器或运行时反射等机制对代码进行处理。

## 注解的定义方式

```java
public @interface MyAnnotation {
    String value() default "default value";  // 带有默认值的元素
    int number();  // 没有默认值的元素
}
```

## 注解的目标对象

- **`ElementType.TYPE`**：类、接口（包括注解类型）或枚举。
- **`ElementType.FIELD`**：字段（包括枚举常量）。
- **`ElementType.METHOD`**：方法。
- **`ElementType.PARAMETER`**：方法参数。
- **`ElementType.CONSTRUCTOR`**：构造方法。
- **`ElementType.LOCAL_VARIABLE`**：局部变量。
- **`ElementType.ANNOTATION_TYPE`**：注解类型。
- **`ElementType.PACKAGE`**：包。

定义在 `ElementType` 枚举中，使用元注解`@Target`指定目标对象

## 注解的生命周期

- **`RetentionPolicy.SOURCE`**：注解仅在源码中存在，编译时被丢弃。
- **`RetentionPolicy.CLASS`**：注解存在于编译后的 `.class` 文件中，但运行时不可用。
- **`RetentionPolicy.RUNTIME`**：注解在运行时可用，可以通过反射机制访问。

定义在 `RetentionPolicy` 枚举中，使用元注解`@Retention`指定生命周期

## 示例

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface JsonField {
    public String value() default "";
}
```

- JsonField 注解的生命周期是 RUNTIME，也就是运行时有效。
- JsonField 注解装饰的目标是 FIELD，也就是针对字段的。
- 创建注解需要用到 `@interface` 关键字。
- JsonField 注解有一个参数，名字为 value，类型为 String，默认值为一个空字符串。