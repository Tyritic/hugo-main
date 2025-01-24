---
date : '2024-11-21T16:00:25+08:00'
draft : false
title : 'Java中的List实现类'
image : ""
categories : ["Java集合","互联网面试题"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## ArrayList类

`ArrayList` 是 Java 集合框架中的一个类，属于 `java.util` 包，是一种 **基于动态数组实现的可变长度集合**。它实现了 `List` 接口，提供了一个可调整大小的数组，能够存储任意类型的对象（包括自定义类和基本类型的包装类）。

### 特点

- **动态数组：**
  - `ArrayList` 的大小是可变的，默认容量为 10。当元素数量超过当前容量时，`ArrayList` 会自动扩容，通常以 1.5 倍的速度增长。
- **有序：**
  - 元素按照插入的顺序存储，可以通过索引访问，顺序不会改变（除非显式调整）。
- **允许重复元素：**
  - `ArrayList` 允许存储重复的元素。
- **支持随机访问：**
  - 因为底层是数组，`ArrayList` 支持快速随机访问，时间复杂度为$ O(1)$。
- **线程不安全：**
  - `ArrayList` 是非同步的，因此在多线程环境下需要手动同步（可以使用 `Collections.synchronizedList()` 或 `CopyOnWriteArrayList` 替代）。

### 常见方法

#### 构造方法

- `public ArrayList()`：创建一个默认初始容量为 10 的空 `ArrayList`
- `public ArrayList(int initialCapacity)`：创建一个具有指定初始容量的空 `ArrayList`
- `public ArrayList(Collection<? extends E> c)`：创建一个包含指定集合中所有元素的 `ArrayList`，按照集合的迭代器顺序。

#### 添加元素

- `boolean add(E e)`：将指定的元素添加到列表的末尾
- `void add(int index, E element)`：将指定的元素插入到列表的指定位置
- `boolean addAll(Collection<? extends E> c)`：将指定集合中的所有元素添加到当前列表的末尾
- `boolean addAll(int index, Collection<? extends E> c)`：将指定集合中的所有元素插入到当前列表的指定位置。

#### 删除元素

- `void clear()`：删除全部元素
- `E remove(int index)`：删除列表中指定位置的元素
- `boolean remove(Object o)`：删除列表中第一次出现的指定元素。如果列表中没有该元素，则不做任何操作。
- `boolean removeAll(Collection<?> c)`：删除当前列表中所有与指定集合中的元素相同的元素
- `void removeRange(int from,int to)`:删除索引[from，to）之间的元素

#### 判断元素

- `boolean contains(Object o)`：判断列表中是否包含指定的元素
- `boolean containsAll(Collection<?> c)`：判断列表是否包含指定集合中的所有元素

#### 修改元素

- `E set(int index, E element)`：用指定的元素替换列表中指定位置的元素

#### 访问元素

- `E get(int index)`：返回指定位置的元素
- `int indexOf(Object o)`：返回指定元素在列表中的第一次出现位置的索引。如果列表中没有该元素，则返回 `-1`
- `int lastIndexOf(Object o)`：返回指定元素在列表中的最后一次出现位置的索引。如果列表中没有该元素，则返回 `-1`

#### 获取大小

- `int size()`：返回列表中元素的数量
- `boolean isEmpty()`：判断列表是否为空
- `void ensureCapacity(int minCapacity)`：确保列表能够容纳至少指定数量的元素，不会导致扩容。

### 扩容机制

#### 源码分析

- 往 `ArrayList` 中添加元素时会有 `ensureCapacityInternal` 的判断

  ```java
  public boolean add(E e) {
      ensureCapacityInternal(size + 1);  // Increments modCount!!
      elementData[size++] = e;
      return true;
  }
  ```

- `ensureCapacityInternal` 内部会调用 `ensureExplicitCapacity` 方法，若 `minCapacity - elementData.length > 0` 即容量不够了，则会调用 grow 方法：

  ```java
  /**
   * 检查并确保集合容量足够，如果需要则增加集合容量。
   *
   * @param minCapacity 所需最小容量
   */
  private void ensureExplicitCapacity(int minCapacity) {
      // 检查是否超出了数组范围，确保不会溢出
      if (minCapacity - elementData.length > 0)
          // 如果需要增加容量，则调用 grow 方法
          grow(minCapacity);
  }
  ```

- `grow` 扩容逻辑

  ```java
   /**
   * 扩容 ArrayList 的方法，确保能够容纳指定容量的元素
   * @param minCapacity 指定容量的最小值
   */
  private void grow(int minCapacity) {
      // 检查是否会导致溢出，oldCapacity 为当前数组长度
      int oldCapacity = elementData.length;
      int newCapacity = oldCapacity + (oldCapacity >> 1); // 扩容至原来的1.5倍
      if (newCapacity - minCapacity < 0) // 如果还是小于指定容量的最小值
          newCapacity = minCapacity; // 直接扩容至指定容量的最小值
      if (newCapacity - MAX_ARRAY_SIZE > 0) // 如果超出了数组的最大长度
          newCapacity = hugeCapacity(minCapacity); // 扩容至数组的最大长度
      // 将当前数组复制到一个新数组中，长度为 newCapacity
      elementData = Arrays.copyOf(elementData, newCapacity);
  }
  ```

#### 总结

当 `ArrayList` 中的元素数量超过其当前容量时，会触发扩容机制。

- 默认情况下，ArrayList 的初始容量为 10。

- 当发生扩容时，`ArrayList` 会创建一个新的数组，其容量为原数组的 1.5 倍（即 `oldCapacity + (oldCapacity >> 1)`），若还是小于指定容量的最小值会直接扩容到指定容量的最小值

- 然后将原数组中的元素复制到新数组中。复制过程是通过 `Arrays.copyOf()` 方法实现的。
- 更新引用：将ArrayList内部指向原数组的引用指向新数组。
- 完成扩容：扩容完成后，可以继续添加新元素。

### 线程安全问题

#### 为什么是线程不安全的

`ArrayList`不是线程安全的。`ArrayList`会暴露三个问题;

- 部分值为`null`（我们并没有add null进去）
- 索引越界异常
  - 线程1走到扩容那里发现当前size是n，数组容量是n+1不用扩容，cpu让出执行权
  - 线程2也发现不用扩容，这时候数组的容量就是n+1
  - 而线程1 set完之后`size++`，这时候线程2再进来`size`就是n+1，数组的大小只有n+1，而你要设置下标索引为n+1的就会越界（数组的下标索引size从0开始）；
- `size`与add的数量不符
  - 因为`size++`本身不是原子操作，可以分为三步：
    - 获取size的值
    - 将size的值加1
    - 将新的size值覆盖掉原来的
  - 线程1和线程2拿到一样的size值加完了同时覆盖，就会导致一次没有加上，所以肯定不会与`add`的数量保持一致的；

#### 解决方法

- 使用Collections类的`synchronizedList`方法将`ArrayList`包装成线程安全的`List`

  ```java
  import java.util.ArrayList;
  import java.util.Collections;
  import java.util.List;
  
  public class SynchronizedListExample {
      public static void main(String[] args) {
          List<Integer> list = Collections.synchronizedList(new ArrayList<>());
  
          // 同步块中操作列表，保证线程安全
          synchronized (list) {
              list.add(1);
              list.add(2);
              System.out.println(list);
          }
      }
  }
  ```

  

- 使用线程安全的替代类`CopyOnWriteArrayList`