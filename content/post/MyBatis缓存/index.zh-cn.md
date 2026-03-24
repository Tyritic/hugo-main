
---
date : '2024-11-07T16:31:55+08:00'
draft : false
title : 'MyBatis缓存'
image : ""
categories : ["MyBatis"]
tags : ["数据库","后端开发"]
description : "MyBatis的缓存相关知识"
---

## 🧠 什么是缓存

缓存是内存中的临时数据

使用缓存后可以减少和数据库的交互次数，提高执行效率

适合放入缓存的数据:

- 经常查询并且不经常改变的。
- 数据的正确与否对最终结果影响不大的。

不适用于缓存的数据:

- 经常改变的。
- 数据的正确与否对最终结果影响很大的。例如:商品的库存，银行的汇率，股市的牌价。

---

## 1️⃣ 一级缓存

一级缓存存在于SqlSession对象中。每次查询都先从SqlSession中找，如果没有则去数据库中查询，查询后将结果写入SqlSession提供的缓存中去，下次访问即可直接访问缓存。SqlSession对象是通过SqlSessionFactory对象获取的，每次重新获取SqlSession对象时，一级缓存就会失效

---

### 🔍 一级缓存的工作流程

&lt;div align="center"&gt;
  &lt;img src="微信截图_20241107163317.png" alt="一级缓存工作流程" width="82%"&gt;
&lt;/div&gt;

1. 第一次发起查询用户id为1的用户信息，先去找缓存中是否有id为1的用户信息，如果没有，从数据库查询用户信息。
2. 得到用户信息，将用户信息存储到一级缓存中。
3. 如果sqlSession去执行commit操作(执行插入、更新、删除)，清空SqlSession中的一级缓存，这样做的目的为了让缓存中存储的是最新的信息，避免脏读。
4. 第二次发起查询用户id为1的用户信息，先去找缓存中是否有id为1的用户信息，缓存中有，直接从缓存中获取用户信息。

{{&lt;notice tip&gt;}}

MyBatis的一级缓存默认开启

{{&lt;/notice&gt;}}

---

### ⚡ 一级缓存失效的四种情况

- 不是同一个SqlSession对象
- 同一个SqlSession对象但查询条件不一样
- 同一个SqlSession对象两次查询期间执行了任何一次增删改操作
- 同一个SqlSession对象两次查询期间手动清空了缓存

---

## 2️⃣ 二级缓存

二级缓存是SqlSessionFactory对象的缓存。由同一个SqlSessionFactory对象创建的SqlSession共享其缓存。因此二级缓存也称为全局缓存。二级缓存默认是不开启的，需要手动开启二级缓存，实现二级缓存的时候，MyBatis要求返回的POJO必须是可序列化的，也就是要求实现Serializable接口

---

### 🔧 配置方式

- 在核心配置文件中设置开启二级缓存：cacheEnabled=true

- 在mapper.xml文件中添加开启二级缓存的标签：&lt;cache&gt;

  - 可以设置属性readOnly

    - true：只允许读取不允许修改
    - false：有副本机制，允许修改

- 二级缓存必须在SqlSession关闭或提交之后有效

- 查询的数据所转换的实体类类型必须实现序列化的接口

  ```xml
  &lt;cache readOnly="true"&gt;&lt;/cache&gt;
  ```

---

### 🔍 二级缓存工作流程

&lt;div align="center"&gt;
  &lt;img src="微信截图_20241107165832.png" alt="二级缓存工作流程" width="82%"&gt;
&lt;/div&gt;

1. 当用户第一次查询某条数据时，会将查出来的数据放到一级缓存中
2. 当sqlSession关闭时，会将一级缓存中的数据保存到二级缓存中
3. 当用户第二次查询时，不会查询一级缓存，而是查询二级缓存
4. 此时若其他的sqlSession查询，也会查询二级缓存

{{&lt;notice tip&gt;}}

二级缓存失效的原因：在两次查询之间执行了任意的增删改，会使一级和二级缓存同时失效

{{&lt;/notice&gt;}}

---

### 🔄 缓存查询的顺序

- 先查询二级缓存，因为二级缓存中可能会有其他程序已经查出来的数据，可以拿来直接使用。
- 如果二级缓存没有命中，再查询一级缓存。
- 如果一级缓存也没有命中，则查询数据库。
- SqlSession关闭之后，一级缓存中的数据会写入二级缓存。

