---
date : '2024-11-07T16:51:41+08:00'
draft : false
title : 'SpringBoot事务管理'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发","数据库"]
description : "SpringBoot框架中实现数据库的事务管理"
---

## 数据库中的事务
概念：事务是一组操作的集合，它是一个不可分割的工作单位，这些操作 要么同时成功，要么同时失败。

操作

- 开启事务(一组操作开始前，开启事务)

  ```mysql
  start transaction;
  ```

- 提交事务(这组操作全部成功后，提交事务)

  ```mysql
  commit;
  ```

- 回滚事务(中间任何一个操作出现异常，回滚事务)

  ```mysql
  rollback;
  ```

  

## Spring中的事务管理

**@Transactional** 注解

- 位置：service层的方法，类，接口上

  - 修饰方法

    ```java
    @Transactional
    @Override
    public void delete(Integer id){
    	deptMapper.delete(id);
    	empMapper.deleteByDeptId(id);
    }
    ```

  - 修饰类

    ```java
    @Transactional
    @Service
    public class DeptServiceImpl implements DeptService{
    }
    ```

  - 修饰接口

    ```java
    @Transactional
    public interface DeptService {
    
    }
    ```

    

- 作用：将当前方法交给spring进行事务管理

  - 方法执行前，开启事务;
  - 成功执行完毕，提交事务;
  - 出现异常，回滚事务

## 事务属性

### 回滚

默认情况下，只有出现 **RuntimeException** 才回滚异常。**rollbackFor** 属性用于控制出现何种异常类型，回滚事务。

示例代码

```java
@Transactional(rollbackFor=Exception.class)
@Override
public void delete(Integer id)throws Exception {
	deptMapper.deleteById(id);
	empMapper.deleteByDeptId(id);
}
```

### 传播行为

传播行为：指的就是当一个事务方法被另一个事务方法调用时，这个事务方法应该如何进行事务控制。

常见的传播行为属性

|    属性值     |                             含义                             |
| :-----------: | :----------------------------------------------------------: |
|   REQUIRED    |         【默认值】需要事务，有则加入，无则创建新事务         |
| REQUIRES_NEW  |             需要新事务，无论有无，总是创建新事务             |
|   SUPPORTS    |          支持事务，有则加入，无则在无事务状态中运行          |
| NOT_SUPPORTED | 不支持事务，在无事务状态下运行,如果当前存在已有事务,则挂起当前事务 |
|   MANDATORY   |                    必须有事务，否则抛异常                    |
|     NEVER     |                    必须没事务，否则抛异常                    |

使用场景

- **REQUIRED**：大部分情况下都是用该传播行为即可。
- **REOUIRES NEW**：当我们不希望事务之间相互影响时，可以使用该传播行为。比如:下订单前需要记录日志，不论订单保存成功与
  否，都需要保证日志记录能够记录成功。