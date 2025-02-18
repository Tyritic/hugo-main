---
date : '2024-11-03T15:06:44+08:00'
draft : false
title : '控制反转（IOC)'
image : ""
categories : ["SpringBoot","Spring"]
tags : ["后端开发"]
description : "Spring框架中的控制反转(IOC)"
---

## IOC容器
### 概念定义

IOC 容器是 Spring 框架的核心部分，负责管理应用程序中的对象生命周期和依赖注入。

### 容器接口

**`BeanFactory`** 接口是 **IOC 的底层容器** 。负责管理和配置应用中的 Bean。主要负责配置、创建和管理 bean，为 Spring 提供了基本的依赖注入（DI）支持。

**`ApplicationContext`** 是 **`BeanFactory`** 的子接口，在 **`BeanFactory`** 的基础上添加了企业级的功能支持。

- 核心容器 **`BeanFactory`**
- 国际化 **`MessageSource`**
- 资源获取 **`ResourceLoader`**
- 环境信息 **`EnvironmentCapable`**
- 事件发布 **`ApplicationEventPublisher`**

其中 **`ApplicationContext`** 具有以下实现类

- **`ClassPathXmlApplicationContext`** ：通过读取类路径（resources）下的 XML格式的配置文件创建IOC容器对象
- **`FileSystemXmlApplicationContext`** ：通过文件系统路径读取 XML 格式的配置文件创建IOC 容器对象
- **`AnnotationConfigApplicationContext`** ：通过读取 Java 配置类创建 IOC 容腊对象
- **`WebApplicationContext`** ：专门为 Web 应用准备，基于 Web 环境创建 IOC 容器对象，并将对象引入存入 ServletContext 城中。

容器获取

- 根据name获取bean: **`Object getBean(String name)`**
- 根据类型获取bean：**`<T>T getBean(class<T> requiredType)`**
- 根据name获取bean(带类型转换)：**`<T>T getBean(String name,Class<T>requiredType)`**

## Bean对象

### 概念定义

任何通过 Spring 容器实例化、组装和管理的 Java 对象都可以被称为 Spring Bean。Bean 可以在 Spring 容器中被定义并且通过依赖注入来与其他 Bean 进行互相依赖。

即 Bean 可以看作是 Spring 应用中的一个对象，它的生命周期（创建、初始化、使用、销毁等过程）完全由 Spring 容器管理。

### 生命周期

#### 过程定义

- **实例化**：当 Spring 容器启动时，根据配置文件或注解，Spring 会首先实例化 Bean。
  - Spring 容器根据 Bean 的定义创建 Bean 的实例，相当于执行构造方法，也就是 new 一个对象。

- **依赖注入**：在实例化之后，Spring 容器会通过构造器、setter 方法或注解将其他 Bean 的依赖注入进来。
  - 相当于执行 setter 方法为字段赋值。

- **初始化**：如果 Bean 实现了 **`InitializingBean`** 接口或者使用了 **`@PostConstruct`** 注解，Spring 会在依赖注入完成后调用相应的初始化方法。
  - 初始化阶段允许执行自定义的逻辑，比如设置某些必要的属性值、开启资源、执行预加载操作等，以确保 Bean 在使用之前是完全配置好的。

- **销毁**：如果 Bean 实现了 **`DisposableBean`** 接口或使用了 **`@PreDestroy`** 注解，Spring 会在容器关闭时调用销毁方法。
  - 相当于执行 `= null`，释放资源。


#### 生命周期的拓展

- **`@PostConstruct`** 注解用于标识某个方法是 Bean 初始化后的回调方法。当 Spring 完成对 Bean 的依赖注入之后，它会自动调用带有 **`@PostConstruct`** 注解的方法。
  - 使用场景
    - **依赖注入后做额外的初始化工作**：例如，某个服务需要在依赖注入后连接外部系统。
    - **进行状态检查**：在 Bean 初始化后验证某些关键属性是否正确配置。
  - 执行时机
    - **`@PostConstruct`** 方法在依赖注入完成后立即执行，但在 Bean 可以被其他对象使用之前调用（即在 Bean 完成初始化前调用，Bean 处于准备状态）。