---

## 🎯 自定义缓存Ehcache

### 📌 Ehcache简介

- Ehcache是一个纯Java的进程内缓存框架，具有快速、精干等特点，是Hibernate中默认的CacheProvider。
- Ehcache是一种广泛使用的开源Java分布式缓存。主要面向通用缓存
- Java进程内的缓存，缓存数据在java进程内
- 缺点：单服务器缓存

---

### 🔧 使用Ehcache

- 首先导入ehcache相关的依赖和mybatis整合ehcache的依赖

  ```xml
  &lt;!--Mybatis提供的整合ehcache的包--&gt;
  &lt;dependency&gt;
      &lt;groupId&gt;org.mybatis.caches&lt;/groupId&gt;
      &lt;artifactId&gt;mybatis-ehcache&lt;/artifactId&gt;
      &lt;version&gt;1.2.1&lt;/version&gt;
  &lt;/dependency&gt;
  &lt;!-- slf4j日志门面--&gt;
  &lt;dependency&gt;
      &lt;groupId&gt;org.slf4j&lt;/groupId&gt;
      &lt;artifactId&gt;slf4j-api&lt;/artifactId&gt;
      &lt;version&gt;1.7.32&lt;/version&gt;
  &lt;/dependency&gt;
  &lt;!-- logback-classic--&gt;
  &lt;dependency&gt;
      &lt;groupId&gt;ch.qos.logback&lt;/groupId&gt;
      &lt;artifactId&gt;logback-classic&lt;/artifactId&gt;
      &lt;version&gt;1.2.3&lt;/version&gt;
  &lt;/dependency&gt;
  ```

- 配置ehcache.xml配置文件

  ```xml
  &lt;?xml version="1.0" encoding="UTF-8" ?&gt;
  &lt;ehcache xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:noNamespaceSchemaLocation="http://ehcache.org/ehcache.xsd"
           updateCheck="false"&gt;
  &lt;diskStore path="D:\rz\ehcache" /&gt;
      &lt;defaultCache
              maxElementsInMemory="1000"
              maxElementsOnDisk="10000000"
              eternal="false"
              overflowToDisk="true"
              timeToIdleSeconds="120"
              timeToLiveSeconds="120"
              diskExpiryThreadIntervalSeconds="120"
              memoryStoreEvictionPolicy="LRU"&gt;
      &lt;/defaultCache&gt;
  &lt;/ehcache&gt;
  ```

- 在mapper的xml文件中的cache标签中设置type属性

  ```xml
  &lt;cache type="org.mybatis.caches.ehcache.EhcacheCache"&gt;&lt;/cache&gt;
  ```

---

### 📝 配置文件说明

- diskStore：指定数据在磁盘中的存储位置。
- defaultCache：当借助CacheManager.add("demoCache")创建Cache时，EhCache便会采用`&lt;defalutCache/&gt;`指定的的管理策略

---

### 🔧 常用配置属性

- maxElementsInMemory：在内存中缓存的element的最大数目
- maxElementsOnDisk：在磁盘上缓存的element的最大数目，若是0表示无穷大
- eternal：设定缓存的elements是否永远不过期。如果为true，则缓存的数据始终有效，如果为false那么还要根据timeToIdleSeconds，timeToLiveSeconds判断
- overflowToDisk：设定当内存缓存溢出的时候是否将过期的element缓存到磁盘上
- timeToIdleSeconds：当缓存在EhCache中的数据前后两次访问的时间超过timeToIdleSeconds的属性取值时，这些数据便会删除，默认值是0,也就是可闲置时间无穷大
- timeToLiveSeconds：缓存element的有效生命期，默认是0也就是element存活时间无穷大
- diskSpoolBufferSizeMB：这个参数设置DiskStore(磁盘缓存)的缓存区大小。默认是30MB。每个Cache都应该有自己的一个缓冲区
- diskPersistent：在VM重启的时候是否启用磁盘保存EhCache中的数据，默认是false
- diskExpiryThreadIntervalSeconds：磁盘缓存的清理线程运行间隔，默认是120秒。每隔120s，相应的线程会进行一次EhCache中数据的清理工作
- memoryStoreEvictionPolicy：当内存缓存达到最大，有新的element加入的时候，移除缓存中element的策略。默认是LRU(最近最少使用)，可选的有LFU(最不常使用)和FIFO(先进先出)

