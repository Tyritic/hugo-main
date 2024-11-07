---
date : '2024-11-07T10:19:39+08:00'
draft : false
title : 'SpringBoot配置文件'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发"]
description : "SpringBoot的配置文件以及参数配置化"
---

## 配置文件的种类

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

  

## 配置文件优先级

优先级从高到低：properties>yml>yaml

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

**@Value 注解**通常用于外部配置的属性注入，具体用法为: @Value("${配置文件中的key}")

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

### 使用自定义配置文件进行参数配置化

自定义properties文件使用@Component注册为Bean对象，使用@ConfigurationProperties注解批量的将外部的属性配置注入到Bean对象的属性中，@ConfigurationProperties的prefix属性指定application.yml的属性

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

