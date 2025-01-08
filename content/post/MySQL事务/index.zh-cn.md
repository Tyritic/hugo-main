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

## 并发事务问题

- 脏读：一个事务读到另外一个事务还没有提交的数据。
- 不可重复读：一个事务先后读取同一条记录，但两次读取的数据不同，称之为不可重复读。
- 幻读：一个事务按照条件查询数据时，没有对应的数据行，但是在插入数据时，又发现这行数据已经存在，好像出现了幻影”。

## 事务隔离级别

|         隔离级别          | 脏读 | 不可重复度 | 幻读 |
| :-----------------------: | :--: | :--------: | :--: |
|   **Read uncommitted**    |  √   |     √      |  √   |
|    **Read committed**     |  ×   |     √      |  √   |
| **Repeatable Read(默认)** |  ×   |     ×      |  √   |
|     **Serializable**      |  ×   |     ×      |  ×   |

其中 **Serializable** 数据安全性更好但是性能最差，**Read uncommitted**反之

### 相关SQL语句

#### 查看事务隔离级别

```mysql
select @@transaction isolation;
```

#### 设置事务隔离级别

```mysql
set [ session | global] transaction isolation level { read uncommitted | read committed | repeatable read | serializable }
```

