---
date : '2024-12-04T13:16:44+08:00'
draft : false
title : 'Java中的synchronized关键字'
image : ""
categories : ["Java并发编程"]
tags : ["JavaSE"]
description : "synchronized关键字的底层原理"
math : true
---

## **synchronized** 关键字

`synchronized` 是 Java 提供的一种**内置同步机制**，用于**解决多线程环境下的并发安全问题**。它能够确保同一时刻只有一个线程执行同步代码块，从而防止线程间的**数据不一致**和**竞态条件**。

## **synchronized** 的作用

- **保证原子性**：同步代码块在执行时不会被其他线程打断，保证操作的完整性。
- **保证可见性**：线程进入 **`synchronized`** 代码块前，必须先从主内存中读取变量最新的值，退出时必须将变量的修改刷新到主内存。
- **保证有序性**：由于 **`synchronized`** 具有**内存屏障**（Memory Barrier），可以保证**重排序不会影响同步代码块的正确性**。

## **synchronized** 使用方式

- **同步实例方法** ：为 **当前对象** 加锁，进入同步代码前要获得当前对象的锁；
- **同步静态方法** ：为 **当前类（Class对象）** 加锁，进入同步代码前要获得当前类的锁；
- **同步代码块** ：指定加锁对象，对给定对象加锁，进入同步代码库前要获得给定对象的锁。

{{<notice tip>}}

构造方法不能使用 **`synchronized`** 关键字修饰。但是可以在构造方法内部使用 **`synchronized`** 代码块。

构造方法本身是 **线程安全** 的，但如果在构造方法中涉及到共享资源的操作，就需要采取适当的同步措施来保证整个构造过程的线程安全。

{{</notice>}}

### **synchronized** 修饰实例方法

在实例方法声明中加入 **`synchronized`** 关键字，可以保证在任意时刻，只有一个线程能执行该方法。也就是说，线程在执行这个方法的时候，其他线程不能同时执行，需要等待锁释放。

```java
synchronized void method() {
    //业务代码
}
```

注意事项

- 修饰实例方法是给当前对象上锁
- 不同实例的 **`synchronized`** 方法不会相互影响（每个对象都有一个对象锁，不同的对象，他们的锁不会互相影响）

### **synchronized** 修饰静态方法

给 **当前类** 加锁，会作用于类的所有对象实例 ，进入同步代码前要获得 **当前 class 的锁**。

静态成员不属于任何一个实例对象，归整个类所有，不依赖于类的特定实例，被类的所有实例共享。

```java
synchronized static void method() {
    //业务代码
}
```

注意事项

- 锁的是 **当前类的 Class 对象**，不属于某个对象。
- 当前类的 Class 对象锁被获取，不影响实例对象锁的获取，两者互不影响
- 静态 **`synchronized`** 方法和非静态 **`synchronized`** 方法之间的调用不互斥（因为访问静态 **`synchronized`** 方法占用的锁是当前类的锁，而访问非静态 **`synchronized`** 方法占用的锁是当前实例对象锁。），比如说如果线程 A 调用了一个对象的非静态 synchronized 方法，线程 B 需要调用这个对象所属类的静态 synchronized 方法，是不会发生互斥的

### **synchronized** 修饰代码块

对括号里指定的对象/类加锁：

- **`synchronized(object)`** ：进入同步代码库前要获得 **给定对象的锁**。
- **`synchronized(类.class)`** ：进入同步代码前要获得 **给定 Class 的锁**

```java
synchronized(this) {
    //业务代码
}
```

## **synchronized** 属于可重入锁

**可重入锁** 是指同一个线程在获取了锁之后，可以再次重复获取该锁而不会造成死锁或其他问题。当一个线程持有锁时，如果再次尝试获取该锁，就会成功获取而不会被阻塞。

因此一个线程调用 **`synchronized`** 方法的同时，在其方法体内部调用该对象另一个 **`synchronized`** 方法是允许的

### **示例**

```java
public class AccountingSync implements Runnable{
    static AccountingSync instance=new AccountingSync();
    static int i=0;
    static int j=0;

    @Override
    public void run() {
        for(int j=0;j<1000000;j++){
            //this,当前实例对象锁
            synchronized(this){
                i++;
                increase();//synchronized的可重入性
            }
        }
    }

    public synchronized void increase(){
        j++;
    }

    public static void main(String[] args) throws InterruptedException {
        Thread t1=new Thread(instance);
        Thread t2=new Thread(instance);
        t1.start();t2.start();
        t1.join();t2.join();
        System.out.println(i);
    }
}
```

