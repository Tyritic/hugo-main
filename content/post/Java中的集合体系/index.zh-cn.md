---
date : '2024-11-11T09:36:04+08:00'
draft : false
title : 'Java中的集合体系和集合遍历方式'
image : ""
categories : ["Java集合","互联网面试题"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## 集合体系结构

![体系结构示意图](1717481094793-b8ffe6ae-2ee6-4de5-b61b-8468e32bf269.webp)

- **`Collection`** 接口：单列数据，所有集合类的根接口，提供基本的集合操作方法
  - **`List`**  接口：元素有序（存储顺序与存放顺序一致），可重复有索引的集合
    - **`ArrayList`** ：基于动态数组，查询速度快，插入、删除慢，线程不安全。
    - **`LinkedList`** ：基于双向链表，插入、删除快，查询速度慢，线程不安全。
    - **`Vector`** ：线程安全的动态数组，类似于 **`ArrayList`**，但开销较大。
  - **`Set`** 接口：元素无序，不可重复，无索引的集合
    - **`HashSet`** ：基于哈希表，元素无序，不允许重复。
      - **`LinkedHashSet`** ：基于链表和哈希表，维护插入顺序，不允许重复。
    - **`TreeSet`** ：基于红黑树，元素有序（元素是按照自然顺序或提供的比较器进行排序的），不允许重复。
  - **`Queue`** 接口：表示一个先进先出的集合
    - **`PriorityQueue`** ：基于优先级堆，元素按照自然顺序或指定比较器排序。
    - **`LinkedList`** ：可以作为队列使用，支持 FIFO（先进先出）操作。
    - **`ArrayQueue`** ：基于数组实现的双端队列
- **`Map`** 接口：双列数据，保存具有映射关系的键值对
  - **`HashMap`** ：基于哈希表，键值对无序，不允许键重复，线程不安全。
  - **`LinkedHashMap`** ：基于链表和哈希表，维护插入顺序，不允许键重复。
  - **`TreeMap`** ：基于红黑树，键值对有序，不允许键重复。
  - **`Hashtable`** ：线程安全的哈希表，不允许键或值为 `null`。
  - **`ConcurrentHashMap`** ：线程安全的哈希表，适合高并发环境，不允许键或值为 **`null`**。

## `Collection`接口

**`Collection`** 接口是 Java 集合框架的根接口，定义了集合类的基本操作方法。

### 添加元素

- **`boolean add(E e)`** ：将指定的元素添加到集合中，如果集合允许该元素的添加（比如没有重复元素限制），则返回 `true`，如果集合已经包含该元素，则返回 ** `false`**
  - 向 **`List`** 集合中添加数据则方法将固定返回 **`true`** ，**`List`** 集合中允许添加重复元素
  - 向 **`Set`** 集合中添加数据若当前元素已经存在返回 **`false`**，若当前元素不存在返回`true`
- **`boolean addAll(Collection<? extends E> c)`** ：将指定集合中的所有元素添加到当前集合中
  - 如果当前集合因为某些原因没有改变（例如集合为空或元素没有添加成功），则返回 **`false`**，否则返回  **`true`**。

### 删除元素

- **`void clear()`** ：移除集合中的所有元素，使集合为空。
- **`boolean remove(Object o)`** ：从集合中移除指定的元素。
  - 如果集合中包含该元素并且成功移除，返回 **`true`**；如果元素不存在，返回 **`false`**。
- **`boolean removeAll(Collection<?> c)`**：移除集合中与指定集合相同的所有元素。
  - 如果集合因移除操作发生变化，则返回 **`true`**；如果没有任何元素被移除，则返回 **`false`**。
- **`boolean retainAll(Collection<?> c)`** ：只保留集合中与指定集合相同的元素，移除其他元素。
  - 如果集合发生变化（即移除了某些元素），则返回 **`true`**；如果没有元素被移除，则返回 **`false`**。

### 判断元素

- **`boolean contains(Object o)`** ：判断集合是否包含指定元素
  - 如果集合中包含该元素，返回 **`true`**；否则返回 **`false`**。
- **`boolean containsAll(Collection<?> c)`**：判断当前集合是否包含指定集合中的所有元素。
- **`boolean isEmpty()`**：判断集合是否为空
  - 如果集合中没有元素，返回 **`true`** ；否则返回 **`false`**。

## 遍历方法

### 迭代器

**`Iterator`** 是 Java 集合框架中用于遍历集合元素的接口，**允许开发者依次访问集合中的每一个元素，而不需要关心集合的具体实现**。它提供了一种统一的方式来遍历 **`List`**、**`Set`**  等集合类型，通常与 **`Collection`** 类接口一起使用。**`Iterator`** 只能单向遍历集合，不能向前遍历。

#### 核心方法

- **`hasNext()`** ：返回 **`true`** 表示集合中还有下一个元素，返回 **`false`** 则表示遍历完毕。
- **`next()`**：返回集合中的下一个元素，如果没有更多元素则抛出 **`NoSuchElementException`**。
- **`remove()`**：从集合中移除最近一次通过 **`next()`** 方法返回的元素，执行时只能在调用 **`next()`** 之后使用。这个方法是可选的，不是所有的实现都支持该操作。如果不支持，调用时会抛出 **`UnsupportedOperationException`**。

#### 注意事项

- 迭代器越界会报错
- 迭代器遍历完毕，指针不会复位
- 迭代器遍历时不允许使用集合的方法进行添加和删除 **（fail—fast）**，
  - 在用迭代器遍历一个集合对象时，如果线程 A 遍历过程中，线程 B 对集合对象的内容进行了修改（增加、删除、修改），则会抛出 **`Concurrent Modification Exception`**。
  - 原理：迭代器在遍历时直接访问集合中的内容，并且在遍历过程中使用一个 **`modCount`** 变量。集合在被遍历期间如果内容发生变化，就会改变 **`modCount`** 的值。每当迭代器使用 **`hashNext()/next()`** 遍历下一个元素之前，都会检测 **`modCount`** 变量是否为 expectedmodCount 值，是的话就返回遍历；否则抛出异常，终止遍历。


#### 示例

```java
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class IteratorExample {
    public static void main(String[] args) {
        // 创建一个List集合并添加元素
        List<String> list = new ArrayList<>();
        list.add("Apple");
        list.add("Banana");
        list.add("Cherry");

        // 获取集合的迭代器
        Iterator<String> iterator = list.iterator();

        // 使用迭代器遍历集合
        while (iterator.hasNext()) {
            String element = iterator.next();
            System.out.println(element);  // 输出元素

            // 删除元素（示例：删除“Banana”）
            if (element.equals("Banana")) {
                iterator.remove();  // 删除“Banana”
            }
        }

        // 打印修改后的集合
        System.out.println("Modified list: " + list);
    }
}
// 输出：
// Apple
// Banana
// Cherry
// Modified list: [Apple, Cherry]
```

#### `ListIterator`（`List` 特有的迭代器）

**`ListIterator`** 是 **`Iterator`** 的子接口，专门用于操作 **`List`** 类型集合。与 **`Iterator`** 不同，**它支持双向遍历和元素修改。**

**核心方法**

- **`hasPrevious()`**：判断是否还有前一个元素。
- **`previous()`**：返回前一个元素。
- **`add(E e)`**：向当前遍历的位置插入元素。
- **`set(E e)`**：修改当前元素。

### for-each循环

#### 语法格式

```java
for (Type item : collection) {
    // 使用 item
}
```

#### 主要特点

- 简洁性：语法更简单，减少了初始化、条件检查和更新的样板代码。**适合用于遍历数组和实现了 Iterable 接口的集合**。
- 只读访问：不提供对当前索引的访问，因此不适合需要根据索引进行复杂操作的场景。
- 安全性：在遍历过程中不能修改集合的结构（例如，不能在遍历 List 的同时添加或删除元素），否则会抛出 **`ConcurrentModificationException`**。

#### 底层实现

实际上是通过 **`Iterator`** 实现的。Java 编译器会将 **`for-each`** 循环转换为一个使用 **`Iterator`** 或索引的标准迭代过程。

### Lambda表达式遍历（forEach方法）

集合类（如 **`List`**、**`Set`**）实现了 **`Iterable`** 接口，**`Iterable`** 接口提供了一个默认的 **`forEach`** 方法，可以直接与 Lambda 表达式结合，进行遍历。

#### 语法格式

```
foreach(new Consumer<? super T> action)
{
	@Override
	public void accept(T s)
	{
		//重写
	}
}
```

