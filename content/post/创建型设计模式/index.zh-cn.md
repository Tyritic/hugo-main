---
date : '2025-05-05T10:53:36+08:00'
draft : false
title : '创建型设计模式'
image : ""
categories : ["设计模式"]
tags : ["后端开发"]
description : "创建型设计模式的常见实现和理解"
math : true
---
## 单例模式

单例模式（Singleton Pattern）提供了一种创建对象的最佳方式。这种模式涉及到一个单一的类，该类负责创建自己的对象，同时确保只有单个对象被创建。这个类提供了一种访问其唯一的对象的方式，可以直接访问，不需要实例化该类的对象。**它确保一个类在整个程序运行过程中只有一个实例，并提供全局访问点以获取该实例**。

### 特点

- **唯一性**：类的实例在整个程序生命周期内只存在一个。
- **全局访问**：提供一个全局访问点，让所有代码可以访问同一个实例。
- **延迟加载**：可以延迟实例化，在需要时才创建实例（如使用懒汉式实现）。

### 实现方式

主要实现方式有如下方式

- **饿汉式**：实例在类加载时就创建，线程安全，但如果实例初始化较重或没有被使用会浪费资源。
- **懒汉式**：实例在首次访问时创建，节约资源，但需要确保线程安全。
- **双重检查锁定**：在懒汉式的基础上优化，直接加锁效率太低，双重检查锁只在第一次检查实例为空时加锁，提高性能。
- **静态内部类**：利用类加载机制实现懒加载和线程安全，推荐使用。

#### 饿汉式实现

```java
public class Singleton {
    private static final Singleton instance = new Singleton(); //在类加载时就立即创建了这个唯一的实例

    private Singleton() {}

    public static Singleton getInstance() {
        return instance;
    }
}
```

- 定义一个私有的、静态的、不可更改（final）的类实例，在类加载时就立即创建了这个唯一的实例
- 构造函数被定义为**私有的**，这样外部类无法通过 **`new Singleton()`** 来创建新对象
- 提供一个公共的静态方法来获取唯一实例
  - 饿汉式特点：类加载时就立即创建了这个唯一的实例

#### 懒汉式实现

```java
public class Singleton {
    private static Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}
```

- 定义一个私有的、静态的、不可更改（final）的类实例，初始值为null，表示尚未初始化
- 构造函数被定义为**私有的**，这样外部类无法通过 **`new Singleton()`** 来创建新对象
- 提供一个 **公共的静态方法**，用于获取唯一实例
  - **懒加载特性**：只有在第一次调用 **`getInstance()`** 时才会创建对象
  - 如果已经创建过了，后续调用直接返回该实例

线程不安全问题

在多线程环境下，可能出现两个线程同时进入 **`if (instance == null)`** 判断，结果都创建了对象，破坏了单例模式。结果导致创建了两个实例

#### 双重锁定检查

```java
public class Singleton {  
    private volatile static Singleton singleton;  
    private Singleton (){}  
    public static Singleton getSingleton() {  
    if (singleton == null) {  
        synchronized (Singleton.class) {  
            if (singleton == null) {  
                singleton = new Singleton();  
            }  
        }  
    }  
    return singleton;  
    }  
}
```

- 定义一个私有的、静态的、不可更改（final），共享（volatile）的类实例，初始值为null，表示尚未初始化
  - **`volatile`** ：防止指令重排，确保在多线程下对象创建过程的可见性，保证不会有半初始化的对象被看见
- 构造函数被定义为**私有的**，这样外部类无法通过 **`new Singleton()`** 来创建新对象
- 提供一个 **公共的静态方法**，用于获取唯一实例
  - **懒加载特性**：只有在第一次调用 **`getInstance()`** 时才会创建对象
  - 第一次非同步检查 **`singleton == null`** 提高性能：如果已经创建了实例，就直接返回，避免进入同步块。
  - 第二次**加锁**进行同步检查再次判断 **`singleton == null`**

### 使用场景

在 **Spring Boot** 中，单例模式是 **默认的 Bean 作用域**，也就是说，你在使用 **`@Component`**、**`@Service`**、**`@Repository`**、**`@Controller`** 等注解时，Spring **默认就以单例方式管理它们的实例**

## 工厂模式

工厂模式（Factory Pattern）提供了一种创建对象的方式，使得创建对象的过程与使用对象的过程分离。工厂模式提供了一种创建对象的方式，而无需指定要创建的具体类。通过使用工厂模式，可以将对象的创建逻辑封装在一个工厂类中，而不是在客户端代码中直接实例化对象，这样可以提高代码的可维护性和可扩展性。

