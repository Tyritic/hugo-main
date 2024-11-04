---
date : '2024-11-03T18:26:36+08:00'
draft : false
title : 'MySQL数据库操作'
image : ""
categories : ["MySQL"]
tags : ["数据库"]
description : "以库为基本单位的数据库操作"
---

## 切换数据库

```mysql
use database_name;
```

## 创建数据库

```mysql
create database[if not exists] database_name;
```

## 查询数据库

- 查询所有的数据库

  ```mysql
  show databases;
  ```

- 查询当前正在使用的数据库

  ```mysql
  select database();
  ```

## 删除数据库

```mysql
drop database [if exist] database_name
```

