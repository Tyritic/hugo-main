---
date : '2024-11-06T17:19:27+08:00'
draft : false
title : 'Lombok类库'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发"]
description : "SpringBoot常用依赖类库lombok"
---

## Lombok简介

Lombok是一个实用的java类库，能通过注解的形式自动生成构造器、getter/setter、equals、hashcode、toString等方法
并可以自动化生成日志变量，简化iava开发

## 常见注解

|        注解         |                             作用                             |
| :-----------------: | :----------------------------------------------------------: |
|   @Getter/@Setter   |                 为所有的属性提供get/set方法                  |
|      @Builder       | 通过建造者模式来创建对象，这样就可以通过链式调用的方式进行对象赋值 |
|      @ToString      |             会给类自动生成易阅读的toString 方法              |
| @EqualsAndHashCode  | 根据类所拥有的非静态字段自动重写 equals方法和 hashcode 方法  |
|        @Data        | 提供了更综合的生成代码功能(@Getter+@Setter+@ToString+@EqualsAndHashCode) |
| @NoArgsConstructor  |                 为实体类生成无参的构造器方法                 |
| @AllArgsConstructor |  为实体类生成除了static修饰的字段之外带有各参数的构造器方法  |

