---
date : '2025-02-04T16:24:44+08:00'
draft : false
title : 'Java中的AQS'
image : ""
categories : ["Java并发编程"]
tags : ["JavaSE"]
description : "AQS-抽象队列同步器"
math : true
---

## 什么是AQS

**`AQS`** 全称 **`Abstract Queued Synchronizer`** 即 **抽象队列同步器**

可以从以下角度理解

- 抽象：抽象类，只实现一些主要逻辑，有些方法由子类实现；
- 队列：使用先进先出（FIFO）的队列存储数据；
- 同步：实现了同步的功能。

**`AQS`** 是一个用来构建锁和同步器的框架，使用 **`AQS`** 能简单且高效地构造出应用广泛的同步器

**`AQS`** 常见的实现类有 **`ReentrantLock`** 、 **`CountDownLatch`** 、 **`Semaphore`**  等等

**`AQS`** 核心思想是，如果被请求的共享资源空闲，则将当前请求资源的线程设置为有效的工作线程，并且将共享资源设置为锁定状态。如果被请求的共享资源被占用，那么就需要一套线程阻塞等待以及被唤醒时锁分配的机制，AQS 是用 **CLH 队列锁** 实现这个机制，即将暂时获取不到锁的线程加入到队列中。

## AQS的底层数据结构

![AQS的数据结构](640.png)

### 状态

**`AQS`** 通过一个 **`volatile`** 类型的整数 **`state`** 来表示同步状态。

```java
/**
 * The synchronization state.
 */
private volatile int state;
```



### CLH双端队列

**`AQS`** 内部使用了一个先进先出（FIFO）的双端队列。用于管理等待获取同步状态的线程。CLH变体队列是一个虚拟的双向队列（虚拟的双向队列即不存在队列实例，仅存在结点之间的关联关系）。每个节点（Node）代表一个等待的线程，节点之间通过 next 和 prev 指针链接。

```java
static final class Node {
    static final Node SHARED = new Node();
    static final Node EXCLUSIVE = null;
    volatile int waitStatus;
    volatile Node prev;
    volatile Node next;
    volatile Thread thread; // 保存等待的线程
    Node nextWaiter;
    .....
}
```

在 CLH 变体队列中，会对等待的线程进行阻塞操作，当队列前边的线程释放锁之后，需要对后边的线程进行唤醒

{{<notice tip>}}

**CLH 锁** 对自旋锁进行了改进，是基于单链表的自旋锁。在多线程场景下，会将请求获取锁的线程组织成一个单向队列，每个等待的线程会通过自旋访问前一个线程节点的状态，前一个节点释放锁之后，当前节点才可以获取锁。

{{</notice>}}

### 资源共享模式

**`AQS`** 支持两种同步方式：

- 独占模式：只有一个线程能获取同步状态，例如 **`ReentrantLock`** 。
- 共享模式：多个线程可以同时获取同步状态，例如 **`Semaphore`** 和 **`ReadWriteLock`**。

如果共享资源被占用，需要一种特定的阻塞等待唤醒机制来保证锁的分配，**`AQS`** 会将竞争共享资源失败的线程添加到一个 CLH 队列中。![CLH队列](javathread-41.png)

在 CLH 锁中，当一个线程尝试获取锁并失败时，它会将自己添加到队列的尾部并自旋，等待前一个节点的线程释放锁。