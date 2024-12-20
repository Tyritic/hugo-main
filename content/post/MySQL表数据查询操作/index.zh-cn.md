---
date : '2024-11-04T15:07:25+08:00'
draft : false
title : 'MySQL表数据查询操作'
image : ""
categories : ["MySQL"]
tags : ["数据库"]
description : "从MySQL数据库中查询元组的操作"
---

## 基本查询

基本语法

```mysql
select #可以添加distinct来去除重复项
	字段列表 #(查询所有字段可以简写为*)
from table_name
where condition  #条件列表
#以下均为可选选项
group by 聚合函数（字段列表）
having 对分组条件的过滤操作
order by 对字段列表的排序 #（ASC升序，DESC降序）
limit 分页参数 (起始索引，查询记录数) #索引从0开始，起始索引=（查询页码-1)*每页记录数
```

## 条件查询

### 常见条件运算符

|     比较运算符      |                  功能                  |
| :-----------------: | :------------------------------------: |
|          >          |                  大于                  |
|         >=          |                大于等于                |
|          <          |                  小于                  |
|         <=          |                小于等于                |
|       <>或!=        |                 不等于                 |
| between ... and ... |  在某个区间范围内（含最大值和最小值）  |
|       in(...)       |        在in中的列表的值，多选一        |
|     like 占位符     | 模糊匹配（_匹配单个字符，&匹配任意字符 |
|       is null       |                 是null                 |

### 常见逻辑运算符

| 逻辑运算符 | 功能 |
| :--------: | :--: |
| and 或 &&  |  与  |
| or 或 \|\| |  或  |
| not 或 \|  |  非  |

## 分组查询

### 聚合函数

| 函数  |  功能  |
| :---: | :----: |
|  sum  |  求和  |
|  avg  | 平均值 |
| count |  计数  |
|  max  | 最大值 |
|  min  | 最小值 |

{{<notice tip>}}

null不参与聚合函数的运算

{{</notice>}}

### having和where的区别

- 执行时机不同:where是分组之前进行过滤，不满足where条件，不参与分组;而having是分组之后对结果进行过滤。
- 判断条件不同:where不能对聚合函数进行判断，而having可以。

### 查询的执行顺序

where >聚合函数 >having

### 注意事项

{{<notice tip>}}

- **select** 子句中的字段一般为用于分组的字段和聚合函数（保证出现在**select**子句中但是没有被聚集的属性只能出现在**group by**子句中
- 在默认情况下，系统按照**group by**子句中指定的列升序排列，但是可以使用**order by**子句指定新的排列顺序。
- 任何出现在**having**子句中但没有被聚集的属性只能出现在**group by**子句中

{{</notice>}}

## 多表查询

### 连接查询

**笛卡尔积**：A表和B表元组的所有组合情况

示例代码：

```mysql
#隐式笛卡尔积
table a,table b
#显式笛卡尔积
table a join table b
```

**内连接**：查询A表和B表相交的部分（有条件的笛卡尔积）

语法：

```mysql
#隐式内连接
select 字段列表
from table a,table b
where condition

#显式内连接
select 字段列表
from table a join table b
on 连接条件
```

外连接：查询只存在A表或B表的部分

```mysql
#左外连接
select 字段列表
from table a left join table b
on 连接条件

#右外连接
select 字段列表
from table a right join table b
on 连接条件
```

### 子查询

子查询：SQL语句中嵌套select语句

类别

- 标量子查询:子查询返回的结果为单个值
- 列子查询:子查询返回的结果为一列
- 行子查询:子查询返回的结果为一行
- 表子查询:子查询返回的结果为多行多列

子查询的位置

- select后面：标量子查询
- from后面：表子查询
- where/having：标量/列/行子查询