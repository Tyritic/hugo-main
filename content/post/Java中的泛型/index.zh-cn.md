---
date : '2024-11-16T09:46:03+08:00'
draft : false
title : 'Java中的泛型'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## 泛型的定义

泛型是 Java 编程语言中的一个重要特性，它允许类、接口和方法在定义时使用一个或多个类型参数，这些类型参数在使用时可以被指定为具体的类型。

泛型的主要目的是在编译时提供更强的类型检查，并且在编译后能够保留类型信息，避免了在运行时出现类型转换异常。

## 泛型的作用

- **类型安全**：泛型允许在编译时进行类型检查，确保在使用集合或其他泛型类时，不会出现类型不匹配的问题，减少了运行时的 `ClassCastException` 错误。
- **代码重用**：泛型使代码可以适用于多种不同的类型，减少代码重复，提升可读性和维护性。
- **消除显式类型转换**：泛型允许在编译时指定类型参数，从而消除了运行时需要显式类型转换的麻烦。

## 泛型的使用

### 泛型类

类的成员变量的类型不确定，可以使用泛型表示

**语法格式**

```java
class className<T>{
    
}
```

**示例代码**

```java
// 泛型类的定义
public class Box<T> {
    private T value;

    public void setValue(T value) {
        this.value = value;
    }

    public T getValue() {
        return value;
    }
}

// 使用泛型类
Box<Integer> intBox = new Box<>();
intBox.setValue(10);
Integer intValue = intBox.getValue();
System.out.println(intValue); // 输出: 10

Box<String> stringBox = new Box<>();
stringBox.setValue("Hello, Generic!");
String strValue = stringBox.getValue();
System.out.println(strValue); // 输出: Hello, Generic!
```

### 泛型接口

用类型参数来参数化接口的方法和字段，泛型类和非泛型类都可以实现泛型接口，只是非泛型类给泛型接口提供具体类型

**示例代码**

- 泛型类实现泛型接口

  ```java
  // 泛型接口的定义
  interface Pair<K, V> {
      K getKey();
      V getValue();
  }
  
  // 泛型接口的实现
  class MyPair<K, V> implements Pair<K, V> {
      private K key;
      private V value;
  
      public MyPair(K key, V value) {
          this.key = key;
          this.value = value;
      }
  
      @Override
      public K getKey() {
          return key;
      }
  
      @Override
      public V getValue() {
          return value;
      }
  }
  
  // 使用泛型接口
  Pair<String, Integer> pair = new MyPair<>("Age", 30);
  System.out.println(pair.getKey() + ": " + pair.getValue()); // 输出: Age: 30
  ```

- 非泛型类实现泛型接口

  ```java
  // 泛型接口
  interface Pair<K, V> {
      K getKey();
      V getValue();
  }
  
  // 非泛型类实现泛型接口
  class MyPair implements Pair<String, Integer> {
      private String key;
      private Integer value;
  
      public MyPair(String key, Integer value) {
          this.key = key;
          this.value = value;
      }
  
      @Override
      public String getKey() {
          return key;
      }
  
      @Override
      public Integer getValue() {
          return value;
      }
  }
  
  public class Main {
      public static void main(String[] args) {
          MyPair pair = new MyPair("Age", 30);
          System.out.println(pair.getKey() + ": " + pair.getValue());  // 输出: Age: 30
      }
  }
  ```



### 泛型方法

泛型方法是指在方法的定义中，使用类型参数。与泛型类不同的是，泛型方法的类型参数只适用于该方法，而不影响整个类。

**语法格式**

```java
访问控制符 <T> 方法返回值 方法名(形参列表){
	
}
```

**示例代码**

```java
// 泛型方法的定义
public class GenericMethodExample {
    public static <T> void printArray(T[] array) {
        for (T element : array) {
            System.out.print(element + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Integer[] intArray = {1, 2, 3};
        String[] strArray = {"Hello", "World"};
        
        // 调用泛型方法
        printArray(intArray); // 输出: 1 2 3
        printArray(strArray); // 输出: Hello World
    }
}
```

## 泛型的通配符

Java 泛型的上限定符 **用于对泛型类型参数进行范围限制** 

### 无界通配符

