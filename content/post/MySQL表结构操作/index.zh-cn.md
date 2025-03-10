---
date : '2024-11-03T18:46:17+08:00'
draft : false
title : 'MySQL表结构操作'
image : ""
categories : ["MySQL"]
tags : ["数据库"]
description : "对数据库表结构的基本操作"
---

## 创建表结构

### 代码结构

```mysql
# 创建一个新的表
create table table_name(
	字段1 字段类型[约束] [comment '关于字段的描述'],
	...
	字段n 字段类型[约束] [comment '关于字段的描述']
    <完整性约束>,
    ...
    <完整性约束>
)[comment 关于表的描述]

#创建与现有的某个表的模式相同的表
create table new_table like old_name

#将查询结果保存为一张表,默认插入数据
create table new_table as
<查询表达式>;

```

### 约束

**概念**：约束是作用于表中字段上的规则，用于限制存储在表中的数据

**目的**：保证数据库中数据的正确性、有效性和完整性。

**常见约束参考**

|   约束   |                        描述                        |     关键字      |
| :------: | :------------------------------------------------: | :-------------: |
| 非空约束 |                限制该字段不能为null                |  **not null**   |
| 唯一约束 |      保证该字段的所有数据都是唯一，不存在重复      |   **unique**    |
| 主键约束 |      主键是一个元组的唯一标识，要求非空且唯一      | **primary key** |
| 默认约束 |      保存数据时要是未指定该字段值则存入默认值      |   **default**   |
| 谓词约束 |             保证所有数据都满足条件谓词             |    **check**    |
| 外键约束 | 通过外键建立两张表的联系，保证数据的一致性和完整性 | **foreign key** |



**示例代码**

```mysql
create table student
(ID varchar (5) comment['唯一标识符'], 
 name varchar (20) not null,unique
 dept_name varchar (20),
 tot_cred numeric (3,0) check (tot_cred >= 0),
 age int default 18 #默认约束
 primary key (ID), #主键约束
 foreign key (dept_name) references department(dept_name) #外键约束
     on delete set null) #违反约束的方法：置为null
 unique(name,age); #多列唯一约束
```

### 数据类型

#### 数值类型

|   类型    | 大小（byte) |     有符号范围     | 无符号范围  |        描述        |                   备注                    |
| :-------: | :---------: | :----------------: | :---------: | :----------------: | :---------------------------------------: |
|  tinyint  |      1      |     (-128,127)     |   (0,255)   |       小整数       |                                           |
| smallint  |      2      |   (-32768,32767)   |  (0,65535)  |       大整数       |                                           |
| mediumint |      3      | (-8388608,8388607) | (0,1677215) |       大整数       |                                           |
|    int    |      4      |  (-2^31 ,2^31-1)   | (0,2^32-1)  |       大整数       |                                           |
|  bigint   |      8      |  (-2^63 ,2^63-1)   | (0,2^64-1)  |      极大整数      |                                           |
|   float   |      4      |                    |             |    单精度浮点值    | float(5,2)，其中5为数字长度，2为小数位数  |
|  double   |      8      |                    |             |    双精度浮点值    | double(5,2)，其中5为数字长度，2为小数位数 |
|  decimal  |             |                    |             | 小数值（精度最高） |                                           |

#### 字符类型

|    类型    | 大小（byte） |            描述             |                            备注                             |
| :--------: | :----------: | :-------------------------: | :---------------------------------------------------------: |
|    char    |    0~255     |         定长字符串          | char(10),最多只能存10个字符，不足10个字符也占有10个字符空间 |
|  varchar   |   0~63315    |         变长字符串          | varchar(10),最多只能存10个字符，不足10个字符按实际长度存储  |
|  tinyblob  |    0~255     | 不超过255个字符的二进制数据 |                                                             |
|  tinytext  |    0~255     |        短文本字符串         |                                                             |
|    blob    |   0~65535    |    二进制形式长文本数据     |                                                             |
|    text    |   0~65535    |         长文本数据          |                                                             |
| mediumblob |  0~16777215  |  二进制形式中等长文本数据   |                                                             |
| mediumtext |  0~16777215  |      中等长度文本数据       |                                                             |
|  longblob  | 0~4294967295 |  二进制形式的极大文本数据   |                                                             |
|  longtext  | 0~4294967295 |        极大文本数据         |                                                             |

#### 日期类型

|   类型    | 大小（byte） |        格式         |                   范围                    |           描述           |
| :-------: | :----------: | :-----------------: | :---------------------------------------: | :----------------------: |
|   date    |      3       |     YYYY-MM-DD      |          1000-01-01到 9999-12-31          |          日期值          |
|   time    |      3       |      HH:MM:SS       |          -838:59:59 到 838:59:59          |     时间值或持续时间     |
|   year    |      1       |        YYYY         |                1901到2155                 |          年份值          |
| datetime  |      8       | YYYY-MM-DD HH:MM:SS | 1000-01-01 00:00:00到 9999-12-31 23:59:59 |     混合日期和时间值     |
| timestamp |      4       | YYYY-MM-DD HH:MM:SS | 1000-01-01 00:00:00到 9999-12-31 23:59:59 | 混合日期和时间值，时间戳 |

时间域的提取

```mysql
extract(unit from date)
## unit为所提取的时间域
## date为字符串
```

字符串转时间类型

```mysql
cast('2024-12-21' as date) 
```

#### 大对象类型

- 大对象类型

  - 字符数据：clob

  - 二进制数据：blob

## 查询表结构

查询当前数据库的所有表

```mysql
show tables
```

查询指定表的表结构

```mysql
desc table_name
```

查询建表语句

```mysql
show create table table_name
```

## 修改表结构

添加字段

```mysql
alter table table_name
	add 字段名 字段类型（长度） [comment '关于字段的描述'] [约束];
```

修改字段类型

```mysql
alter table table_name
	modify 字段名 新字段类型（长度）;
```

修改字段名和字段类型

```mysql
alter table table_name
	change 旧字段名 新字段名 新类型（长度）[comment '关于字段的描述'] [约束];
```

删除字段

```mysql
alter table table_name
	drop column 字段名; 
#column可以不填写
alter table table_name
	drop 字段名; 
```

修改表名

```mysql
rename table 旧表名 to 新表名;
```

## 删除表结构

删除表中所有元组以及表的结构
```mysql
drop table 表名;
```
