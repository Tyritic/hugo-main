---
date : '2024-11-14T11:44:37+08:00'
draft : false
title : 'Java中的this关键字和就近原则'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## 就近原则

通常是指在方法调用过程中，编译器或 JVM 根据 "就近" 的方式来解析某些元素，特别是 **变量**、**方法**、**类型**、**类** 等的访问。

### 示例代码

```java
public class Example {
    private int x = 10;  // 类成员变量

    public void myMethod(int x) {  // 参数 x 会遮蔽成员变量 x
        System.out.println("Local x: " + x);  // 使用的是方法参数 x
        System.out.println("Member x: " + this.x);  // 使用成员变量 x
    }

    public static void main(String[] args) {
        Example obj = new Example();
        obj.myMethod(20);
    }
}

```

## this关键字

`this`关键字用于指代类实例化后的当前实例

### 使用场景

#### 当局部变量和实例变量重名时进行区分

其中被`this`修饰的变量是实例变量

不被 `this`修饰的变量是局部变量

**示例代码**

```java
public class WithThisStudent {
    String name;
    int age;

    WithThisStudent(String name, int age) {
        this.name = name;
        this.age = age;
    }

    void out() {
        System.out.println(name+" " + age);
    }

    public static void main(String[] args) {
        WithThisStudent s1 = new WithThisStudent("王二", 18);
        WithThisStudent s2 = new WithThisStudent("王三", 16);

        s1.out();
        s2.out();
        
        // 输出：
        // 王二 18
		// 王三 16
    }
}
```

#### 调用当前类的方法

可以在一个类中使用 `this` 关键字来调用另外一个方法，如果没有使用的话，编译器会自动帮我们加上

#### 调用当前类的其他构造方法

`this`关键字可以用于在当前类的构造方法中调用当前类的其他构造方法，但是`this()` 必须放在构造方法的第一行

**示例代码**

```java
// 调用当前类的无参构造方法
public class InvokeConstrutor {
    InvokeConstrutor() {
        System.out.println("hello");
    }

    InvokeConstrutor(int count) {
        this();
        System.out.println(count);
    }

    public static void main(String[] args) {
        InvokeConstrutor invokeConstrutor = new InvokeConstrutor(10);
    }
    // 输出
    // hello
	// 10
}

// 调用当前类的有参构造方法
public class InvokeParamConstrutor {
    InvokeParamConstrutor() {
        this(10);
        System.out.println("hello");
    }

    InvokeParamConstrutor(int count) {
        System.out.println(count);
    }

    public static void main(String[] args) {
        InvokeParamConstrutor invokeConstrutor = new InvokeParamConstrutor();
    }
}
```

#### 作为方法的参数

`this` 关键字可以作为参数在方法中传递，此时，它指向的是当前类的对象。

#### 作为返回值实现链式调用

`this` 关键字作为方法的返回值的时候，方法的返回类型为类的类型

**示例代码**

```java
public class ThisAsMethodResult {
    ThisAsMethodResult getThisAsMethodResult() {
        return this;
    }
    
    void out() {
        System.out.println("hello");
    }

    public static void main(String[] args) {
        new ThisAsMethodResult().getThisAsMethodResult().out();
    }
}
```

### 内存实现

`this`代表当前调用方法的对象引用，哪个对象调用方法，`this`就代表哪个对象的地址值