### 特点

- 优点
  - 调用者只需要知道对象的名称即可创建对象。
  - 扩展性高，如果需要增加新产品，只需扩展一个工厂类即可。
  - 屏蔽了产品的具体实现，调用者只关心产品的接口。
- 缺点
  - 每次增加一个产品时，都需要增加一个具体类和对应的工厂，使系统中类的数量成倍增加，增加了系统的复杂度和具体类的依赖，不符合开闭原则

### 结构

- 抽象产品（Abstract Product）：定义了产品的共同接口或抽象类。它可以是具体产品类的父类或接口，规定了产品对象的共同方法。
- 具体产品（Concrete Product）：实现了抽象产品接口，定义了具体产品的特定行为和属性。
- 抽象工厂（Abstract Factory）：声明了创建产品的抽象方法，可以是接口或抽象类。它可以有多个方法用于创建不同类型的产品。
- 具体工厂（Concrete Factory）：实现了抽象工厂接口，负责实际创建具体产品的对象。

![简单工厂模式的UML图](AB6B814A-0B09-4863-93D6-1E22D6B07FF8.jpg)

### 具体实现

```java
// 抽象产品
public interface Shape {
   void draw();
}
// 具体产品
public class Rectangle implements Shape {
 
   @Override
   public void draw() {
      System.out.println("Inside Rectangle::draw() method.");
   }
}
public class Square implements Shape {
 
   @Override
   public void draw() {
      System.out.println("Inside Square::draw() method.");
   }
}
public class Circle implements Shape {
 
   @Override
   public void draw() {
      System.out.println("Inside Circle::draw() method.");
   }
}
// 具体工厂
public class ShapeFactory {
    
   //使用 getShape 方法获取形状类型的对象
   public Shape getShape(String shapeType){
      if(shapeType == null){
         return null;
      }        
      if(shapeType.equalsIgnoreCase("CIRCLE")){
         return new Circle();
      } else if(shapeType.equalsIgnoreCase("RECTANGLE")){
         return new Rectangle();
      } else if(shapeType.equalsIgnoreCase("SQUARE")){
         return new Square();
      }
      return null;
   }
}
// 使用工厂模式创建对象
public class FactoryPatternDemo {
 
   public static void main(String[] args) {
      ShapeFactory shapeFactory = new ShapeFactory();
 
      //获取 Circle 的对象，并调用它的 draw 方法
      Shape shape1 = shapeFactory.getShape("CIRCLE");
 
      //调用 Circle 的 draw 方法
      shape1.draw();
 
      //获取 Rectangle 的对象，并调用它的 draw 方法
      Shape shape2 = shapeFactory.getShape("RECTANGLE");
 
      //调用 Rectangle 的 draw 方法
      shape2.draw();
 
      //获取 Square 的对象，并调用它的 draw 方法
      Shape shape3 = shapeFactory.getShape("SQUARE");
 
      //调用 Square 的 draw 方法
      shape3.draw();
   }
}
```

## 抽象工厂模式

抽象工厂模式（Abstract Factory Pattern）是围绕一个超级工厂创建其他工厂。该超级工厂又称为其他工厂的工厂。在抽象工厂模式中，接口是负责创建一个相关对象的工厂，不需要显式指定它们的类。每个生成的工厂都能按照工厂模式提供对象。抽象工厂模式提供了一种创建一系列相关或相互依赖对象的接口，而无需指定具体实现类。通过使用抽象工厂模式，可以将客户端与具体产品的创建过程解耦，使得客户端可以通过工厂接口来创建一族产品。

### 特点

和简单工厂模式的区别：工厂模式**关注的是创建单一类型对象**，定义一个抽象方法，由子类实现具体对象的实例化。抽象工厂模式**关注的是创建一族相关对象**，提供一个接口来创建一组相关的或互相依赖的对象，而无需指定它们的具体类。

### 应用实例

假设有不同类型的衣柜，每个衣柜（具体工厂）只能存放一类衣服（成套的具体产品），如商务装、时尚装等。每套衣服包括具体的上衣和裤子（具体产品）。所有衣柜都是衣柜类（抽象工厂）的具体实现，所有上衣和裤子分别实现上衣接口和裤子接口（抽象产品）。

### 结构