无界通配符表示泛型类型没有任何限制，可以接受任何类型。它适用于不关心具体类型的场景，常用于方法参数中。

**语法参数**

```java
<?>
```

**示例代码**

```java
import java.util.List;

public class WildcardExample {
    public static void printList(List<?> list) {
        for (Object obj : list) {
            System.out.println(obj);
        }
    }

    public static void main(String[] args) {
        List<String> stringList = List.of("a", "b", "c");
        List<Integer> intList = List.of(1, 2, 3);

        printList(stringList);  // 可以传递任何类型的 List
        printList(intList);
    }
}
```

### 上界通配符

**语法格式**

```java
<? extends T>
```

上界通配符限制泛型类型必须是指定类型 `T` 或 `T` 的子类。这意味着，`<? extends T>` 可以接受 `T` 类型及其所有子类型。上界通配符通常用于**读取操作，确保可以读取为 `T` 或 `T` 的子类的对象**。。

**示例代码**

```java
import java.util.List;

public class UpperBoundWildcardExample {

    public static void printNumbers(List<? extends Number> list) {
        for (Number number : list) {
            System.out.println(number);
        }
    }

    public static void main(String[] args) {
        List<Integer> intList = List.of(1, 2, 3);
        List<Double> doubleList = List.of(1.1, 2.2, 3.3);

        printNumbers(intList);  // 可以传递 List<Integer>
        printNumbers(doubleList);  // 可以传递 List<Double>
    }
}
```

### 下界通配符

**语法格式**

```java
<? super T>
```

下界通配符限制泛型类型必须是指定类型 `T` 或 `T` 的父类。`<? super T>` 适用于我们要往集合中添加元素的情况，它保证了**能够安全地将 `T` 类型及其子类型的对象放入容器中。**

**示例代码**

```java
import java.util.List;

public class LowerBoundWildcardExample {

    public static void addNumbers(List<? super Integer> list) {
        list.add(42);  // 只允许添加 Integer 或其子类型的元素
    }

    public static void main(String[] args) {
        List<Number> numberList = List.of(1, 2, 3);
        List<Object> objectList = List.of("string", 10.5);

        addNumbers(numberList);  // 可以传递 List<Number>
        addNumbers(objectList);  // 可以传递 List<Object>
    }
}
```

### 使用规则

####   `<? extends T>` 的泛型集合中只能读取数据不能写入数据

**示例**

```java
import java.util.List;

public class Test {
    public static void addToList(List<? extends Number> list) {
        for (Number num : list) {
        	System.out.println(num); // 读取是安全的
   		}
        // list.add(1); // 编译错误
        // list.add(3.14); // 编译错误
    }
}
```

**解释**

- 当使用`<? extends T>` ,泛型集合中元素的类型是 `T` 类型或 `T` 的任意子类型
- **可读取性**：`<? extends T>` 确保了集合中的每个元素至少是 `T` 类型或其子类，因此可以安全地以多态（向上转型）赋值给 `T` 类型的变量 。
- **不可写入性**：`List<? extends T>` 限定了泛型上界为 `T` 的子类，但无法保证具体是哪种类型，因此不能添加元素（除了 `null`），否则会违反类型安全性。

####   `<? super T>` 的泛型集合中只能写入数据不能读取数据

**示例**

```java
import java.util.List;
import java.util.ArrayList;

public class Test {
    public static void addToList(List<? super Integer> list) {
        list.add(10);    // 可以添加 Integer 类型的数据
        list.add(100);   // 可以继续添加 Integer 类型的数据
    }

    public static void main(String[] args) {
        List<Number> numberList = new ArrayList<>();
        addToList(numberList); // 传入 List<Number> 是安全的

        List<Object> objectList = new ArrayList<>();
        addToList(objectList); // 传入 List<Object> 也是安全的
        
        Object obj = list.get(0); // 可以读取为 Object 类型
        // Integer num = list.get(0); // 编译错误，不能直接读取为 Integer
    }
}

```

**解释**

