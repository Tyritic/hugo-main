---
date : '2025-05-05T16:45:49+08:00'
draft : false
title : '结构型设计模式'
image : ""
categories : ["设计模式"]
tags : ["后端开发"]
description : "结构型设计模式的基础"
math : true
---
## 适配器模式

适配器模式（Adapter Pattern）充当两个不兼容接口之间的桥梁，属于结构型设计模式。它通过一个中间件（适配器）将一个类的接口转换成客户期望的另一个接口，使原本不能一起工作的类能够协同工作。

### 特点

- **接口转换**：适配器提供一种中间层，将一个类的接口转换为客户端需要的接口。
- **解耦性**：通过适配器模式，客户端不需要修改现有的代码，即可使用不同接口的类。

### 结构

适配器模式包含以下几个主要角色：

- **目标接口（Target）**：定义客户需要的接口。
- **适配者类（Adaptee）**：定义一个已经存在的接口，这个接口需要适配。
- **适配器类（Adapter）**：实现目标接口，并通过组合或继承的方式调用适配者类中的方法，从而实现目标接口。

### 具体实现

```java
// 目标接口
interface Target {
    void request();
}

// 被适配者
class Adaptee {
    void specificRequest() {
        System.out.println("Called specificRequest from Adaptee");
    }
}

// 适配器类
class Adapter implements Target {
    private final Adaptee adaptee;

    public Adapter(Adaptee adaptee) {
        this.adaptee = adaptee;
    }

    @Override
    public void request() {
        adaptee.specificRequest();
    }
}

// 客户端
public class Main {
    public static void main(String[] args) {
        Adaptee adaptee = new Adaptee();
        Target adapter = new Adapter(adaptee);
        adapter.request(); // Output: Called specificRequest from Adaptee
    }
}
```

## 代理模式

在代理模式（Proxy Pattern）中，一个类代表另一个类的功能。代理模式通过引入一个代理对象来控制对原对象的访问。代理对象在客户端和目标对象之间充当中介，负责将客户端的请求转发给目标对象，同时可以在转发请求前后进行额外的处理。在代理模式中，我们创建具有现有对象的对象，以便向外界提供功能接口。

### 特点

- **间接访问**：客户端通过代理访问实际对象，代理对象负责对实际对象的控制。
- **功能增强**：代理对象可以在访问实际对象之前或之后添加额外的功能。
- **解耦性**：客户端不直接与实际对象交互，通过代理对象可以透明地扩展实际对象的功能。

### 结构

- **抽象主题（Subject）:**定义了真实主题和代理主题的共同接口，这样在任何使用真实主题的地方都可以使用代理主题。
- **真实主题（Real Subject）:**实现了抽象主题接口，是代理对象所代表的真实对象。客户端直接访问真实主题，但在某些情况下，可以通过代理主题来间接访问。
- **代理（Proxy）:**实现了抽象主题接口，并持有对真实主题的引用。代理主题通常在真实主题的基础上提供一些额外的功能，例如延迟加载、权限控制、日志记录等。
- **客户端（Client）:**使用抽象主题接口来操作真实主题或代理主题，不需要知道具体是哪一个实现类。

### 具体实现

```java
// 抽象主题
interface Subject {
    void request();
}

// 真实主题
class RealSubject implements Subject {
    @Override
    public void request() {
        System.out.println("RealSubject: Handling request.");
    }
}

// 代理
class ProxySubject implements Subject {
    private RealSubject realSubject;

    @Override
    public void request() {
        if (realSubject == null) {
            realSubject = new RealSubject(); // 延迟初始化
        }
        System.out.println("Proxy: Logging before delegating request.");
        realSubject.request();
        System.out.println("Proxy: Logging after delegating request.");
    }
}

// 客户端
public class Main {
    public static void main(String[] args) {
        Subject proxy = new ProxySubject();
        proxy.request();
    }
}

```

## 装饰器模式

装饰器模式（Decorator Pattern）允许向一个现有的对象添加新的功能，同时又不改变其结构。它是作为现有的类的一个包装。装饰器模式通过将对象包装在装饰器类中，以便动态地修改其行为。这种模式创建了一个装饰类，用来包装原有的类，并在保持类方法签名完整性的前提下，提供了额外的功能。

### 结构

- 抽象组件（Component）：定义了原始对象和装饰器对象的公共接口或抽象类，可以是具体组件类的父类或接口。
- 具体组件（Concrete Component）：是被装饰的原始对象，它定义了需要添加新功能的对象。
- 抽象装饰器（Decorator）：实现或者继承抽象组件，它包含了一个抽象组件对象，并定义了与抽象组件相同的接口，同时可以通过组合方式持有其他装饰器对象。
- 具体装饰器（Concrete Decorator）：实现了抽象装饰器的接口，负责向抽象组件添加新的功能。具体装饰器通常会在调用原始对象的方法之前或之后执行自己的操作。

### 具体实现

```java
// 抽象组件
interface Component {
    void operation();
}

// 具体组件
class ConcreteComponent implements Component {
    @Override
    public void operation() {
        System.out.println("ConcreteComponent operation");
    }
}

// 装饰器抽象类
abstract class Decorator implements Component {
    protected Component component;

    public Decorator(Component component) {
        this.component = component;
    }

    @Override
    public void operation() {
        component.operation();
    }
}

// 具体装饰器A
class ConcreteDecoratorA extends Decorator {
    public ConcreteDecoratorA(Component component) {
        super(component);
    }

    @Override
    public void operation() {
        super.operation();
        System.out.println("ConcreteDecoratorA added behavior");
    }
}

// 具体装饰器B
class ConcreteDecoratorB extends Decorator {
    public ConcreteDecoratorB(Component component) {
        super(component);
    }

    @Override
    public void operation() {
        super.operation();
        System.out.println("ConcreteDecoratorB added behavior");
    }
}

// 客户端
public class Main {
    public static void main(String[] args) {
        Component component = new ConcreteComponent();
        Component decoratorA = new ConcreteDecoratorA(component);
        Component decoratorB = new ConcreteDecoratorB(decoratorA);

        decoratorB.operation();
        // Output:
        // ConcreteComponent operation
        // ConcreteDecoratorA added behavior
        // ConcreteDecoratorB added behavior
    }
}
```

