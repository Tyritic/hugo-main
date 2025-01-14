---
date : '2024-11-14T12:15:40+08:00'
draft : false
title : 'Java中的构造方法'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## 构造方法的作用

用于给对象实例进行初始化，只有在构造方法被调用的时候，对象才会被分配内存空间。

## 构造方法的调用时机

每次使用 `new` 关键字创建对象的时候，构造方法至少会被调用一次。”

## 定义构造方法的规则

- 构造方法的名字必须和类名一样；
- 构造方法没有返回类型，包括 void；
- 构造方法不能是抽象的（abstract）、静态的（static）、最终的（final）、同步的（synchronized）。
  - 由于构造方法不能被子类继承，所以用 final 和 abstract 关键字修饰没有意义；
  - 构造方法用于初始化一个对象，所以用 static 关键字修饰没有意义；
  - 多个线程不会同时创建内存地址相同的同一个对象，所以用 synchronized 关键字修饰没有必要。

## 无参构造方法（默认构造方法）

如果一个构造方法中没有任何参数，那么它就是一个默认构造方法，也称为无参构造方法。

通常情况下，无参构造方法是可以缺省的，开发者并不需要显式的声明无参构造方法，编译器将提供一个无参数，方法体为空的构造方法。

当用户显式定义了构造方法后，系统将不再提供默认构造函数。

默认构造方法的目的主要是为对象的字段提供默认值

## 有参构造方法

有参数的构造方法被称为有参构造方法，参数可以有一个或多个。有参构造方法可以为不同的对象提供不同的值。

如果没有有参构造方法的话，就需要通过 setter 方法给字段赋值了。

## 重载构造方法

构造方法它也可以像方法一样被重载。构造方法的重载只需要提供不同的参数列表即可。编译器会通过参数的数量来决定应该调用哪一个构造方法。

```java
public class OverloadingConstrutorPerson {
    private String name;
    private int age;
    private int sex;

    public OverloadingConstrutorPerson(String name, int age, int sex) {
        this.name = name;
        this.age = age;
        this.sex = sex;
    }

    public OverloadingConstrutorPerson(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void out() {
        System.out.println("姓名 " + name + " 年龄 " + age + " 性别 " + sex);
    }

    public static void main(String[] args) {
        OverloadingConstrutorPerson p1 = new OverloadingConstrutorPerson("王二",18, 1);
        p1.out();

        OverloadingConstrutorPerson p2 = new OverloadingConstrutorPerson("王三",16);
        p2.out();
    }
}
```

## 拷贝构造方法

利用一个已有对象将该对象的参数字段直接传递给新的对象

**语法格式**

```java
// 语法格式
class_name(class_name obj)
{
	//字段赋值操作
}

//示例代码
public class CopyConstrutorPerson {
    private String name;
    private int age;

    public CopyConstrutorPerson(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public CopyConstrutorPerson(CopyConstrutorPerson person) {
        this.name = person.name;
        this.age = person.age;
    }

    public void out() {
        System.out.println("姓名 " + name + " 年龄 " + age);
    }

    public static void main(String[] args) {
        CopyConstrutorPerson p1 = new CopyConstrutorPerson("沉默王二",18);
        p1.out();

        CopyConstrutorPerson p2 = new CopyConstrutorPerson(p1);
        p2.out();
    }
}
```

