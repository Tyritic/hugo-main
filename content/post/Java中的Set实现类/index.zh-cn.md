---
date : '2024-11-25T10:21:08+08:00'
draft : false
title : 'Java中的Set实现类'
image : ""
categories : ["Java集合","互联网面试题"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## HashSet类

**`HashSet`** 是 Java 集合框架中的一个实现类，属于 `Set` 接口的一种实现，基于**哈希表**来存储数据。它不允许存储重复元素，并且不保证元素的顺序。

### 特点

- **无重复元素**：
  - **`HashSet`** 使用哈希算法来存储元素，保证集合中没有重复的元素。
  
  - 元素的唯一性由 **`equals()`** 和 **`hashCode()`** 方法决定。
  
- **无序存储**：
  - **`HashSet`** 不保证元素的存储顺序，与插入顺序无关。

- **允许存储一个 `null` 值**：
  - 只能包含一个 **`null`** 值。

- **非线程安全**：
  - 默认情况下，**`HashSet`** 不是线程安全的。
- **性能高效**：
  - 添加、删除和查找操作的时间复杂度为 $O(1)$，但需要良好的哈希算法来避免哈希冲突。

### 注意事项

- 必须同时重写**`hashCode()`**方法和**`equal()`**方法
  - 通过 **`hashCode()`** 方法快速找到存储位置（哈希桶）。
  - 再通过 **`equals()`** 方法检查对象是否相等，避免重复存储。
- **`hashCode()`**方法默认根据地址值计算，**`equal()`**方法默认根据地址值判断对象是否相同

### 底层原理

**`HashSet`** 的底层是由一个 **`HashMap`** 实现的，它将需要存储的元素作为 **`HashMap`** 的键（`key`），而值（**`value`**）则是一个固定的常量 **`PRESENT`**。

#### 去重原理

**`HashSet`** 是基于 **哈希表** 实现的集合类，它的去重功能依赖于两个方法：

- **`hashCode()` 方法**：用于快速定位存储位置（哈希桶）。
- **`equals`() 方法**：用于确定逻辑相等性（是否是重复元素）。

当调用 **`HashSet`** 的 **`add()`** 方法时，具体过程如下：

1. **计算哈希值**：
   - 调用元素的 **`hashCode()`** 方法，计算出该元素的哈希值，用于确定其存储位置（哈希桶）。
2. **定位哈希桶**：
   - 根据哈希值找到对应的哈希桶。
3. **检查冲突**：
   - 如果桶中已经有一个或多个元素（两个对象具有相同的哈希值，发生哈希冲突），则调用元素的**`equals()`**方法，与桶中已有元素逐一比较：
     - 如果 **`equals()`** 返回 **`true`**，说明两个对象逻辑相等，不添加新元素，去重成功。
     - 如果 **`equals()`** 返回 **`false`**，说明不是重复元素，将新元素添加到桶中。
4. **存储元素**：
   - 如果桶中没有冲突（即不存在相同的哈希值和 **`equals()`** 相等的对象），直接存储该元素。

```java
import java.util.HashSet;
import java.util.Objects;

class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age && Objects.equals(name, person.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }

    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
}

public class HashSetExample {
    public static void main(String[] args) {
        HashSet<Person> set = new HashSet<>();

        Person p1 = new Person("Alice", 25);
        Person p2 = new Person("Alice", 25); // 与 p1 逻辑相等
        Person p3 = new Person("Bob", 30);

        set.add(p1);
        set.add(p2); // 不会添加，因为 p1 和 p2 逻辑相等
        set.add(p3);

        System.out.println("HashSet contains:");
        for (Person p : set) {
            System.out.println(p);
        }
    }
}
```

#### 扩容机制

**初始容量**

- **`HashSet`** 的底层 **`HashMap`** 默认初始容量为 **16**。
- 如果在创建 **`HashSet`** 时指定了初始容量，则会根据该容量初始化底层的 **`HashMap`**。

**负载因子**

- 默认负载因子为 **0.75**。
- 负载因子是一个用来衡量哈希表满的程度的指标。
  - 当哈希表中的元素个数达到 `容量 × 负载因子` 时，触发扩容。

**扩容条件**

当 **`HashSet`** 中的元素数量达到容量的 **75%** 时（即 `size ≥ capacity × loadFactor`），底层的 **`HashMap`** 会触发扩容操作

**扩容过程**

- **容量翻倍**：每次扩容时，**`HashMap`** 的容量会 **翻倍**。
- **重新哈希**：扩容后，所有已有元素需要重新计算哈希值并分配到新的桶中
- **迁移数据**：将原哈希表中的元素迁移到新的哈希表中
  - 遍历旧哈希表中的每个桶。
  - 对每个桶中的元素重新计算哈希值，将其分配到新哈希表中

### 常见方法

#### 构造方法

- **`public HashSet()`**：创建一个空的 **`HashSet`**，默认容量为 **16**，负载因子为 **0.75**。
- **`public HashSet(int initialCapacity)`**：创建一个具有指定初始容量的空 **`HashSet`**。
- **`public HashSet(int initialCapacity, float loadFactor)`**：创建一个具有指定初始容量和负载因子的空 **`HashSet`**。
- **`public HashSet(Collection<? extends E> c)`**：创建一个包含指定集合中所有元素的 **`HashSet`**

#### 添加元素

- **`public boolean add(E e)`**：如果元素不存在，则添加成功并返回 **`true`**；否则返回 **`false`**。
- **`public boolean addAll(Collection<? extends E> c)`**：将指定集合中的所有元素添加到当前 **`HashSet`**。

#### 删除元素

- **`public boolean remove(Object o)`**：如果集合中存在该元素，则移除并返回 **`true`**；否则返回 **`false`**。
- **`public boolean removeAll(Collection<?> c)`**：从当前集合中移除指定集合中的所有元素
- **`public void clear()`**：移除集合中的所有元素

#### 查询元素

- **`public boolean contains(Object o)`**：如果集合中存在指定的元素，则返回 **`true`**
- **`public boolean containsAll(Collection<?> c)`**：如果当前集合包含指定集合中的所有元素，则返回 **`true`**

#### 集合大小

- **`public boolean isEmpty()`**：如果集合为空，则返回 **`true`**
- **`public int size()`**：返回集合中的元素数量

#### 集合运算

- **并集（Union）** 将两个集合的所有元素合并在一起，去重后返回新集合
  - **`public boolean addAll(Collection<? extends E> c)`**
  - 将指定集合中的所有元素添加到当前集合中
- **交集（Intersection）** 将两个集合中共同的元素取出来
  - **`public boolean retainAll(Collection<?> c)`**
  - 只保留当前集合和指定集合中的交集部分
- **差集（Difference）** 从一个集合中去除另一个集合中的元素
  - **`public boolean removeAll(Collection<?> c)`**
  - 从当前集合中移除与指定集合相交的元素

### 与HashMap的关系

实际上**`HashSet`** 内部使用 **`HashMap`** 来实现，**`HashSet`** 中的元素实际上存储在 **`HashMap`** 的键中，而所有的值都是一个常量对象 **`PRESENT`**。因此，**`HashSet`** 仅操作 **`HashMap`** 的键部分。

## LinkedHashSet类

**`LinkedHashSet`** 是 Java 集合框架中的一个类，它实现了 **`Set`** 接口，并且结合了 **`HashSet`** 和链表的特性。它是 **`HashSet`** 的一个变种，具有元素唯一性和顺序性的特点。**`LinkedHashSet`** 维护了元素插入的顺序（即按插入顺序遍历元素），这使得它在保持 **`Set`** 接口的特性（元素唯一性）的同时，还能提供元素的顺序遍历。

### 特点

- **元素唯一性**：
  - **`LinkedHashSet`** 和 **`HashSet`** 一样，保证集合中的元素不重复，即不允许重复元素。
  
- **保持插入顺序**：

  - 与 **`HashSet`** 不同的是，**`LinkedHashSet`** 维护了元素的插入顺序。也就是说，元素是按照它们被添加到集合中的顺序来存储的。
  - 这使得 **`LinkedHashSet`** 在遍历时能按照元素的插入顺序进行。

- **基于哈希表和链表实现**：
- 它继承了 **`HashSet`**，因此内部使用哈希表来存储元素，同时使用链表来记录元素的插入顺序。
  
- 使用哈希表来实现高效的查找、插入和删除操作。

### 底层原理

#### 插入顺序的维护

**`LinkedHashSet`** 通过内部维护一个 **双向链表** 来保持元素的插入顺序。每个元素在哈希表中不仅存储它的哈希值，还会保存指向前一个元素和后一个元素的引用。这使得集合可以按照插入顺序遍历元素。

**插入时创建新节点**：

- 当调用 **`add(E e)`** 方法插入一个新元素时，**`LinkedHashSet`** 会先通过哈希表检查该元素是否已存在。如果不存在，它会将元素插入到哈希表中，并在双向链表的末尾添加该元素。

- 每次添加元素时，它会被插入到链表的末尾，并通过双向链表保持元素之间的顺序。这样，在遍历 **`LinkedHashSet`** 时，元素会按照它们被插入的顺序输出。

## TreeSet类

### 特点

- **排序功能**：
  - **`TreeSet`** 中的元素是自动按升序排序的。它使用 **自然顺序**（元素必须实现 **`Comparable`** 接口）或者提供的 **`Comparator`** 对元素进行排序。

- **元素唯一性**：
  - 与 **`HashSet`** 一样，**`TreeSet`** 保证集合中的元素不重复，即不允许添加重复元素。

- **基于红黑树实现**：

  - **`TreeSet`** 是基于 **红黑树** 数据结构实现的。红黑树是一种自平衡的二叉查找树，能够保证树的高度始终处于对数级别，从而保证了操作的效率。

  - 由于使用了红黑树，**`TreeSet`** 可以在对元素进行插入、删除、查找时提供 $O(log n)$ 的时间复杂度。

- **不允许 `null` 元素**：
  - **`TreeSet`** 不允许 **`null`** 元素。如果尝试向 **`TreeSet`** 中添加 **`null`** 元素，将会抛出 **`NullPointerException`**。

- **线程不安全**：
  - **`TreeSet`** 不是线程安全的。如果多个线程同时访问一个 **`TreeSet`**，并且至少有一个线程修改了该集合，则必须在外部进行同步。

- **访问和操作性能**：
  - **`TreeSet`** 的常见操作（如 **`add()`**、**`remove()`**、**`contains()`**）的时间复杂度是 $O(log n)$，这是因为它使用了红黑树来存储元素。

### 排序规则

- 对于数值类型默认采用升序排列
- 对于字符类型默认采用ASCII码排序
- 对于字符串类型采用字典序进行排列
- 自定义规则
  - 让元素实现**`Comparable`**接口
  - 创建集合时传递**`Comparator`**指定规则