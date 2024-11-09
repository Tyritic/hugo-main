---
date : '2024-11-08T18:47:12+08:00'
draft : false
title : 'SpringBoot底层原理'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发","框架原理"]
description : "SpringBoot框架的底层原理"
---

## 起步依赖

原理：SpringBoot框架提供的起步依赖通过**Maven的依赖传递**集成了开发中常见的依赖

## 自动配置

### 概念

当spring容器启动后，一些配置类、bean对象就自动存入到了I0C容器中，不需要手动去声明，从而简化了开发，省去了繁琐的配置操作。

### 实现方案

#### 方案一：@ComponentScan 组件扫描依赖

```java
@SpringBootApplication
@ComponentScan({"com.alibaba","com.google","org.springframework","org.mybatis",...}
public class springbootWebconfig2Application{
}
```

#### 方案二：@lmport 导入

使用@lmport导入的类会被Spring加载到I0C容器中，导入形式主要有以下几种:

- 导入 普通类
- 导入 配置类
- 导入 ImportSelector 接口实现类
- @EnableXXX注解，封装了@Import

```java
@Import({TokenParser.class,Headerconfig.class})
@SpringBootApplication
public class springbootWebconfig2Application{
    
}
```

### 源码分析

1. 查看启动类的注解**@SpringBootApplication**的源码

   ```java
   //自定义组件所需的元注解
   @Target({ElementType.TYPE})
   @Retention(RetentionPolicy.RUNTIME)
   @Documented
   @Inherited
   //表示启动类也是一个配置类
   @SpringBootConfiguration
   //自动配置功能
   @EnableAutoConfiguration
   @ComponentScan(
       excludeFilters = {@Filter(
       	type = FilterType.CUSTOM,
       	classes = {TypeExcludeFilter.class}
       ), @Filter(
       	type = FilterType.CUSTOM,
       	classes = {AutoConfigurationExcludeFilter.class}
       )}
   )
   ```

   {{<notice tip>}}

   问：为什么在启动类中可以声明第三方Bean对象？

   答：@SpringBootApplication中封装了@SpringBootConfiguration，表明启动类也是一个配置类

   问：为什么启动类只会扫描启动类所在包及其子包的组件

   答：@SpringBootApplication中封装了@ComponentScan的注解

   {{</notice>}}

2. 由 **@SpringBootApplication** 的注解源码可知自动配置由注解 **@EnableAutoConfiguration** 提供，查看 @EnableAutoConfiguration的注解

   ```
   @Target({ElementType.TYPE})
   @Retention(RetentionPolicy.RUNTIME)
   @Documented
   @Inherited
   @AutoConfigurationPackage
   @Import({AutoConfigurationImportSelector.class})
   public @interface EnableAutoConfiguration {
       String ENABLED_OVERRIDE_PROPERTY = "spring.boot.enableautoconfiguration";
   
       Class<?>[] exclude() default {};
   
       String[] excludeName() default {};
   }
   
   ```

   可以看出 **@EnableAutoConfiguration** 注解通过 **@Import**注解导入 ImportSelector 接口实现类来实现自动配置

3. **查看AutoConfigurationImportSelector.class** 的源码

   ```java
   public String[] selectImports(AnnotationMetadata annotationMetadata) {
           if (!this.isEnabled(annotationMetadata)) {
               return NO_IMPORTS;
           } else {
               AutoConfigurationEntry autoConfigurationEntry = 	             this.getAutoConfigurationEntry(annotationMetadata);
               return StringUtils.toStringArray(autoConfigurationEntry.getConfigurations());
           }
       }
   ```
   **selectImports**方法返回要导入的Bean对象的全类名
   
4. 从 **AutoConfigurationImportSelector.class** 的源码可以知道返回值从 **autoConfigurationEntry.getConfigurations()** 获得而**autoConfigurationEntry** 由 **AutoConfigurationImportSelector.getAutoConfigurationEntry**方法获得。查看 **getAutoConfigurationEntry** 的源码

   ```java
   protected AutoConfigurationEntry getAutoConfigurationEntry(AnnotationMetadata annotationMetadata) {
           if (!this.isEnabled(annotationMetadata)) {
               return EMPTY_ENTRY;
           } else {
               AnnotationAttributes attributes = this.getAttributes(annotationMetadata);
               List<String> configurations = this.getCandidateConfigurations(annotationMetadata, attributes);
               configurations = this.removeDuplicates(configurations);
               Set<String> exclusions = this.getExclusions(annotationMetadata, attributes);
               this.checkExcludedClasses(configurations, exclusions);
               configurations.removeAll(exclusions);
               configurations = this.getConfigurationClassFilter().filter(configurations);
               this.fireAutoConfigurationImportEvents(configurations, exclusions);
               return new AutoConfigurationEntry(configurations, exclusions);
           }
       }
   ```

5. 从 **AutoConfigurationImportSelector.getAutoConfigurationEntry**看出 **configuration**是一个List\<String\>对象，从**AutoConfigurationImportSelector.getCandidateConfigurations(annotationMetadata, attributes)** 中获得。查看**AutoConfigurationImportSelector.getCandidateConfigurations(annotationMetadata, attributes)** 的源码

   ```java
   protected List<String> getCandidateConfigurations(AnnotationMetadata metadata, AnnotationAttributes attributes) {
           List<String> configurations = ImportCandidates.load(AutoConfiguration.class, this.getBeanClassLoader()).getCandidates();
           Assert.notEmpty(configurations, "No auto configuration classes found in META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports. If you are using a custom packaging, make sure that file is correct.");
           return configurations;
   }
   ```
   SpringBoot框架会自动加载 **META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports** 的配置文件并封装到 **configurations** 这个List集合中

### 实现过程

1. **@SpringBootApplication**注解封装了 **@EnableAutoConfiguration** 来实现自动配置

2. **@EnableAutoConfiguration** 封装了 **@Import** 注解，该注解以引入 **ImportSelector**接口的实现类**AutoConfigurationImportSelector** 来完成自动装配

3.  **AutoConfigurationImportSelector** 获取 **AutoConfigurationEntry** 对象，该对象具有成员变量**Configurations**用于存储Bean对象的全类名

4.  **AutoConfigurationEntry** 使用 **getCandidateConfigurations**方法，SpringBoot框架会自动加载 **META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports** 配置文件并封装到 **configurations** 这个List集合中

5.  **META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports** 中封装了Bean对象的声明

### 条件配置

**@Conditional**
作用：按照一定的条件进行判断，在满足给定条件后才会注册对应的bean对象到SpringIOC容器中。

位置：方法、类

**@Conditional** 本身是一个父注解，派生出大量的子注解:

- **@Conditional0nClass**：判断环境中是否有对应字节码文件，才注册bean到IOC容器。
- **@ConditionalOnMissingBean**：判断环境中没有对应的bean(类型或名称)，才注册bean到IOC容器。
- **@ConditionalOnProperty**：判断配置文件中有对应属性和值，才注册bean到IOC容器。