- **`@PreDestroy`** 注解用于标识当 Bean 被销毁时应该调用的方法。这个方法通常用于释放资源、关闭连接或者其他清理操作。Spring 容器在关闭时，会自动调用这些方法来进行资源的释放。
  - 使用场景
    - **资源清理**：例如关闭数据库连接、文件句柄、线程池等。
    - **会话管理**：例如在 Web 应用中，清理用户会话或缓存。
  - 执行时机：
    - **`@PreDestroy`** 方法在 Bean 即将被销毁时调用，一般是在 Spring 容器关闭时执行。对于单例（`singleton`）作用域的 Bean，会在容器关闭时调用；对于原型（`prototype`）作用域的 Bean，不会调用销毁方法，因为容器不管理其生命周期。
- **BeanPostProcessor接口**：
  - 通过实现 **`BeanPostProcessor`** 接口，开发者可以在 Bean 初始化前后添加自定义逻辑，如动态代理、AOP 增强等。
- **BeanFactoryPostProcessor接口**：
  - **`BeanFactoryPostProcessor`** 允许开发者在 Bean 实例化之前，修改 Bean 的定义信息（如属性值），它在所有 Bean 实例化之前执行。
- **Aware 接口**：
  - Spring 提供了多个 **`Aware`** 接口，如 **`BeanNameAware`**、**`BeanFactoryAware`**、**`ApplicationContextAware`** 等，允许 Bean 获取 Spring 容器的相关信息，进一步定制生命周期。

### 定义方式

#### 基于xml配置文件

早期的 Spring 应用通常通过 XML 文件定义 Bean，使用 `<bean>` 标签来指定类、构造器参数和依赖关系。

具体实现步骤

- 编写配置文件（元数据）
- 示例化IOC容器
- 获取Bean对象

#### 基于注解定义Bean对象

| 注解        | 说明                                                         | 位置                                            |
| ----------- | ------------------------------------------------------------ | ----------------------------------------------- |
| @Component  | 声明Bean对象的基本注解                                       | 不属于以下三类时使用该注解                      |
| @Service    | @Component的衍生注解，用于标识业务逻辑层的类。它具有明确的语义，表明该类承担业务操作 | 标注在ServiceImpl类上                           |
| @Controller | @Component的衍生注解，用于处理 HTTP 请求，并将结果返回给客户端。 | 标注在Controller类上                            |
| @Repository | @Component的衍生注解，用于数据访问层（DAO）的类，与数据库交互。 | 标注在数据访问类上（现在有mybatis，使用频率少） |

**示例**

```java
@Component
public class UserService {
}

```

**注意事项**

- 声明bean的时候，可以通过value属性指定bean的名字，如果没有指定，默认为类名首字母小写
- 使用以上四个注解都可以声明bean，但是在springboot集成web开发中，声明控制器bean只能用 **`@Controller`**

具体实现步骤

- 在组件中添加对应注解
- 指定组件扫描范围
  - Spring：修改xml配置文件
  - SpringBoot：默认扫描的范围是启动类所在包及其子包。**`@ComponentScan`** 注解虽然没有显式配置，但是实际上已经包含在了启动类声明注解 **`@SpringBootApplication`** 中
- 从IOC容器中获取容器

{{<notice tip>}}

**`@Bean`** 和 **`@Component`** 的区别

- **`@Bean`** 注解通常用于 Java 配置类的方法上，以声明一个 Bean 并将其添加到 Spring 容器中，**用于显示声明**。
  - 使用场景：用于配置第三方库或复杂对象
  - 控制权限：**`@Bean`** 注解允许开发人员手动控制Bean的创建和配置过程
- **`@Component`** 注解用于类级别，将该类标记为 Spring 容器中的一个组件，自动检测并注册为 Bean（需要扫对应的包），用于**自动扫描和注入**。
  - 使用场景：用于自动发现并注册自定义类
  - 控制权限：**`@Component`** 注解修饰的类是出Spring框架来创建和初始化的

{{</notice>}}

#### 基于配置类定义Bean对象

可以使用Java配置类来代替xml文件对Bean对象进行配置。

**`@Configuration`** 用于修饰一个类，指示某个Java类是配置类

**@Bean** 用于修饰一个方法，标识该方法的返回值是一个Bean对象

- 创建Bean类
- 创建对应的Java配置类，并使用 **`@Configuration`** 进行修饰，并在配置类中定义一个返回值为Bean对象的方法，这个方法用**`@Bean`**
- 从IOC容器中获取Bean对象

**示例代码**

```java
@Configuration
public class commonconfig{
	@Bean //将方法返回值交给I0C容器管理,成为IOC容器的bean对象
public SAXReader saxReader(){
	return new SAXReader();
}
```

{{<notice tip>}}

