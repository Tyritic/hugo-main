---
date : '2024-11-12T10:01:20+08:00'
draft : false
title : 'SpringBoot整合Springdoc-OpenApi'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发"]
description : "在SpringBoot框架中使用Springdoc-OpenApi框架生成接口文档"
---

## 简介

Springdoc-OpenApi是一个规范且完整的框架，用于生成、描述、调用和可视化 RESTful 风格的 Web 服务。

Springdoc-OpenApi 的目标是对 REST API 定义一个标准且和语言无关的接口，可以让人和计算机拥有无须访问源码、文档或网络流量监测就可以发现和理解服务的能力。

## 具体使用

1. 引入具体依赖springfox

   ```xml
   <!-- 导入相关依赖 -->
   <dependency>
       <groupId>org.springdoc</groupId>
       <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
       <version>2.5.0</version>
   </dependency>
   
   ```

2. 添加配置类用于Api文档的基本配置

   ```java
   package org.example.user.config;
   import io.swagger.v3.oas.models.OpenAPI;
   import io.swagger.v3.oas.models.info.Contact;
   import io.swagger.v3.oas.models.info.Info;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   @Configuration
   public class SpringDocConfig {
       // OpenAPI类用于定制全局文档信息
       @Bean
       public OpenAPI customOpenAPI() {
           return new OpenAPI()
               // 定制文档基本信息
               .info(new Info()
                     //关于文档信息
                   .title("API 文档标题")
                   .description("API 文档描述")
                   .version("1.0.0")
                   .termsOfService("https://example.com/terms")
                     
                     //关于开发者
                   .contact(new Contact()
                       .name("开发者姓名")
                       .url("开发者网址")
                       .email("开发者邮箱"))
                     
                     //关于许可证
                   .license(new License()
                       .name("许可证名称")
                       .url("许可证文件")))
               
               //配置服务器信息（可选）
               .servers(List.of(
                   new Server().url("服务器url").description("服务器描述"),
                   new Server().url("https://api.example.com").description("生产服务器")))
               
               //配置外部文档信息（可选）
               .externalDocs(new ExternalDocumentation()
                   .description("外部文档描述")
                   .url("外部文档url"));
       }
   }
   ```

3. 修改application.yml配置文件

   ```yml
   springdoc:
   	api-docs:
   		enable: true
   	swagger-ui:
   		enable: true
   ```

   其余属性参见官方文档 [SpringDoc-OpenApi官方文档](https://springdoc.org/#swagger-ui-properties)

   {{<notice tip>}}

   ```yml
   springdoc:
   	 group-configs: #进行文档分组每个组配置对应的请求路径以及区分所在包
       	- group: 'user'
        	  paths-to-match: '/api/users/**'
             packages-to-scan: com.toher.springdoc.user
       	- group: 'product'
             paths-to-match: '/api/product/**'
             packages-to-scan: com.toher.springdoc.product
   ```

   可以在微服务架构中进行分组

   {{</notice>}}

4. 查看接口文档

   1. Swagger-UI接口文档：http://localhost:8080/swagger-ui/index.html
   2. Json形式接口文档：[localhost:8080/v3/api-docs](http://localhost:8080/v3/api-docs)

5. 使用注解编写接口文档

## 常用注解

### 对实体类的描述

- `@Schema`：用于描述类或字段的数据结构和属性，支持OpenAPI 3规范中的各种特性，如类型、格式、默认值等。

  ```java
  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  @Builder
  public class User {
      @Schema(description = "用户ID", example = "1")
      private int id;
      @Schema(description = "用户姓名", example = "张三")
      private String name;
      @Schema(description = "用户年龄", example = "18")
      private int age;
  }
  ```


### 对方法的描述

- `@Operation`：用于方法级别，提供对API操作的详细描述，包括摘要、描述、响应、参数等信息。

  - `summary`：操作的简要描述。
  - `description`：操作的详细描述。
  - `tags`：与操作相关的标签。
  - `operationId`：操作的唯一标识符。
  - `parameters`：操作的参数列表。
  - `responses`：操作的响应列表。

  ```java
  @Operation(
      summary = "获取用户信息",
      description = "根据用户ID获取用户详细信息",
      tags = {"用户操作"},
      operationId = "getUserById"
  )
  @RequestMapping("/users")
  public User getUserById(@PathVariable Long id) {
      // 实现逻辑
  }
  ```

- `@ApiResponses`是一个容器注解，用于收集多个@ApiResponse，描述方法可能返回的各种响应情况。

- `@ApiResponse`描述了API操作的一个特定响应，包括响应的状态码、描述、内容类型等。

  - `responseCode`：响应代码。
  - `description`：响应描述。
  - `content`：响应内容。

  ```java
  	@RequestMapping(value="/{id}", method = RequestMethod.GET)
      @Operation(summary = "findById方法", description = "根据id查询用户")
      @Parameter(name = "id", description = "用户id", required = true, in = ParameterIn.PATH)
      @ApiResponses(value = {
              @ApiResponse(responseCode = "200", description = "查询成功",content={@Content(mediaType = "application/json",
                      schema = @Schema(implementation = Result.class))}),
              @ApiResponse(responseCode = "500", description = "查询失败",content={@Content(mediaType = "application/json",
                      schema = @Schema(implementation = Result.class))})
      })
     
      public Result<User> findById(@PathVariable Integer id) {
          return Result.success("查询成功", new User(id, "张三", 20));
      }
  ```

- `@Parameters`是一个容器注解，用于收集多个@Parameter注解，描述方法的多个请求参数。

- `@Parameter`：用于描述单个请求参数，可以是查询参数、路径参数、请求头等。

  - `name`：参数名。
  - `description`：参数描述。
  - `required`：是否必需参数。
  - `in`：参数所在位置（query、header、path、cookie）。

  ```java
  @Parameters(value = {
          @Parameter(name = "name", description = "姓名", in = ParameterIn.PATH),
          @Parameter(name = "age", description = "年龄", in = ParameterIn.QUERY)
  })
  @GetMapping("/{name}")
  public List<Programmer> getProgrammers(@PathVariable("name") String name, @RequestParam("age") Integer age) { 
      ...
  }
  ```

  

### 对类的描述

@Tag：用于标记API控制器或方法属于哪一个功能分类或标签，有助于组织和分类API文档中的不同部分

```java
@Tag(name = "程序员", description = "程序员乐园")
@RestController
@RequestMapping("/api/programmer")
public class ProgrammerController {
...
}
```
