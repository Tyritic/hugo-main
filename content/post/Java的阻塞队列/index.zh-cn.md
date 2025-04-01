---
date : '2025-02-07T21:27:50+08:00'
draft : false
title : 'Java的阻塞队列'
image : ""
categories : ["Java并发编程"]
tags : ["JavaSE"]
description : "线程池中常用的阻塞队列"
math : true
---

## 什么是阻塞队列

阻塞队列代表的是线程安全的队列，不仅可以由多个线程并发访问，还添加了等待/通知机制，以便在队列为空时阻塞获取元素的线程，直到队列变得可用，或者在队列满时阻塞插入元素的线程，直到队列变得可用。

## 常见操作

由于 BlockingQueue 继承了 Queue 接口，因此，BlockingQueue 也具有 Queue 接口的基本操作，如下所示：

### 插入元素

- **`boolean add(E e)`**  ：将元素添加到队列尾部，如果队列满了，则抛出异常 **`IllegalStateException`** 。
- **`boolean offer(E e)`** ：将元素添加到队列尾部，如果队列满了，则返回 **`false`**。

### 删除元素

- **`boolean remove(Object o)`** ：从队列中删除元素，成功返回 **`true`**，失败返回 **`false`**
- **`E poll()`** ：检索并删除此队列的头部，如果此队列为空，则返回 **`null`**。

### 查找元素

- **`E element()`** ：检索但不删除此队列的头部，如果队列为空时则抛出 **`NoSuchElementException`** 异常；
- **`peek()`** ：检索但不删除此队列的头部，如果此队列为空，则返回  **`null`** .

### 特定方法

- **`void put(E e)`** ：将元素添加到队列尾部，如果队列满了，则线程将阻塞直到有空间。
- **`offer(E e, long timeout, TimeUnit unit)`** ：将指定的元素插入此队列中，如果队列满了，则等待指定的时间，直到队列可用。
- **`take()`** ：检索并删除此队列的头部，如有必要，则等待直到队列可用；
- **`poll(long timeout, TimeUnit unit)`** ：检索并删除此队列的头部，如果需要元素变得可用，则等待指定的等待时间。

## ArrayBlockingQueue

**`ArrayBlockingQueue`** 它是一个基于数组的有界阻塞队列

### 特点

- 有界：**`ArrayBlockingQueue`** 的大小是在构造时就确定了，并且在之后不能更改。这个界限提供了流量控制，有助于资源的合理使用。
- FIFO：队列操作符合先进先出的原则。
- 当队列容量满时，尝试将元素放入队列将导致阻塞；尝试从一个空的队列取出元素也会阻塞

### 实现原理

**`ArrayBlockingQueue`** 一旦创建，容量不能改变。其并发控制采用可重入锁 **`ReentrantLock`** ，不管是插入操作还是读取操作，都需要获取到锁才能进行操作。当队列容量满时，尝试将元素放入队列将导致操作阻，尝试从一个空队列中取一个元素也会同样阻塞。

**`ArrayBlockingQueue`** 默认情况下不能保证线程访问队列的公平性但是可以在构造方法中将第二个 **`Boolean`** 类型参数设置为 **`true`**

## LinkedBlockingQueue

**`LinkedBlockingQueue`** 是一个底层基于**单向链表**实现的阻塞队列，可以当做无界队列也可以当做有界队列来使用，同样满足 FIFO 的特性。

### 特点

- 可以在队列头部和尾部进行高效的插入和删除操作。
- 当队列为空时，取操作会被阻塞，直到队列中有新的元素可用。当队列已满时，插入操作会被阻塞，直到队列有可用空间。
- 可以在构造时指定最大容量。如果不指定，默认为 **`Integer.MAX_VALUE`**，这意味着队列的大小受限于可用内存。

### 实现原理

**`LinkedBlockingQueue`** 使用两个锁（putLock 和 takeLock），一个用于放入操作，另一个用于取出操作。锁分离

## PriorityBlockingQueue

**`PriorityBlockingQueue`** 是一个支持优先级的无界阻塞队列。默认情况下元素采用自然顺序进行排序，也可以通过自定义类实现 **`compareTo()`** 方法来指定元素排序规则，或者初始化时通过构造器参数 **`Comparator`** 来指定排序规则。

**`PriorityBlockingQueue`** 并发控制采用的是可重入锁 **`ReentrantLock`**，队列为无界队列（ **`ArrayBlockingQueue`** 是有界队列，**`LinkedBlockingQueue`** 也可以通过在构造函数中传入 **`capacity`** 指定队列最大的容量，但是 **`PriorityBlockingQueue`** 只能指定初始的队列大小，后面插入元素的时候，**如果空间不够的话会自动扩容**）。

## 其他阻塞队列

- **`SynchronousQ ueue`**：每个插入操作必须等待另一个线程的移除操作，同样，任何一个移除操作都必须等待另一个线程的插入操作。
- **`DelayQueue`** ：类似于 PriorityBlockingQueue，由二叉堆实现的无界优先级阻塞队列。