- 当使用 `<? super T>` 时，泛型集合中元素的类型是 `T` 类型或 `T` 的任意父类型
- **可写入性**：`<? super T>` 确保了集合中的每个元素至少是 `T` 类型或其父类，因此可以安全地写入 `T` 类型及其子类的变量。
- **不可读取性**：编译器并不知道集合实际存储的具体类型，因此无法确定返回的元素类型是什么，唯一可以确定的是，所有元素至少是 `Object` 类型，因此只能将读取的元素视为 `Object`。

### **PECS 原则**

**PECS** 原则是 `Producer Extends, Consumer Super` 的缩写，帮助理解何时使用上界和下界限定符：

- **Producer Extends**：如果某个对象提供数据（即生产者），使用 `extends`（上界限定符）。
- **Consumer Super**：如果某个对象接收数据（即消费者），使用 `super`（下界限定符）。

## 类型擦除和伪泛型

Java 中的泛型被称为 **伪泛型**（**erasure**），这是因为 Java 的泛型是通过 **类型擦除（type erasure）** 实现的

### 类型擦除

#### 实现方式

**编译时**：

- **用原始类型替换泛型类型**：所有泛型类和方法会被编译为使用原始类型的代码。例如，`List<String>` 会变成 `List`，`T` 会变成 `Object`。
- **类型边界**：如果泛型类或方法有上界限制（如 `T extends Number`），那么在擦除时，`T` 会被替换为这个边界类型（例如 `Number`）。
- **类型参数的强制转换**：在泛型类和方法中，编译器会插入强制类型转换，以确保在运行时正确转换类型。

**运行时**：在运行时，Java 并不保留泛型类型信息，所有泛型类型都被转换成了原始类型。

**示例说明**

编译前

```java
public class Box<T> {
    private T value;

    public void setValue(T value) {
        this.value = value;
    }

    public T getValue() {
        return value;
    }
}

```

编译后

```java
public class Box {
    private Object value;

    public void setValue(Object value) {
        this.value = value;
    }

    public Object getValue() {
        return value;
    }
}
```



#### 作用和影响

**作用**：泛型擦除确保了 Java 代码的向后兼容性，但它也限制了在运行时对泛型类型的操作。

**影响**：

- **类型信息丢失**：由于类型擦除，无法在运行时获取泛型的实际类型，导致无法进行以下操作
  - 不能创建泛型类型的数组，不能实例化泛型类型的变量
  - 对泛型类型使用 `instanceof` 检查
- **类型转换异常**：在运行时，由于类型擦除的存在，可能会导致类型转换异常。例如，如果你错误地将 `List<Integer>` 和 `List<String>` 混用，编译时可能不会发现问题，而在运行时会导致 `ClassCastException`。
- **无法使用基本类型作为泛型**：由于类型擦除的原因，Java 泛型无法直接使用基本数据类型（如 `int`、`char` 等），只能使用它们的包装类型（如 `Integer`、`Character`）。

#### 利用反射获取泛型类型的情况

因为泛型信息保存在`class`文件中

- 成员变量的泛型
- 方法入参的泛型
- 方法返回值的泛型

#### 带来的问题

```java
public class Cmower {
    
    public static void method(ArrayList<String> list) {
        System.out.println("ArrayList<String> list");
    }

    public static void method(ArrayList<Date> list) {
        System.out.println("ArrayList<Date> list");
    }
}
```

在 Java 中，泛型是在编译时擦除的，这意味着 `ArrayList<String>` 和 `ArrayList<Date>` 在编译后会变成相同的类型 `ArrayList`。

- 当方法重载时，如果两种方法的签名 **在类型擦除后相同**，就会发生冲突。
- 在这段代码中，`ArrayList<String>` 和 `ArrayList<Date>` 在类型擦除后都会变成 `ArrayList`，因此，编译器无法区分这两个方法，导致编译时发生冲突。

### 为什么是伪泛型

泛型只在**编译时**进行类型检查，**运行时**并不会保留泛型类型信息。

在**运行时**泛型根本没有起作用！**也就是说在运行的时候 JVM 获取不到泛型的信息，也会不对其做任何的约束**。

因此，虽然在 IDE 写代码的时候泛型生效了，而实际上**在运行的时候泛型的类型是被擦除的**。

一言蔽之，**Java的泛型只在编译时生效，JVM 运行时没有泛型**。
