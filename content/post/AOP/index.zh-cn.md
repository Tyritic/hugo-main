---
date : '2024-11-07T18:38:05+08:00'
draft : false
title : 'AOP'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发"]
description : "面向切面编程的相关理解"
---

## 概述

AOP就是是Aspect Oriented Programming(面向切面编程、面向方面编程)，其实就是面向特定方法编程

底层实现：动态代理是面向切面编程最主流的实现。而SpringAOP是Spring框架的高级技术，旨在管理bean对象的过程中，主要通过底层的动态代理机制，对特定的方法进行编程。

应用场景

- 记录操作日志
- 权限控制
- 事务管理

## 具体实现

1. 导入相关依赖

2. 编写AOP程序

   ```java
   @Component
   @Aspect
   public class TimeAspect {
   	@Around("execution()”)
       public Object recordTime(ProceedingJoinPoint proceedingJoinPoint)throws Throwable 
       	{
           	long begin=System.currentTimeMillis();
           	0bject object=proceedingJoinPoint.proceed();//调用原始方法运行
   			long end=System.currentTimeMillis();
   			log.info(proceeding]oinPoint.getsignature()+"执行耗时:{}ms",end - begin);
                 return object;
       	}
   }
   ```

   

## AOP核心概念

- 连接点（JoinPoint）：可以被AOP控制的方法(暗含方法执行时的相关信息)
- 通知（Advice）：指哪些重复的逻辑，也就是共性功能
  - 体现为被@Around()修饰的方法
- 切入点（PointCut）：匹配连接点的条件，通知仅会在切入点方法执行时被应用
  - 相关注解：@Around("execution()”)
- 切面（Aspect）：描述通知与切入点的对应关系(通知+切入点)
  - 相关注解：@Aspect用于修饰类

- 目标对象（Target）：通知所应用的对象

## AOP执行流程

1. 底层为目标对象生成代理对象
2. 在代理对象中使用通知对目标对象的连接点做功能增强
3. 在依赖注入时注入代理对象

![](微信截图_20241108095453.png)

## AOP通知

### 通知类型

- @Around:环绕通知，此注解标注的通知方法在目标方法前、后都被执行
- @Before:前置通知，此注解标注的通知方法在目标方法前披执行
- @After :后置通知，此注解标注的通知方法在目标方法后被执行，无论是否有异常都会执行
- @AfterReturning: 返回后通知，此注解标注的通知方法在目标方法后被执行，有异常不会执行
- @AfterThrowing: 异常后通知，此注解标注的通知方法发生异常后执行



{{<notice tip>}}

- @Around环绕通知需要自己调用 ProceedingJoinPoint.proceed()来让原始方法执行，其他通知不需要考虑目标方法
- 执行@Around环绕通知方法的返回值，必须指定为Object，来接收原始方法的返回值。

{{</notice>}}



### 通知顺序

当有多个切面的切入点都匹配到了目标方法，目标方法运行时，多个通知方法都会被执行

#### 不同切面类的通知顺序

- 目标方法前的通知方法：字母排名靠前的先执行
  目标方法后的通知方法：字母排名靠前的后执行
- 用注解@Order(数字) 加在切面类上来控制顺序
  - 目标方法前的通知方法:数字小的先执行
  - 目标方法后的通知方法:数字小的后执行

#### 同一个切面类的通知顺序

1. Around-Before
2. Before
3. Around-after
4. after

## 切入点表达式

切入点表达式：描述切入点方法的一种表达式
作用：主要用来决定项目中的哪些方法需要加入通知

### execution(….)根据方法的签名来匹配

execution 主要根据方法的返回值、包名、类名、方法名、方法参数等信息来匹配

语法：execution(访问修饰符? 返回值 包名.类名.?方法名(方法参数)throws 异常?) 

带?的部分可以省略

- 访问修饰符:可省略(比如:public、protected)
- 包名.类名: 可省略
- throws 异常:可省略(注意是方法上声明抛出的异常，不是实际抛出的异常)

通配符

- *：单个独立的任意符号，可以通配任意返回值、包名、类名、方法名、任意类型的一个参数，也可以通配包、类、方法名的一部分

  ```java
  execution(* com.*.service.*.update*(*))
  ```

- :：多个连续的任意符号，可以通配任意层级的包，或任意类型、任意个数的参数

  ```java
  execution(* com.itheima..Deptservice.*(..))
  ```

  

### @annotation(.):根据注解匹配

@annotation切入点表达式，用于匹配标识有特定注解的方法

语法：@annotation(全类名)

```
@Before("@annotation(com.itheima.anno.Log)")
public void before(){
	log.info("before ....");
}
```

{{<notice tip>}}

@PointCut
该注解的作用是将公共的切点表达式抽取出来，需要用到时引用该切点表达式即可

```java
@Pointcut("execution()")
public void pt(){)
@Around("pt()")
public Object recordrime(ProceedingjoinPoint joinPoint) throws Throwable {
    
}
```

注意事项

- private:仅能在当前切面类中引用该表达式
- public:在其他外部的切面类中也可以引用该表达式

{{</notice>}}



## 连接点

在Spring中用**JoinPoint**抽象了连接点，用它可以获得方法执行时的相关信息，如目标类名、方法名、方法参数等。

对于 @Around 通知，获取连接点信息只能使用ProceedingJoinPoint

对于其他四种通知，获取连接点信息只能使用JoinPoint，它是ProceedingJoinPoint 的父类型

相关方法

```java
@Around("execution()")
public object around(Proceeding)oinPoint joinPoint)throws Throwable {
	String className=joinPoint.getTarget().getc1ass().getName(); //获取目标类名
	Signature signature=joinPoint.getsignature();//获取目标方法签名
	String methodName= joinPoint.getsignature().getName();//获取目标方法名
	0bject[]args = joinPoint.getArgs();//获取目标方法运行参数
	0bject res= joinPoine.proceed();/执行原始方法,获取返回值(环绕通知)
	return res;
}
```

```
@Before("execution(""))
public void befored(JoinPoint joinPoint)
{
	String className=joinPoint.getTarget().getclass().getName();//获取目标类名
	Signature signature=joinPoint.getsignature();//获取目标方法签名
	String methodName =joinPoint.getsignature().getName();//获取目标方法名
	0bject[]args= joinPoint.getArgs();//获取目标方法运行参数
}

```

