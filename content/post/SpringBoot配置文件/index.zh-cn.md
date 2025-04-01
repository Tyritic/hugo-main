---
date : '2024-11-07T10:19:39+08:00'
draft : false
title : 'SpringBoot配置文件'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发"]
description : "SpringBoot的配置文件以及参数配置化"
---

## 配置方法

### 通过配置文件配置

#### 配置文件的种类

SpringBoot提供了多种属性配置方式

- **application.properties**

  ```properties
  server.port=8080
  server.address=127.0.0.1
  ```

  

- **application.yml**

  ```yml
  server:
  	port:8080
  	address:127.0.0.1
  ```

  

- **application.yaml**

  ```yaml
  server:
  	port:8080
  	address:127.0.0.1
  ```

  

#### 配置文件优先级

优先级从高到低：properties>yml>yaml

外部配置文件的优先级（从低到高）

- classpath（resource文件夹）
- classpath根config
- 项目根目录（对于存在继承/聚合关系的maven项目项目根目录是父工程的根目录）
- 项目根目录/config
- 直接子目录/config

#### 多配置文件的加载

Profile意思是配置，不同环境可能需要不同的配置需要

SpringBoot框架提供了多profile的管理功能，我们可以使用profile文件来区分不同环境的配置

如果需要创建自定义的yml文件时，可以用application-{profile}.yml的命名方式

切换不同环境的yml文件时在application.yml中配置

```yml
spring:
  profiles:
    active: profile
```

### 其他配置方式

#### Java系统属性

- 执行maven打包指令package

- 执行java指令，运行jar包，在执行java命令时添加参数

- 参数格式

  ```
  -Dxxx=xxx
  ```


#### 命令行参数

- 执行maven打包指令package

- 执行java指令，运行jar包，在执行java命令时添加参数

- 参数格式

  ```
  --xxx=xxx
  ```


### 配置方法的优先级

优先级从低到高

- application.yaml(忽略)
- application.yml
- application.properties
- java系统属性(-Dxxx=xxx)
- 命令行参数(--xxx=xxx)

## yml文件语法

### 基本语法

- 大小写敏感
- 数值前边必须有空格，作为分隔符
- 使用缩进表示层级关系，缩进时，不允许使用Tab键，只能用空格(idea中会自动将Tab转换为空格)
- 缩进的空格数目不重要，只要相同层级的元素左侧对齐即可
- #表示注释，从这个字符一直到行尾，都会被解析器忽略

### 数据格式

- 对象/Map集合

  ```yml
  user:
  	name: zhangsan
  	age: 18
  	password:123456
  ```

- 数组/List集合

  ```yml
  hobby:
  	-java
  	-game
  	-sport
  ```

## 参数配置化

### 利用注解进行参数配置化

**`@Value`** 通常用于外部配置的属性注入，具体用法为: **`@Value("${配置文件中的key}")`**

在 Spring 框架中，**`@Value`** 注解用于注入外部化的配置值到 Spring 管理的 Bean 中。通过 **`@Value`** 注解，可以将属性文件、环境变量、系统属性等外部资源中的值注入到 Spring Bean 的字段、方法参数或构造函数参数中。

示例代码

```properties
aliyun.oss.endpoint=https://oss-cn-hangzhou.aliyuncs.com
aliyun.oss.accessKeyId=LTAI4GCHlvX6DKqJWxdбnEuW
aliyun.oss.accessKeySecret=yBshYweHOpqDuhCArrVHwIiBKPYqSL
aliyun.oss.bucketName=web-tlias
```

```java
@Component
pubiic class AliossUti1s{
 @Value("${aliyun.oss.endpoint}")
 private string endpoint;
	
 @Value("${aliyun.oss.accessKeyId}")
 private string accesskeyId;
	
 @Value("${aliyun.oss.accessKeySecret}")
 private String accessKeySecret;
	
 @Value ("${aliyun.oss.bucketName } ")
 private String bucketName
}
```

### 使用自定义配置类进行参数配置化

自定义properties文件使用 **`@Component`** 注册为Bean对象，使用 **`@ConfigurationProperties`** 注解批量的将yml配置文件的属性和Bean对象属性绑定，**`@ConfigurationProperties`** 的prefix属性指定application.yml的子节点，该节点中的子节点将自动和属性进行绑定

示例代码

```java
@Data
@Component
@ConfigurationProperties(prefix = "operator.aliyun.oss")
public class AliyunOSSProperties {
    String endpoint;
    String accessKeyId;
    String accessKeySecret;
    String bucketName;
    String region;
}
```

**`@ConfigurationProperties`** 支持jsr-300数据校验使用 **@Validate**

{{<notice tip>}}

​	jsr-300数据校验

- @Null：被注释的元素必须为 null
- @NotNull：被注释的元素必须不为nu11
- @AssertTrue：被注释的元素必须为true
- @AssertFalse：被注释的元素必须为false
- @Min(value)：被注释的元素必须是一个数字，其值必须大于等于指定的最小值
- @Max(value)：被注释的元素必须是一个数字，其值必须小于等于指定的最大值
- @DecimalMin(value)：被注释的元素必须是一个数字，其值必须大于等于指定的最小值
- @DecimalMax(value)：被注释的元素必须是一个数字，其值必须小于等于指定的最大值
- @Size(max，min)：被注释的元素的大小必须在指定的范围内
- @Digits (integer,fraction)：被注释的元素必须是一个数字，其值必须在可接受的范围内
- @Past：被注释的元素必须是一个过去的日期
- @Future：被注释的元素必须是一个未来的日期

{{</notice>}}
