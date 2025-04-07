---
date : '2025-03-09T18:35:25+08:00'
draft : false
title : 'MySQL的慢查询和性能调优'
image : ""
categories : ["MySQL"]
tags : ["数据库"]
description : "MySQL的慢查询和性能调优策略"
math : true
---

## 慢查询

慢 SQL 就是执行时间较长的 SQL 语句，MySQL 中 long_query_time 默认值是 10 秒，也就是执行时间超过 10 秒的 SQL 语句会被记录到慢查询日志中。

### 慢SQL日志的启用

- 修改配置文件中慢SQL日志的开关和慢SQL日志的时间
- **`show processlist`** ：查看当前正在执行的 SQL 语句，找出执行时间较长的 SQL

## count(*)，count(1)，count(主键)，count(列)的执行效率比较

结果：count(*)=count(1)>count(主键)>count(列)

count函数的执行过程

在通过 count 函数统计有多少个记录时，MySQL 的 server 层会维护一个名叫 count 的变量。

server 层会循环向 InnoDB 读取一条记录，如果 count 函数指定的参数不为 NULL，那么就会将变量 count 加 1，直到符合查询的全部记录被读完，就退出循环。最后将 count 变量的值发送给客户端。

执行过程

- count(主键)
  - 如果表里只有主键索引，没有二级索引时，那么，InnoDB 循环遍历聚簇索引，将读取到的记录返回给 server 层，然后读取记录中的 id 值，就会 id 值判断是否为 NULL，如果不为 NULL，就将 count 变量加 1。
  - 如果表里有二级索引时，InnoDB 循环遍历的对象就不是聚簇索引，而是二级索引。
- count(1)
  - InnoDB 循环遍历聚簇索引（主键索引），将读取到的记录返回给 server 层，**但是不会读取记录中的任何字段的值**，因为 count 函数的参数是 1，不是字段，所以不需要读取记录中的字段值。参数 1 很明显并不是 NULL，因此 server 层每从 InnoDB 读取到一条记录，就将 count 变量加 1。
  - 但是，如果表里有二级索引时，InnoDB 循环遍历的对象就二级索引了。
- count(*)与count(1)基本一致

## SQL的性能调优策略

### 查询优化

#### 避免使用不必要的列

尽量避免使用 **`select *`**，只查询需要的列，减少数据传输量

#### 使用JOIN优化

对于 JOIN 操作，可以通过优化子查询、小表驱动大表、适当增加冗余字段、避免 join 太多表等方式来进行优化。

- 尽量减少使用子查询，特别是在 select 列表和 where 子句中的子查询，往往会导致性能问题，因为它们可能会为每一行外层查询执行一次子查询。通常使用JOIN联表查询来代替子查询
- 小表驱动大表：在执行 JOIN 操作时，应尽量让行数较少的表（小表）驱动行数较多的表（大表），这样可以减少查询过程中需要处理的数据量。
- 避免使用JOIN关联太多表因为 JOIN 太多表会降低查询的速度，返回的数据量也会变得非常大，不利于后续的处理。

#### 使用UNION优化

条件下推是指将 where、limit 等子句下推到 union 的各个子查询中，以便优化器可以充分利用这些条件进行优化。

例如下列SQL语句

```sql
SELECT * FROM (
    SELECT * FROM A
    UNION
    SELECT * FROM B
) AS sub
WHERE sub.id = 1;
```

可以将where子句的条件下推到union的各个子查询

```sql
SELECT * FROM A WHERE id = 1
UNION
SELECT * FROM B WHERE id = 1;
```

### 索引优化

参考[往期博客](https://tyritic.github.io/p/mysql%E7%B4%A2%E5%BC%95/#%E7%B4%A2%E5%BC%95%E4%BC%98%E5%8C%96%E6%96%B9%E6%B3%95)