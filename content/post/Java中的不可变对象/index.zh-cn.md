---
date : '2024-11-14T19:07:43+08:00'
draft : false
title : 'Java中的不可变对象'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## 不可变类的定义

一个类的对象在通过构造方法创建后如果状态不会再被改变，那么它就是一个不可变（immutable）类。

它的所有成员变量的赋值仅在构造方法中完成，不会提供任何 setter 方法供外部类去修改，这种类的实例在整个生命周期内保持不变。

## 不可变类的实现

- 类被`final`修饰，保证该类不被继承
- 所有的字段都是`private`和`final`的，确保它们在初始化后不能被更改
- 不提供`setter`方法
- 通过构造函数初始化所有字段
- 如果类包含可变对象的引用，确保这些引用在对象外部无法被修改。例如 `getter` 方法中返回对象的副本（new 一个新的对象）来保护可变对象

**示例代码**

```java
// 不可变类 Writer
public final class Writer {
    private final String name;
    private final int age;
    private final Book book;

    public Writer(String name, int age, Book book) {
        this.name = name;
        this.age = age;
        this.book = book;
    }


    public int getAge() {
        return age;
    }

    public String getName() {
        return name;
    }
    
    // 确保返回的是可变对象的副本
   	public Book getBook() {
    	Book clone = new Book();
   		clone.setPrice(this.book.getPrice());
    	clone.setName(this.book.getName());
    	return clone;
	}
}

// 可变类 Book
public class Book {
    private String name;
    private int price;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getPrice() {
        return price;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    @Override
    public String toString() {
        return "Book{" +
                "name='" + name + '\'' +
                ", price=" + price +
                '}';
    }
}
```

## 不可变类的特点

**优点**：

1. **线程安全**：由于不可变对象的状态不能被修改，它们天生是线程安全的，在并发环境中无需同步。
2. **缓存友好**：不可变对象可以安全地被缓存和共享，如 `String` 的字符串常量池。
3. **防止状态不一致**：不可变类可以有效避免因意外修改对象状态而导致的不一致问题。

**缺点**：

1. **性能问题**：不可变对象需要在每次状态变化时创建新的对象，这可能会导致性能开销，尤其是对于大规模对象或频繁修改的场景（例如 String 频繁拼接）。