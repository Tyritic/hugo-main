---
date : '2024-11-08T17:05:51+08:00'
draft : false
title : 'Bean对象的管理'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发","框架原理"]
description : "Bean对象在IOC容器的管理过程"
math : true
---

## Bean对象的获取

默认情况下，Spring项目启动时，会把bean都创建好放在IOC容器中

{{<notice tip>}}

上述所说的【Spring项目启动时，会把其中的bean都创建好】还会受到作用域及延迟初始化影响，这里主要针对于默认的单例非延迟加载的bean而言。

{{</notice>}}

但可以主动获取Bean对象

具体实现

1. 注入IOC容器对象：ApplicationContext

```java
根据name获取bean: Object getBean(String name)
根据类型获取bean：<T>T getBean(class<T> requiredType)
根据name获取bean(带类型转换)：<T>T getBean(String name,Class<T>requiredType)
```



## Bean对象的作用域

Spring支持五种作用域，后三种在web环境才生效

|   作用域    |                      说明                      |
| :---------: | :--------------------------------------------: |
|  singleton  | 容器内同 名称 的 bean 只有一个实例(单例)(默认) |
|  prototype  |    每次使用该 bean 时会创建新的实例(非单例)    |
|   request   | 每个请求范围内会创建新的实例(web环境中，了解)  |
|   session   | 每个会话范围内会创建新的实例(web环境中，了解)  |
| application | 每个应用范围内会创建新的实例(web环境中，了解)  |

使用@Scope注解来指定作用域

```java
@Scope("prototype")
@RestController
@RequestMapping("/depts")
public class DeptController {
}
```

{{<notice warning>}}

注意事项

- 默认singleton的bean，在容器启动时被创建，可以使用@Lazy注解来延迟初始化(延迟到第一次使用时)prototype的bean，每一次使用该bean的时候都会创建一个新的实例。
- 实际开发当中，绝大部分的Bean是单例的，也就是说绝大部分Bean不需要配置scope属性。

{{</notice>}}



## 第三方Bean对象

如果要管理的bean对象来自于第三方(不是自定义的)，是无法用 @Component及衍生注解声明bean的，就需要用到 @Bean注解。

具体实现

​	方法一：在启动类中使用@Bean注解修饰一个返回值为Bean对象的方法（不推荐）

```java
@springBootApplication
public class springbootWebconfig2Application {
@Bean/将方法返回值交给I0C容器管理,成为IOC容器的bean对象
public SAXReader saxReader(){
	return new SAXReader();
}
```

方法二：创建一个配置类（使用@Configuration)集中配置Bean对象

```java
@Configuration
public class commonconfig{
	@Bean/将方法返回值交给I0C容器管理,成为IOC容器的bean对象
public SAXReader saxReader(){
	return new SAXReader();
}
```

{{<notice tip>}}

- 通过@Bean注解的name或value属性可以声明bean的名称，如果不指定，默认bean的名称就是方法名
- 如果第三方bean需要依赖其它bean对象，直接在bean定义方法中设置形参即可，容器会根据类型自动装配。

{{</notice>}}