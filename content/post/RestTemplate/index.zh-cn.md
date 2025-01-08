---
date : '2024-11-11T18:48:31+08:00'
draft : false
title : 'RestTemplate'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发"]
description : "RestTemplate在web开发中的使用以及REST服务"
---

## Restful服务

Restful是目前流行的互联网软件服务架构设计风格

### **服务特点**

- 每一个URL代表一种资源
- 客户端使用GET、POST、PUT、DELETE四种表示操作方式的动词对服务端资源进行操作：GET用于获取资源，POST用于新建资源（也可以用于更新资源），PUT用于更新资源，DELETE用于删除资源。
- 通过操作资源的表现形式来实现服务端请求操作。
- 资源的表现形式是JSON或者HTML。
- 客户端与服务端之间的交互在请求之间是无状态的，从客户端到服务端的每个请求都包含必需的信息。

示例：

```java
@RestController
public class UserController{
   @ApiOperation("获取用户")
   @GetMapping("/user/{id}")
   public String getUserById(@PathVariable int id){
       System.out.println(id);
       return "根据ID获取用户信息";
  }
   @PostMapping("/user")
   public String save(User user){
       return "添加用户";
  }
   @PutMapping("/user")
   public String update(User user){
       return "更新用户";
  }
   @DeleteMapping("/user/{id}")
   public String deleteById(@PathVariable int id){
       System.out.println(id);
       return "根据ID删除用户";
  }
}

```

### **最佳实现**

#### 接口设计

- URL的组成
  - 网络协议
  - 服务器地址
  - 接口名称
  - ？参数列表（GET方法）

#### 响应设计

- Content-body用来存放数据
- 用于描述数据的msg和code放入Content-header中

## RestTemplate

### 简介

RestTemplate是Spring提供的用于访问Rest服务的，RestTemplate提供了多种便捷访问远程Http服务的方法，传统情况下在java代码里访问restfuI服务，一般使用Apache的HttpClient，不过此种方法使用起来太过繁琐。spring提供了一种简单便捷的模板类来进行操作，这就是RestTemplate.（常用于客户端和微服务）

### 具体使用

以微服务为例

1. 创建一个Controller类（用@RestController修饰）

2. 创建一个Config类对RestTemplate进行配置和创建

   ```java
   @Configuration
   public class RestTemplateConfig {
       /**
        * 没有实例化RestTemplate时，初始化RestTemplate
        * 性能上OkHttp优于Apache的HttpClient，Apache的HttpClient优于HttpURLConnection（默认）。
        * @return
        */
       @ConditionalOnMissingBean(RestTemplate.class)
       @Bean
       public RestTemplate restTemplate(){
           RestTemplate restTemplate = new RestTemplate(getClientHttpRequestFactory());
           return restTemplate;
       }
       
       /**
    		* 使用OkHttpClient作为底层客户端
    		* @return
    	*/
   	private ClientHttpRequestFactory getClientHttpRequestFactory(){
       		OkHttpClient okHttpClient = new OkHttpClient.Builder()
               .connectTimeout(5, TimeUnit.SECONDS)
               .writeTimeout(5, TimeUnit.SECONDS)
               .readTimeout(5, TimeUnit.SECONDS)
               .build();
       		return new OkHttp3ClientHttpRequestFactory(okHttpClient);
   	}
   
   }
   
   ```

3. 进行依赖注入并使用该Bean对象

### 常见方法

#### GET请求

- getForObject：获取请求体
  - 不带参数：(uri, \<T \>.class) 代表 请求地址、HTTP响应转换被转换成的对象类型
  - 带参数(uri, String.class, paramMap) 代表 请求地址、HTTP响应转换被转换成的对象类型，请求参数

- getForEntity：获取整个请求，除了包含响应体，还包含`HTTP`状态码、`contentType、contentLength、Header`等信息

#### POST请求

- postForObject：获取请求体
- postForEntity：获取整个请求，除了包含响应体，还包含`HTTP`状态码、`contentType、contentLength、Header`等信息

#### PUT请求

- put：

#### Delete请求

- delete：

#### 通用请求

- exchange(String url, HttpMethod method,@Nullable HttpEntity<?> requestEntity, Class responseType, Map uriVariables) 
  - url: 请求地址；     
  - method: 请求类型(如：POST,PUT,DELETE,GET)；    
  - requestEntity: 请求实体，封装请求头，请求内容    
  - responseType: 响应类型，根据服务接口的返回类型决定     
  - uriVariables: url中参数变量值