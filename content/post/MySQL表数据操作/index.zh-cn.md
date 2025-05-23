---
date : '2024-11-04T14:57:14+08:00'
draft : false
title : 'MySQL表数据操作'
image : ""
categories : ["MySQL"]
tags : ["数据库"]
description : "对MySQL表中元组的操作"
---
## 插入元组

指定字段添加元组

```mysql
insert into table_name (字段1,子段2,...子段n) values(值1,..值n);
```

全部字段添加元组

```mysql
insert into table_name values(值1,值2,...值n);
```

批量添加指定子段的元组

```mysql
insert into table_name (子段1,子段2,...子段n) values(值1,...值n),..(值1,...值n);
```

全部数据批量添加

```mysql
insert into table_name values(值1,...值n),..(值1,...值n);
```

## 更新元组

更新符合指定条件的元组

```mysql
update table_name set 字段1=值1,..字段n=值n [where condition]
```

## 删除元组

删除表中的元组但是不删除表（当不存在条件时为删除所有元组
```mysql
delete from table_name [where condition]
```

删除表中的所有元组但是保留表结构（同时按照原来的建表语句重新建立表）

```mysql
truncate table table_name
```

