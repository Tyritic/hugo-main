---
date : '2024-11-14T23:16:07+08:00'
draft : false
title : 'Java中的final关键字'
image : ""
categories : ["Java"]
tags : ["Java基础"]
description : "手写笔记转换"
math : true
---

## 🧠 作用

**`final`** 关键字用于修饰不可被改变的变量/方法、类，表示最终态，禁止进一步的修改或继承。

---

## 📚 修饰方式

### 💡 修饰类

被 **`final`** 修饰的类无法被继承，整个类都是最终版本。

```java
public final class ImmutableClass {
    // 不能有子类
}

// 编译错误：Cannot extend final class
// class SubClass extends ImmutableClass { }
```

### 🔧 修饰方法

被 **`final`** 修饰的方法不能被继承类重写，保证方法的实现固定不变。

```java
public class Parent {
    public final void criticalMethod() {
        System.out.println("This method cannot be overridden");
    }
}

public class Child extends Parent {
    // 编译错误：Cannot override final method
    // public void criticalMethod() { }
}
```

### 📌 修饰变量

表明这个变量是常量，只能被赋值一次，赋值后不能改变。

```java
public class FinalVariableExample {
    // 常量：必须在声明时或构造方法中赋值
    private final String name;
    
    public FinalVariableExample(String name) {
        this.name = name;  // 赋值一次
        // this.name = "other";  // 编译错误：不能重新赋值
    }
}
```

---

## ⚙️ 修饰基本数据类型 vs 引用数据类型

### 🔹 基本数据类型

修饰基本数据类型则变量存储的数值不变。

```java
final int num = 10;
num = 20;  // 编译错误：不能改变值
```

### 🔹 引用数据类型

修饰引用数据类型则变量存储的地址值不变，但是对象的属性可以改变。

```java
public class Box {
    private int value;
    
    public Box(int value) {
        this.value = value;
    }
    
    public void setValue(int value) {
        this.value = value;
    }
}

public class FinalReferenceExample {
    public static void main(String[] args) {
        final Box box = new Box(10);
        
        // ❌ 编译错误：不能改变引用指向
        // box = new Box(20);
        
        // ✅ 可以改变对象的属性
        box.setValue(20);
    }
}
```

---

## ✅ 最佳实践

1. **使用 final 修饰不可变对象** - 提高线程安全性
2. **类设计时明确继承意图** - 如不需要被继承，使用 final
3. **性能优化** - JVM 可以对 final 方法进行内联优化