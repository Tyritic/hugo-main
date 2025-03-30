---
date : '2025-02-06T14:56:39+08:00'
draft : false
title : 'Java中的原子操作类'
image : ""
categories : ["Java并发编程"]
tags : ["JavaSE"]
description : "Java中的原子操作类"
math : true
---

## 原子操作类是什么

原子类就是具有原子性操作特征的类。

**`java.util.concurrent.atomic`** 包中的 **`Atomic`** 原子类提供了一种线程安全的方式来操作单个变量。

## 原子类的基本特性

- **非阻塞（无锁）**：基于 **CAS（Compare-And-Swap）** 实现，不使用 `synchronized`。
- **高效并发**：比 `synchronized` 或 `Lock` 更快，适合高并发环境。
- **保证原子性**：不会发生竞态条件（Race Condition）。

## 原子操作基本数据类型

- **`AtomicBoolean`**：以原子更新的方式更新 **`boolean`**
- **`AtomicInteger`** ：以原子更新的方式更新 **`Integer`**
- **`AtomicLong`**：以原子更新的方式更新 **`Long`**

常用方法（以 **`AtomicInteger`** 为例）

```java
public final int get() //获取当前的值
public final int getAndSet(int newValue)//获取当前的值，并设置新的值
public final int getAndIncrement()//获取当前的值，并自增
public final int getAndDecrement() //获取当前的值，并自减
public final int getAndAdd(int delta) //获取当前的值，并加上预期的值
boolean compareAndSet(int expect, int update) //如果输入的数值等于预期值，则以原子方式将该值设置为输入值（update）
public final void lazySet(int newValue)//最终设置为newValue, lazySet 提供了一种比 set 方法更弱的语义，可能导致其他线程在之后的一小段时间内还是可以读到旧的值，但可能更高效。
```

## 原子操作数组类型

- **`AtomicIntegerArray`**：原子更新 **`int`** 整数数组的方法。
- **`AtomicLongArray`** ：原子更新 **`long`** 型证书数组的方法。
- **`AtomicReferenceArray`** ：原子更新引用类型数组的方法。

常用方法（以 **`AtomicIntegerArray`** 为例）

```java
public final int get(int i) //获取 index=i 位置元素的值
public final int getAndSet(int i, int newValue)//返回 index=i 位置的当前的值，并将其设置为新值：newValue
public final int getAndIncrement(int i)//获取 index=i 位置元素的值，并让该位置的元素自增
public final int getAndDecrement(int i) //获取 index=i 位置元素的值，并让该位置的元素自减
public final int getAndAdd(int i, int delta) //获取 index=i 位置元素的值，并加上预期的值
boolean compareAndSet(int i, int expect, int update) //如果输入的数值等于预期值，则以原子方式将 index=i 位置的元素值设置为输入值（update）
public final void lazySet(int i, int newValue)//最终 将index=i 位置的元素设置为newValue,使用 lazySet 设置之后可能导致其他线程在之后的一小段时间内还是可以读到旧的值。
```

## 原子操作引用类型

- **`AtomicReference`** ：原子更新引用类型；
- **`AtomicStampedReference`** ：原子更新带有版本号的引用类型。该类将整数值与引用关联起来，可用于解决原子的更新数据和数据的版本号，可以解决使用 **`CAS`** 进行原子更新时可能出现的 ABA 问题。
- **`AtomicMarkableReference`** ：原子更新带有标记的引用类型。该类将 **`boolean`** 标记与引用关联起来

**示例**

```java
public class AtomicDemo {

    private static AtomicReference<User> reference = new AtomicReference<>();

    public static void main(String[] args) {
        User user1 = new User("a", 1);
        reference.set(user1);
        User user2 = new User("b",2);
        User user = reference.getAndSet(user2);
        System.out.println(user);
        System.out.println(reference.get());
    }

    static class User {
        private String userName;
        private int age;

        public User(String userName, int age) {
            this.userName = userName;
            this.age = age;
        }

        @Override
        public String toString() {
            return "User{" +
                    "userName='" + userName + '\'' +
                    ", age=" + age +
                    '}';
        }
    }
}

// 输出结果
// User{userName='a', age=1}
// User{userName='b', age=2}
```



## 原子更新字段

- **`AtomicIntegerFieldUpdater`** :原子更新整形字段的更新器
- **`AtomicLongFieldUpdater`** ：原子更新长整形字段的更新器
- **`AtomicReferenceFieldUpdater`** ：原子更新引用类型里的字段的更新器

使用步骤

- 通过静态方法 **`newUpdater`** 创建一个更新器，并且设置想要更新的类和字段；
- 字段必须使用 **`public volatile`** 进行修饰；

**示例**

```java
public class AtomicDemo {

    private static AtomicIntegerFieldUpdater updater = AtomicIntegerFieldUpdater.newUpdater(User.class,"age");
    public static void main(String[] args) {
        User user = new User("a", 1);
        int oldValue = updater.getAndAdd(user, 5);
        System.out.println(oldValue);
        System.out.println(updater.get(user));
    }

    static class User {
        private String userName;
        public volatile int age;

        public User(String userName, int age) {
            this.userName = userName;
            this.age = age;
        }

        @Override
        public String toString() {
            return "User{" +
                    "userName='" + userName + '\'' +
                    ", age=" + age +
                    '}';
        }
    }
}
```

## 原子操作的实现原理

Java 中的原子类是通过使用硬件提供的原子操作指令（ **`CAS`** ，Compare-And-Swap）来确保操作的原子性，从而避免线程竞争问题。

具体细节参见 [往期博客](https://tyritic.github.io/p/java%E4%B8%AD%E7%9A%84%E9%94%81/#cas%E7%AE%97%E6%B3%95)