- **`AccountingSync`** 类中定义了一个静态的 **`AccountingSync`** 实例 **`instance`** 和两个静态的整数 **`i`** 和 **`j`**，静态变量被所有的对象所共享。
- 在 **`run()`** 方法中，使用了 **`synchronized(this)`** 来加锁。这里的锁对象是 **`this`**（当前的 **`AccountingSync`** 实例）。在锁定的代码块中，对静态变量 **`i`** 进行增加，并调用了 **`increase()`** 方法。
- **`increase()`** 方法是一个同步方法，它会对 **`j`** 进行增加。由于 **`increase()`** 方法也是同步的，所以它能在已经获取到锁的情况下被 **`run()`** 方法调用，体现 **`synchronized`** 关键字的可重入性。
- 在 **`main`** 方法中，创建了两个线程 **`t1`** 和 **`t2`**，它们共享同一个 **`Runnable`** 对象
-  **`synchronized(this)`** 和 **`synchronized`** 方法都使用了同一个锁对象（当前的 AccountingSync 实例），并且对静态变量 **`i`** 和 **`j`** 进行了增加操作，因此，在多线程环境下，也能保证 **`i`** 和 **`j`** 的操作是线程安全的。

### 实现原理

**`synchronized`** 底层是利用计算机系统mutex Lock实现的。每一个可重入锁都会关联一个线程ID和一个锁状态 **`status`**。

- 当一个线程获取对象锁时，JVM 会将该线程的 ID 写入 **`Mark Word`**，并将锁计数器设为 1。
- 如果一个线程尝试再次获取已经持有的锁，JVM 会检查 **`Mark Word`** 中的线程 ID。
  - 如果 ID 匹配，表示的是同一个线程，锁计数器递增。
- 当线程退出同步块时，锁计数器递减。如果计数器值为零，JVM 将锁标记为未持有状态，并清除线程 ID 信息。

## **synchronized** 底层实现原理

**`synchronized`** 实现原理依赖于 JVM 的 Monitor（监视器锁） 和 对象头（Object Header）。

当 **`synchronized`** 修饰在方法或代码块上时，会对特定的对象或类加锁，从而确保同一时刻只有一个线程能执行加锁的代码块。

- **synchronized 修饰方法**：会在方法的访问标志中增加一个 **`ACC_SYNCHRONIZED`** 标志。每当一个线程访问该方法时，JVM 会检查方法的访问标志。如果包含 **`ACC_SYNCHRONIZED`** 标志，线程必须先获得该方法对应的对象的监视器锁（即对象锁），然后才能执行该方法，从而保证方法的同步性。
- **synchronized 修饰代码块**：会在代码块的前后插入 **`monitorenter`** 和 **`monitorexit`** 字节码指令。
  - 执行 **`monitorenter`** 指令时会尝试获取对象锁，如果对象没有被锁定或者已经获得了锁，锁的计数器+1。此时其他竞争锁的线程则会进入等待队列中。
  - 执行 **`monitorexit`** 指令时则会把计数器-1，当计数器值为0时，则锁释放，处于等待队列中的线程再继续竞争锁。


从源码的角度上

- 当多个线程进入同步代码块时，首先进入entryList
- 有一个线程获取到monitor锁后，就赋值给当前线程，并且计数器+1
- 如果线程调用wait方法，将释放锁，当前线程置为null，计数器-1，同时进入waitSet等待被唤醒，调用notify或者notifyAll之后又会进入entryList竞争锁
- 如果线程执行完毕，同样释放锁，计数器-1，当前线程置为null

### 原子性的保证

- 线程加锁前，将清空工作内存中共享变量的值，从而使用共享变量时需要从主内存中重新读取最新的值。
- 线程加锁后，其它线程无法获取主内存中的共享变量。
- 线程解锁前，必须把共享变量的最新值刷新到主内存中。

### 有序性的保证

**`synchronized`** 同步的代码块，具有排他性，一次只能被一个线程拥有，所以 **`synchronized`** 保证同一时刻，代码是单线程执行的。

**`synchronized`** 通过 JVM 指令 **`monitorenter`** 和 **`monitorexit`** 来确保加锁代码块内的指令不会被重排。

- **`monitorenter`** ：获取锁，进入同步代码块 
- **`monitorexit`** ：释放锁，退出同步代码块

### 可重入锁的实现

可重入意味着同一个线程可以多次获得同一个锁，而不会被阻塞。

**`synchronized`** 支持可重入的原理

- Java 的对象头包含了一个 Mark Word，用于存储对象的状态，包括锁信息。

- 当一个线程获取对象锁时，JVM 会将该线程的 ID 写入 Mark Word，并将锁计数器设为 1。

- 如果一个线程尝试再次获取已经持有的锁，JVM 会检查 Mark Word 中的线程 ID。如果 ID 匹配，表示的是同一个线程，锁计数器递增。

- 当线程退出同步块时，锁计数器递减。如果计数器值为零，JVM 将锁标记为未持有状态，并清除线程 ID 信息。

源码中是通过 Monitor 对象的 owner 和 count 字段实现的，owner 记录持有锁的线程，count 记录线程获取锁的次数。

## **synchronized** 的锁升级过程

参见[下期博客](https://tyritic.github.io/p/java%E4%B8%AD%E7%9A%84%E9%94%81/)
