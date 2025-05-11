---
date : '2025-05-05T19:01:20+08:00'
draft : false
title : '行为型设计模式'
image : ""
categories : ["设计模式"]
tags : ["后端开发"]
description : "行为型设计模式的理解"
math : true
---
## 策略模式

在策略模式（Strategy Pattern）中一个类的行为或其算法可以在运行时更改。它定义了一系列算法，并将每个算法封装起来，使它们可以相互替换，让算法独立于使用它的客户端（调用方）而变化。主要目的是为了解耦多个策略，并方便调用方在针对不同场景灵活切换不同的策略。

### 特点

- **算法封装**：将算法的实现与使用算法的代码分离，通过封装提高代码的灵活性和可扩展性。
- **动态替换**：可以在运行时选择和替换算法。
- **遵循开闭原则**：新增策略无需修改现有代码。

### 组成

- **策略接口（Strategy）**：定义算法的通用接口。
- **具体策略（ConcreteStrategy）**：实现具体的算法。
- **上下文类（Context）**：持有策略接口的引用，调用具体策略的方法

### 具体实现

```java
// 策略接口
interface Strategy {
    void execute();
}

// 具体策略A
class ConcreteStrategyA implements Strategy {
    @Override
    public void execute() {
        System.out.println("Executing Strategy A");
    }
}

// 具体策略B
class ConcreteStrategyB implements Strategy {
    @Override
    public void execute() {
        System.out.println("Executing Strategy B");
    }
}

// 上下文类
class Context {
    private Strategy strategy;

    public void setStrategy(Strategy strategy) {
        this.strategy = strategy;
    }

    public void executeStrategy() {
        if (strategy != null) {
            strategy.execute();
        } else {
            System.out.println("No strategy set");
        }
    }
}

// 客户端
public class Main {
    public static void main(String[] args) {
        Context context = new Context();

        Strategy strategyA = new ConcreteStrategyA();
        Strategy strategyB = new ConcreteStrategyB();

        context.setStrategy(strategyA);
        context.executeStrategy(); // Output: Executing Strategy A

        context.setStrategy(strategyB);
        context.executeStrategy(); // Output: Executing Strategy B
    }
}
```

## 观察者模式

观察者模式（发布订阅模式）是一种行为型设计模式，**用于定义对象之间的一种一对多的依赖关系**，使得一个对象状态发生变化时，所有依赖它的对象都会收到通知并自动更新。它的目的就是将观察者和被观察者代码解耦，使得一个对象或者说事件的变更，让不同观察者可以有不同的处理，非常灵活，扩展性很强，是事件驱动编程的基础。

### 特点

- **松耦合**：观察者和被观察者之间是松耦合的，便于扩展和维护。
- **动态订阅**：可以动态添加或移除观察者，灵活性高。
- **单向通信**：被观察者通知观察者，观察者不能反向修改被观察者的状态。

### 结构

- Subject（抽象主题/被观察者）：状态发生变化时，通知所有注册的观察者。
- Observer（抽象观察者）：接收来自主题的更新通知，并进行相应的操作。
- ConcreteSubject（具体主题）：实现具体的主题对象，保存需要被观察的状态。
- ConcreteObserver（具体观察者）：实现具体的观察者对象，更新自己以与主题的状态同步。

### 具体实现

```java
import java.util.ArrayList;
import java.util.List;

// 抽象观察者
interface Observer {
    void update(String message);
}

// 抽象被观察者接口
interface Subject {
    void addObserver(Observer observer);
    void removeObserver(Observer observer);
    void notifyObservers();
}

// 具体被观察者
class ConcreteSubject implements Subject {
    private List<Observer> observers = new ArrayList<>();
    private String state;

    @Override
    public void addObserver(Observer observer) {
        observers.add(observer);
    }

    @Override
    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }

    @Override
    public void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(state);
        }
    }

    public void setState(String state) {
        this.state = state;
        notifyObservers();
    }
}

// 具体观察者
class ConcreteObserver implements Observer {
    private String name;

    public ConcreteObserver(String name) {
        this.name = name;
    }

    @Override
    public void update(String message) {
        System.out.println(name + " received update: " + message);
    }
}

// 客户端
public class Main {
    public static void main(String[] args) {
        ConcreteSubject subject = new ConcreteSubject();

        Observer observer1 = new ConcreteObserver("Observer1");
        Observer observer2 = new ConcreteObserver("Observer2");

        subject.addObserver(observer1);
        subject.addObserver(observer2);

        subject.setState("New State 1");
        subject.setState("New State 2");
    }
}
```