- 抽象工厂（Abstract Factory）：声明了一组用于创建产品对象的方法，每个方法对应一种产品类型。抽象工厂可以是接口或抽象类。
- 具体工厂（Concrete Factory）：实现了抽象工厂接口，负责创建具体产品对象的实例。
- 抽象产品（Abstract Product）：定义了一组产品对象的共同接口或抽象类，描述了产品对象的公共方法。
- 具体产品（Concrete Product）：实现了抽象产品接口，定义了具体产品的特定行为和属性。

### 具体实现

```java

// 抽象产品A
public interface ProductA {
    void use();
}

// 具体产品A1
public class ConcreteProductA1 implements ProductA {
    @Override
    public void use() {
        System.out.println("Using ConcreteProductA1");
    }
}

// 具体产品A2
public class ConcreteProductA2 implements ProductA {
    @Override
    public void use() {
        System.out.println("Using ConcreteProductA2");
    }
}

// 抽象产品B
public interface ProductB {
    void eat();
}

// 具体产品B1
public class ConcreteProductB1 implements ProductB {
    @Override
    public void eat() {
        System.out.println("Eating ConcreteProductB1");
    }
}

// 具体产品B2
public class ConcreteProductB2 implements ProductB {
    @Override
    public void eat() {
        System.out.println("Eating ConcreteProductB2");
    }
}

// 抽象工厂
public interface AbstractFactory {
    ProductA createProductA();
    ProductB createProductB();
}

// 具体工厂1
public class ConcreteFactory1 implements AbstractFactory {
    @Override
    public ProductA createProductA() {
        return new ConcreteProductA1();
    }

    @Override
    public ProductB createProductB() {
        return new ConcreteProductB1();
    }
}

// 具体工厂2
public class ConcreteFactory2 implements AbstractFactory {
    @Override
    public ProductA createProductA() {
        return new ConcreteProductA2();
    }

    @Override
    public ProductB createProductB() {
        return new ConcreteProductB2();
    }
}

// 使用抽象工厂创建产品
public class Client {
    public static void main(String[] args) {
        AbstractFactory factory1 = new ConcreteFactory1();
        ProductA productA1 = factory1.createProductA();
        ProductB productB1 = factory1.createProductB();
        productA1.use();
        productB1.eat();

        AbstractFactory factory2 = new ConcreteFactory2();
        ProductA productA2 = factory2.createProductA();
        ProductB productB2 = factory2.createProductB();
        productA2.use();
        productB2.eat();
    }
}
```

## 建造者模式

建造者模式是一种创建型设计模式，**用于将复杂对象的构建过程与其表示分离**。通过使用建造者模式，可以一步一步地创建一个复杂的对象，同时允许不同的建造者创建不同的对象表示。

### 特点

- 分离构建过程和表示，使得构建过程更加灵活，可以构建不同的表示。
- 可以更好地控制构建过程，隐藏具体构建细节。
- 代码复用性高，可以在不同的构建过程中重复使用相同的建造者。

### 结构

- **产品（Product）**：要构建的复杂对象。产品类通常包含多个部分或属性。
- **抽象建造者（Builder）**：定义了构建产品的抽象接口，包括构建产品的各个部分的方法。
- **具体建造者（Concrete Builder）**：实现抽象建造者接口，具体确定如何构建产品的各个部分，并负责返回最终构建的产品。
- **指导者（Director）**：负责调用建造者的方法来构建产品，指导者并不了解具体的构建过程，只关心产品的构建顺序和方式。

### 具体实现

```java
// 产品类
class Product {
    private String partA;
    private String partB;

    public void setPartA(String partA) {
        this.partA = partA;
    }

    public void setPartB(String partB) {
        this.partB = partB;
    }

    @Override
    public String toString() {
        return "Product [PartA=" + partA + ", PartB=" + partB + "]";
    }
}

// 抽象建造者
abstract class Builder {
    protected Product product = new Product();

    public abstract void buildPartA();
    public abstract void buildPartB();

    public Product getResult() {
        return product;
    }
}

// 具体建造者
class ConcreteBuilder extends Builder {
    @Override
    public void buildPartA() {
        product.setPartA("Custom Part A");
    }

    @Override
    public void buildPartB() {
        product.setPartB("Custom Part B");
    }
}

// 指挥者
class Director {
    private Builder builder;

    public Director(Builder builder) {
        this.builder = builder;
    }

    public void construct() {
        builder.buildPartA();
        builder.buildPartB();
    }
}

// 客户端
public class Main {
    public static void main(String[] args) {
        Builder builder = new ConcreteBuilder();
        Director director = new Director(builder);
        director.construct();

        Product product = builder.getResult();
        System.out.println(product); 
        // Output: Product [PartA=Custom Part A, PartB=Custom Part B]
    }
}
```

