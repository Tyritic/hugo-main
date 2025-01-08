---
date : '2025-01-01T14:51:32+08:00'
draft : false
title : 'BO、VO、PO、DO、DTO的理解'
image : ""
categories : ["项目技术"]
tags : [""]
description : "项目开发中对各种数据交换对象的理解"
math : true
---

## Pojo类

pojo类在项目开发中用于标识实体类，该类在项目对应一个实际的业务对象，例如：user,student等

## PO/DO

PO/DO类在项目中对应数据库中的一张表，数据库PO/DO是持久化对象，用于表示数据库中的一条记录映射成的Java对象，类中应该都是基本数据类型和String

PO仅仅用于表示数据，不对数据进行操作，拥有get和set方法。对象类中的属性对应数据库表中的字段，有多少个字段就有多少个属性，完全匹配。

**命名规范**：数据库表名+PO/DO

## DTO

全称（**Data Transfer Object**）用于后端接受前端的请求，将前端请求参数封装成对象

通常用于将前端请求传递到控制层和控制层传递到业务逻辑层

## VO

全称（**View Object**）用于后端响应前端的过程中，作为视图对象

## BO

全称（**Business Object**）用于后端业务逻辑的处理

BO是实际的业务对象，会参与业务逻辑的处理操作，里面可能会包含多个类，用于表示一个业务对象。遵循JavaBean规范，拥有get和set方法。

