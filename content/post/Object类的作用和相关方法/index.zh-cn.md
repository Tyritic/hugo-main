---
date : '2025-01-02T14:24:41+08:00'
draft : false
title : 'Object类的作用和相关方法'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "Java中Object类的作用"
math : true
---

## 作用

Object类是Java所有类的父类，所有的Java类默认继承Object类，Object类中的所有方法都可以被Java类使用

## 常见方法

以下是 `Object` 类中的主要方法及其作用：

### 对象比较

`public boolean equals(Object obj)`

- **作用**：用于比较两个对象是否相等。默认实现比较对象的内存地址，即判断两个引用是否指向同一个对象。
- **使用**：通常会重写此方法来比较对象的内容或特定属性，以定义对象的相等性。

`public int hashCode()`

- **作用**：返回对象的哈希码，是对象的整数表示。哈希码用于支持基于哈希的集合（如 `HashMap` 和 `HashSet`）。
- **使用**：如果重写了 `equals` 方法，则通常也需要重写 `hashCode` 方法，以保证相等的对象具有相同的哈希码。

#### `hashCode`和`equals`的关系

`equals`决定了对象的**逻辑相等性**

`hashCode`决定了对象的**哈希存储方式**。

**`equals()` 方法**：

- 用于判断两个对象是否相等。默认实现是使用 `==` 比较对象的内存地址，但可以在类中重写 `equals()` 来定义自己的相等逻辑。

**`hashCode()` 方法**：

- 返回对象的哈希值，主要用于基于哈希的集合（如 `HashMap`、`HashSet`）。同一个对象每次调用 `hashCode()` 必须返回相同的值，且相等的对象必须有相同的哈希码。

#### `equals` 和 `hashCode` 的约定

- **相等对象的哈希值必须相等** ： 如果两个对象通过 `equals` 方法比较相等（`a.equals(b) == true`），那么它们的哈希值必须相同（`a.hashCode() == b.hashCode()`）

- **不相等的对象可以有相同的哈希值** ： 如果两个对象通过 `equals` 方法比较不相等（`a.equals(b) == false`），它们的哈希值不必不同，但为了提升性能，应尽量让不相等的对象有不同的哈希值。
- **哈希值不相同的对象一定不相同**

#### 编码建议

重写 `equals` 方法的时候，也要重写 `hashCode` 方法，这样才能保持条件判断的同步。

**解释**

如果仅重写 `equals` 方法而不重写 `hashCode`，会违反 `hashCode` 与 `equals` 的约定，从而导致集合类行为异常。例如：`HashSet` 基于哈希值来判断对象是否相同，哈希值不同导致它们被视为不同的对象。

### 对象转字符串

`public String toString()`

- **作用**：返回对象的字符串表示。默认实现返回对象的类名加上其哈希码的十六进制表示。
- **使用**：通常会重写此方法以提供对象的更有意义的描述。

### 反射

`public final Class<?> getClass()`

- **作用**：返回对象的运行时类（`Class` 对象）。此方法是 `Object` 类中的一个 final 方法，不能被重写。
- **使用**：可以用来获取对象的类信息，常用于反射操作。

### 多线程调度

`public void notify()`

- **作用**：唤醒在对象的监视器上等待的一个线程。该方法需要在同步块或同步方法中调用。
- **使用**：用于在多线程环境中进行线程间的通信和协调。

`public void notifyAll()`

- **作用**：唤醒在对象的监视器上等待的所有线程。该方法需要在同步块或同步方法中调用。
- **使用**：与 `notify()` 相似，但唤醒所有等待线程，用于处理多个线程之间的协作。

`public void wait()`

- **作用**：使当前线程等待，直到其他线程调用 `notify()` 或 `notifyAll()` 方法。此方法需要在同步块或同步方法中调用。
- **使用**：用于线程间的通信，线程会等待直到被唤醒或超时。

`public void wait(long timeout)`

- **作用**：使当前线程等待，直到指定的时间到期或被唤醒。超时后线程会自动被唤醒。
- **使用**：用于实现带有超时的等待机制。

`public void wait(long timeout, int nanos)`

- **作用**：使当前线程等待，直到指定的时间和纳秒数到期或被唤醒。
- **使用**：用于实现更精细的等待控制，允许指定等待时间的精确到纳秒。

### 对象拷贝

`protected Object clone()`

- **作用**：创建并返回当前对象的一个副本。默认实现是进行浅拷贝。
- **使用**：通常会重写此方法来实现深拷贝，以确保克隆对象的完整性。

### 垃圾回收

`protected void finalize()`

- **作用**：在垃圾回收器确定不存在对该对象的更多引用时调用，用于进行资源释放等清理工作。
- **使用**：不建议使用，因为它依赖于垃圾回收器的实现，可能会导致不确定的性能问题。推荐使用 `try-with-resources` 和 `AutoCloseable` 接口进行资源管理

### 示例代码

```java
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // 重写equals方法
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Person person = (Person) obj;
        return age == person.age && name.equals(person.name);
    }

    // 重写hashCode方法
    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }

    // 重写toString方法
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }

    public static void main(String[] args) {
        Person p1 = new Person("Alice", 30);
        Person p2 = new Person("Alice", 30);

        System.out.println(p1.equals(p2)); // true
        System.out.println(p1.hashCode() == p2.hashCode()); // true
        System.out.println(p1); // Person{name='Alice', age=30}
    }
}
```

