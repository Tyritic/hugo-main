---
date : '2024-11-15T16:14:45+08:00'
draft : false
title : 'Java中的内部类'
image : ""
categories : ["Java基础","互联网面试题"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## 内部类的定义

在 Java 中，**内部类（Inner Class）** 是定义在另一个类内部的类。内部类可以更方便地访问外部类的成员变量和方法，同时也提升了封装性和代码的逻辑关联性。

## 内部类的访问特定

- 内部类可以直接访问外部类的成员（包括`private`）
- 外部类要访问内部类的成员必须创建内部类对象

## 成员内部类

成员内部类是定义在外部类成员位置中的普通类。它与外部类的实例关联，只有在创建了外部类对象后，才能创建其内部类对象。

### 特点

- 内部类可以直接访问外部类的私有成员。
- 创建内部类对象需要先创建外部类对象，再通过外部类对象创建内部类对象。
- 内部类中的变量可以被访问控制符和`static`修饰

### 使用格式

```java
外部类.内部类
```

### 内存实现

在创建内部类对象时使用`Outer.this`记录外部类对象的地址值

### 示例代码

```java
public class Outer {
    private String name = "OuterClass";

    // 成员内部类
    public class Inner {
        public void display() {
            System.out.println("内部类访问外部类的成员: " + name);
        }
    }

    public static void main(String[] args) {
        Outer outer = new Outer();
        Outer.Inner inner = outer.new Inner();  // 创建内部类对象
        inner.display();
    }
}

```

## 静态内部类

静态内部类使用 `static` 修饰符定义，可以独立于外部类的实例进行创建

### 特点

- 可以直接访问外部类的静态成员
- 不可以直接访问外部类的非静态成员,若要访问则要创建外部类对象
- 不存在`Outer.this`

### 语法格式

- 创建静态内部类对象

  ```java
  外部类.内部类 变量名=new 外部类.内部类构造器
  ```

- 调用静态内部类方法的格式

  - 非静态方法：先创建静态内部类对象再调用
  - 静态方法：`外部类.内部类.方法名()`

### 示例代码

```java
public class Outer {
    private static String staticName = "StaticOuterClass";

    // 静态内部类
    public static class StaticInner {
        public void display() {
            System.out.println("静态内部类访问外部类的静态成员: " + staticName);
        }
    }

    public static void main(String[] args) {
        Outer.StaticInner inner = new Outer.StaticInner();  // 直接创建静态内部类对象
        inner.display();
    }
}

```

## 局部内部类

局部内部类是在方法或代码块中定义的类，作用域仅限于所在方法或代码块。

### 特点

- 局部内部类的作用域仅限于定义它的方法或代码块中。
- 局部内部类可以访问外部类的成员以及方法中的局部变量（需要局部变量使用 `final` 或隐式 `final` 修饰）。

### 示例代码

```java
public class Outer {
    public void method() {
        class LocalInner {
            public void display() {
                System.out.println("这是局部内部类");
            }
        }
        LocalInner inner = new LocalInner();  // 创建局部内部类对象
        inner.display();
    }

    public static void main(String[] args) {
        Outer outer = new Outer();
        outer.method();
    }
}
```

## 匿名内部类

**匿名内部类**是没有名字的内部类，它是在**定义类的同时创建该类的对象**，通常用于简化代码，尤其在需要实现接口或继承抽象类时，可以避免单独定义实现类。

本质：**隐藏了名字的内部类**

使用前提：必须继承一个父类或实现一个接口

### 特点

- **没有名字**：匿名内部类在创建时定义，没有类名。

- **一次性使用**：匿名内部类只能使用一次，不能重复创建多个实例。

- **可以继承类或实现接口**：

  - 如果继承一个类，匿名内部类只能继承一个父类。

  - 如果实现一个接口，匿名内部类可以实现该接口并提供方法实现。

- **与外部类关系**：

  - 匿名内部类可以直接访问外部类的成员（包括私有成员）。

  - 如果匿名内部类是在局部方法中定义的，它只能访问 **`final`** 的局部变量。

- **不能有构造方法**：因为匿名内部类没有名字，无法定义构造方法。

### 语法格式

```java
new 接口名或父类名() {
    // 方法实现
};
```

### Lambda表达式

**Lambda 表达式**是 Java 8 引入的一种新特性，旨在简化代码，特别是当使用匿名内部类实现接口时。Lambda 表达式可以理解为一种匿名函数，直接将行为（函数）作为参数传递，使代码更加简洁、可读。

#### 语法格式

```java
(参数列表) -> { 方法体 }
```

#### 可以用于简写匿名内部类

Lambda表达式只能简化实现**函数式接口**的匿名内部类

**函数式接口**：有且仅有一个抽象方法的接口，被`@FunctionalInterface`注解

#### 省略规则

- **在参数列表中，参数类型可以省略**，因为编译器会根据上下文推断参数的类型。
- 当 Lambda 表达式只有一个参数时，可以省略参数两边的小括号 `()`
- **当 Lambda 表达式的方法体中只有一条语句时，可以省略大括号 `{}`**。同时，如果这条语句是 `return` 语句，可以省略 `return` 关键字。

#### 示例代码

```java
import java.util.Comparator;

public class LambdaExample {
    public static void main(String[] args) {
        // 匿名内部类
        Comparator<String> comparatorAnonymous = new Comparator<String>() {
            @Override
            public int compare(String s1, String s2) {
                return s1.length() - s2.length();
            }
        };

        // Lambda 表达式完整格式
        Comparator<String> comparatorFull = (String s1, String s2) -> {
            return s1.length() - s2.length();
        };

        // Lambda 表达式省略格式
        Comparator<String> comparatorSimplified = (s1, s2) -> s1.length() - s2.length();

        // 使用匿名内部类
        String resultAnonymous = max("apple", "banana", comparatorAnonymous);
        System.out.println("使用匿名内部类较长的字符串是：" + resultAnonymous);

        // 使用 Lambda 表达式完整格式
        String resultFull = max("apple", "banana", comparatorFull);
        System.out.println("使用 Lambda 完整格式较长的字符串是：" + resultFull);

        // 使用 Lambda 表达式省略格式
        String resultSimplified = max("apple", "banana", comparatorSimplified);
        System.out.println("使用 Lambda 省略格式较长的字符串是：" + resultSimplified);
    }

    // 辅助方法：根据 Comparator 返回较长的字符串
    public static String max(String s1, String s2, Comparator<String> comparator) {
        return comparator.compare(s1, s2) > 0 ? s1 : s2;
    }
}

```