- 通过 **`@Bean`** 注解的name或value属性可以声明bean的名称，如果不指定，默认bean的名称就是方法名
- 如果第三方bean需要依赖其它bean对象，直接在bean定义方法中设置形参即可，容器会根据类型自动装配。

{{</notice>}}

### 作用域

#### 五大作用域

Spring支持五种作用域，后三种在web环境才生效

|   作用域    |                     说明                      |
| :---------: | :-------------------------------------------: |
|  singleton  | 容器内同名称 的 bean 只有一个实例(单例)(默认) |
|  prototype  |   每次使用该 bean 时会创建新的实例(非单例)    |
|   request   | 每个请求范围内会创建新的实例(web环境中，了解) |
|   session   | 每个会话范围内会创建新的实例(web环境中，了解) |
| application | 每个应用范围内会创建新的实例(web环境中，了解) |

使用 **`@Scope`** 注解来指定作用域

```java
@Scope("prototype")
@RestController
@RequestMapping("/depts")
public class DeptController {
}
```

{{<notice warning>}}

注意事项

- **`singleton`** 的bean，在容器启动时被创建，可以使用 **`@Lazy`** 注解来延迟初始化(延迟到第一次使用时)
- **`prototype`** 的bean，每一次使用该bean的时候都会创建一个新的实例。
- 实际开发当中，绝大部分的Bean是单例的，也就是说绝大部分Bean不需要配置scope属性。
- Spring 中的 Bean 默认都是单例的。

{{</notice>}}

#### 作用域对生命周期的影响

Spring 只帮我们管理单例模式 Bean 的完整生命周期，对于 **`prototype`** 的 Bean，Spring 在创建好交给使用者之后，则不会再管理后续的生命周期。

### 区分要素

在 **Spring** 中，`id` 和 `name` 用于唯一标识 **Bean**，确保在 **IOC 容器** 中可以正确获取 Bean。

| **属性** | 作用                  | 定义方式          | 唯一性       |
| -------- | --------------------- | ----------------- | ------------ |
| **id**   | Bean 的唯一标识符     | 只能是 **一个**   | **必须唯一** |
| **name** | Bean 的别名，可有多个 | 允许 **多个别名** | **可以重复** |

Spring **默认以类名（首字母小写）**  作为Bean的 **`name`**

默认情况下，**`id`** 属性和 **`name`** 属性的值是相同的。如果只配置了 **`id`** 属性而没有配置 **`name`** 属性，则 **`name`** 属性默认与 **`id`** 属性相同。

{{<notice tip>}}

使用xml文件配置时，同一个xml配置文件中不允许存在多个相同的id，在多个xml配置文件中允许存在多个相关id，但是

在同一个配置类文件中，如果存在多个 **`id`** 相同的Bean对象，容器内只会注册第一个Bean对象

{{</notice>}}

## 什么是控制反转（IOC)

IOC意味着将你设计好的对象交给容器控制，而不是传统的在你的对象内部直接控制。以右图为例![](73d67b2030772821a4bd2e6b746ecd38.png)

IOC容器作为中间位置“第三方”，也就是，使得A、B、C、D这四个对象没有了耦合关系，齿轮之间的传动全部依靠IOC容器，全部对象的控制权上交给IOC容器，所以IOC容器成了整个系统的关键核心，它起到一个“粘合剂”的作用，把系统中所有对象粘合在一起发挥作用。

## IOC的关键点

- **谁控制谁**：
  - 传统Java SE程序设计，我们直接在对象内部通过new进行创建对象，是程序主动去创建依赖对象；
  - 而IOC是有专门一个容器来创建这些对象，即由Ioc容器来控制对象的创建；
- **控制了什么**
  - 那就是主要控制了外部资源获取（不只是对象包括比如文件等）。
- **什么是反转**：
  - 传统应用程序是由我们自己在对象中主动控制去直接获取依赖对象，也就是正转；
  - 而反转则是由容器来帮忙创建及注入依赖对象
- **为什么是反转**：因为由容器帮我们查找及注入依赖对象，对象只是被动的接受依赖对象。
- **哪些方面反转了**：依赖对象的获取被反转了。

## IOC的过程

- 所有的类都会在Spring容器中登记，告诉spring你是个什么东西，你需要什么东西，
- 然后spring会在系统运行到适当的时候，把你要的东西主动给你，同时也把你交给其他需要你的东西。
- 所有的类的创建、销毁都由 spring来控制，也就是说控制对象生存周期的不再是引用它的对象，而是spring。
- 对于某个具体的对象而言，以前是它控制其他对象，现在是所有对象都被spring控制，所以这叫控制反转。

