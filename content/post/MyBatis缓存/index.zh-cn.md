---
date : '2024-11-15T20:31:12+08:00'
draft : false
title : 'MyBatis缓存'
image : ""
categories : ["MyBatis"]
tags : ["后端开发","数据库"]
description : "MyBatis框架的缓存机制"
---

## 一级缓存

一级缓存是SqlSession级别的，通过同一个SqlSession查询的数据会被缓存，下次查询相同的数据，就会从缓存中直接获取，不会从数据库重新访问

### 使一级缓存失效的四种情况:

- 不同的SqlSession对应不同的一级缓存
- 同一个SqlSession但是查询条件不同
- 同一个SqlSession两次查询期间执行了任何一次增删改操作
- 同一个SqlSession两次查询期间手动清空了缓存

## 二级缓存

二级缓存是SqlSessionFactory级别，通过同一个SqlSessionFactory创建的SqlSession查询的结果会被缓存;此后若再次执行相同的查询语句，结果就会从缓存中获取。

### 二级缓存开启的条件:

1. 在核心配置文件中，设置全局配置属性cacheEnabled="true"，默认为true，不需要设置
2. 在mapper.xml映射文件中设置标签\<cache \>
3. 二级缓存必须在SqlSession关闭或提交之后有效
4. 查询的数据所转换的实体类类型必须实现序列化的接口

### 失效的情况

在两次查询之间进行任意的增删改，手动清空缓存只会清空一级缓存

### 相关配置

在mapper.xml映射文件中设置标签\<cache \>

相关属性参见 [MyBatis官方文档](https://mybatis.org/mybatis-3/sqlmap-xml.html#cache)

## 缓存查询顺序

- 先查询二级缓存，因为二级缓存中可能会有其他程序已经查出来的数据，可以拿来直接使用
- 如果二级缓存没有命中，再查询一级缓存
- 如果一级缓存也没有命中，则查询数据库
- Sqisession关闭之后，一级缓存中的数据会写入二级缓存