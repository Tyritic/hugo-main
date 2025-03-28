---
date : '2025-01-03T10:56:32+08:00'
draft : false
title : 'Java中静态方法和实例方法的区别'
image : ""
categories : ["互联网面试题"]
tags : ["JavaSE"]
description : "Java中静态方法和实例方法的辨析"
math : true
---

## 回答重点

### 静态方法

#### 方法特点

- 由 **static** 关键字修饰
- 方法属于类，而不是类的某个实例
- 可以通过类名.方法名的格式直接调用，也可以通过对象调用（不推荐）
- 只能访问类的静态变量和其他静态方法（这些方法和变量属于类），但是不能访问类的实例方法和实例变量（实例方法和实例变量属于对象）
- 随着类的加载而加载，随着类的消亡而消失

#### 典型使用场景

- 工具类
- 工厂方法

### 实例方法

#### 方法特点

- 不使用 **static** 关键字声明的方法。
- 属于类的实例。
- 必须通过对象来调用。
- 可以访问实例变量和实例方法。也可以访问类的静态变量和静态方法。
- 随着对象的创建而存在，随着对象的销毁而消失。

#### 典型使用场景

- 操作或修改对象的实例变量。
- 执行与对象状态相关的操作。

### 两者对比

| 特性     | 静态方法                   | 实例方法                                       |
| -------- | -------------------------- | ---------------------------------------------- |
| 关键字   | static                     | 无                                             |
| 归属     | 类                         | 对象                                           |
| 调用方式 | 通过类名或对象调用         | 通过对象调用                                   |
| 访问权限 | 只能访问静态变量和静态方法 | 可以访问实例变量、实例方法、静态变量和静态方法 |
| 典型用途 | 工具类方法、工厂方法       | 操作对象实例变量、与对象状态相关的操作         |
| 生命周期 | 类加载时存在，类卸载时消失 | 对象创建时存在，对象销毁时消失                 |

## 拓展知识

- 静态方法中不能使用 `this` 关键字，因为 `this` 代表当前对象实例，而静态方法属于类，不属于任何实例。
- 静态方法可以被重载（同类中方法名相同，但参数不同），但不能被子类重写（因为方法绑定在编译时已确定）。实例方法可以被重载，也可以被子类重写。
- 实例方法中可以直接调用静态方法和访问静态变量。
- 静态方法不具有多态性，即不支持方法的运行时动态绑定。