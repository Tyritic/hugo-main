---
date : '2024-11-04T19:06:51+08:00'
draft : false
title : 'MySQL事务'
image : ""
categories : ["MySQL"]
tags : ["数据库"]
description : "MySQL事务的使用"
---

## 概念

事务是一组操作的集合，它是一个不可分割的工作单位。事务会把所有的操作作为一个整体一起向系统提交或撤销操作请求，即这些操作 要么同时成功，要么同时失败。

{{<notice tip>}}

MySQL会立即隐式的提交事务。默认MySQL的事务是自动提交的，

{{</notice>}}

## 事务控制语句

开启事务

```mysql
start transaction；
```

提交事务

```mysql
commit;
```

回滚事务

```mysql
rollback;
```

## 四大特性

- 原子性（Atomicity）：事务是不可分割的最小单元，要么全部成功，要么全部失败
- 一致性（Consistency）：事务完成时，必须使所有的数据都保持一致状态
- 隔离性（lsolation）：数据库系统提供的隔离机制，保证事务在不受外部并发操作影响的独立环境下运行
- 持久性（Durability）：事务一旦提交或回滚，它对数据库中的数据的改变就是永久的
