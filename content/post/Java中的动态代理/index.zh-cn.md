---
date : '2025-01-19T20:10:12+08:00'
draft : false
title : 'Java的动态代理'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : ""
math : true
---
## 动态代理的定义

**动态代理（Dynamic Proxy）** 是 Java 提供的一种机制，它允许在运行时创建实现指定接口的代理类，而不需要在编译时编写实现类。

## 动态代理主要用途

- 简化代码：通过代理模式，可以减少重复代码，尤其是在横切关注点（如日志记录、事务管理、权限控制等）方面。
- 增强灵活性：动态代理使得代码更具灵活性和可扩展性，因为代理对象是在运行时生成的，可以动态地改变行为。
- 实现 AOP：动态代理是实现面向切面编程（AOP, Aspect-Oriented Programming）的基础，可以在方法调用前后插入额外的逻辑

## 动态代理的工作原理

1. **接口与代理**： 代理类并不是通过继承或实现接口来定义的，而是通过 `Proxy` 类在运行时动态创建。代理类会在运行时被创建，并会实现与原接口相同的方法。
2. **`InvocationHandler` 接口**： 这个接口是动态代理的核心，它定义了 `invoke()` 方法，当代理对象调用任何方法时，都会触发 `invoke()` 方法，从而可以在其中执行增强逻辑。
3. **`Proxy.newProxyInstance()` 方法**： 这是 Java 提供的用于创建动态代理实例的工具方法。通过这个方法，可以创建实现指定接口的代理对象，并指定一个 `InvocationHandler` 来处理方法的调用。

## 动态代理的实现步骤

- **定义接口**： 被代理对象必须实现一个接口。
- **处理器类实现 `InvocationHandler` 接口**： 通过 `InvocationHandler` 接口来定义代理类的逻辑，重写`invoke`方法实现对方法的拦截。
  - `Object proxy`：代理对象
  - `Method method`：调用的方法
  - `Object[] args`：传递的实参
- **主类使用 `Proxy.newProxyInstance()` 创建代理对象**： 通过 `Proxy` 类的 `newProxyInstance()` 方法创建代理对象。

## 示例

```java
// 定义接口
public interface UserService {
    void addUser(String name);
    void deleteUser(String name);
}

// 实现接口
public class UserServiceImpl implements UserService {
    @Override
    public void addUser(String name) {
        System.out.println("Adding user: " + name);
    }

    @Override
    public void deleteUser(String name) {
        System.out.println("Deleting user: " + name);
    }
}

// 处理器实现InvocationHandler接口
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public class LoggingHandler implements InvocationHandler {
    private final Object target;

    public LoggingHandler(Object target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        // 在方法执行前添加日志
        System.out.println("Method " + method.getName() + " is called with arguments: " + args[0]);
        
        // 调用真实对象的方法
        Object result = method.invoke(target, args);
        
        // 在方法执行后添加日志
        System.out.println("Method " + method.getName() + " execution completed.");
        
        return result;
    }
}

// 创建代理对象
import java.lang.reflect.Proxy;

public class ProxyExample {
    public static void main(String[] args) {
        UserService userService = new UserServiceImpl();
        
        // 创建动态代理对象
        UserService proxy = (UserService) Proxy.newProxyInstance(
                userService.getClass().getClassLoader(),
                userService.getClass().getInterfaces(),
                new LoggingHandler(userService)
        );
        
        // 使用代理对象
        proxy.addUser("Alice");
        proxy.deleteUser("Bob");
    }
}
```

