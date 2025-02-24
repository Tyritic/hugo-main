---
date : '2024-11-07T16:51:41+08:00'
draft : false
title : 'Spring事务管理'
image : ""
categories : ["SpringBoot","Spring"]
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

Spring 事务的本质其实就是数据库对事务的支持，没有数据库的事务支持，Spring 是无法提供事务功能的。Spring 只提供统一事务管理接口，具体实现都是由各数据库自己实现，数据库事务的提交和回滚是通过数据库自己的事务机制实现。

### 编程式事务

编程式事务是指将事务管理代码嵌入嵌入到业务代码中，来控制事务的提交和回滚。

编程式事务可以使用 **`TransactionTemplate`** 和 **`PlatformTransactionManager`** 来实现，需要显式执行事务。允许我们在代码中直接控制事务的边界，通过编程方式明确指定事务的开始、提交和回滚。

```java
@Autowired
private TransactionTemplate transactionTemplate;
public void testTransaction() {

        transactionTemplate.execute(new TransactionCallbackWithoutResult() {
            @Override
            protected void doInTransactionWithoutResult(TransactionStatus transactionStatus) {

                try {

                    // ....  业务代码
                } catch (Exception e){
                    //回滚
                    transactionStatus.setRollbackOnly();
                }

            }
        });
}
```

### 声明式事务

声明式事务是建立在 AOP 之上的。其本质是通过 AOP 功能，对方法前后进行拦截，将事务处理的功能编织到拦截的方法中，也就是在目标方法开始之前启动一个事务，在目标方法执行完之后根据执行情况提交或者回滚事务。

**`@Transactional`** 注解

- 位置：service层的方法，类，接口上

  - 修饰方法：**该注解只能应用到 public 方法上，否则不生效。**

    ```java
    @Transactional
    @Override
    public void delete(Integer id){
    	deptMapper.delete(id);
    	empMapper.deleteByDeptId(id);
    }
    ```

  - 修饰类：如果这个注解使用在类上的话，表明该注解对该类中所有的 public 方法都生效。

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

| 属性名      | 说明                                                         |
| :---------- | :----------------------------------------------------------- |
| propagation | 事务的传播行为，默认值为 REQUIRED                            |
| isolation   | 事务的隔离级别，默认值采用 DEFAULT                           |
| timeout     | 事务的超时时间，默认值为-1（不会超时）。如果超过该时间限制但事务还没有完成，则自动回滚事务。 |
| readOnly    | 指定事务是否为只读事务，默认值为 false。                     |
| rollbackFor | 用于指定能够触发事务回滚的异常类型，并且可以指定多个异常类型。 |



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

传播行为：指的就是当一个事务方法被另一个事务方法调用时，这个事务方法应该如何进行事务控制。主要作用是**定义和管理事务边界**，尤其是一个事务方法调用另一个事务方法时，事务如何传播的问题。它解决了多个事务方法嵌套执行时，是否要开启新事务、复用现有事务或者挂起事务等复杂情况。

常见的传播行为属性

|    属性值     |                             含义                             |
| :-----------: | :----------------------------------------------------------: |
|   REQUIRED    |         【默认值】需要事务，有则加入，无则创建新事务         |
| REQUIRES_NEW  |             需要新事务，无论有无，总是创建新事务             |
|   SUPPORTS    |          支持事务，有则加入，无则在无事务状态中运行          |
| NOT_SUPPORTED | 不支持事务，在无事务状态下运行,如果当前存在已有事务,则挂起当前事务 |
|   MANDATORY   |                    必须有事务，否则抛异常                    |
|    NESTED     | 如果当前事务存在，则在嵌套事务中执行，内层事务依赖外层事务，如果外层失败，则会回滚内层，内层失败不影响外层。 |
|     NEVER     |                    必须没事务，否则抛异常                    |

使用场景

- **REQUIRED**：大部分情况下都是用该传播行为。
  - 如果外部方法没有开启事务的话，`Propagation.REQUIRED`修饰的内部方法会新开启自己的事务，且开启的事务相互独立，互不干扰。
  - 如果外部方法开启事务并且被`Propagation.REQUIRED`的话，所有`Propagation.REQUIRED`修饰的内部方法和外部方法均属于同一事务 ，只要一个方法回滚，整个事务均回滚。
- **REOUIRES NEW**：当我们不希望事务之间相互影响时，可以使用该传播行为。
  - 创建一个新的事务，如果当前存在事务，则把当前事务挂起。

### 隔离级别

- **DEFAULT**（默认）：使用底层数据库的默认隔离级别。如果数据库没有特定的设置，通常默认为 `READ_COMMITTED`。
- **READ_UNCOMMITTED**（读未提交）：最低的隔离级别，允许事务读取尚未提交的数据，可能会导致脏读、不可重复读和幻读。
- **READ_COMMITTED**（读已提交）：仅允许读取已经提交的数据，避免了脏读，但可能会出现不可重复读和幻读问题。
- **REPEATABLE_READ**（可重复读）：确保在同一个事务内的多次读取结果一致，避免脏读和不可重复读，但可能会有幻读问题。
- **SERIALIZABLE**（可串行化）：最高的隔离级别，通过强制事务按顺序执行，完全避免脏读、不可重复读和幻读，代价是性能显著下降。

{{<notice tip>}}

- **脏读（Dirty Read）**：一个事务读取了另一个尚未提交的事务的数据，如果该事务回滚，则数据是不一致的。
- **不可重复读（Non-repeatable Read）**：在同一事务内的多次读取，前后数据不一致，因为其他事务修改了该数据并提交。
- **幻读（Phantom Read）**：在一个事务内的多次查询，查询结果集不同，因为其他事务插入或删除了数据。

{{</notice>}}

## 声明式事务的实现原理

Spring 的声明式事务管理是通过 AOP（面向切面编程）和代理机制实现的。

- **在 Bean 初始化阶段创建代理对象**
  - Spring 容器在初始化单例 Bean 的时候，会遍历所有的 **`BeanPostProcessor`** 实现类，并执行其 **`postProcessAfterInitialization`** 方法。
  - 在执行 **`postProcessAfterInitialization`** 方法时会遍历容器中所有的切面，查找与当前 Bean 匹配的切面，这里会获取事务的属性切面，也就是 `@Transactional` 注解及其属性值。
  - 然后根据得到的切面创建一个代理对象，默认使用 JDK 动态代理创建代理，如果目标类是接口，则使用 JDK 动态代理，否则使用 Cglib。
- **在执行目标方法时进行事务增强操作**
  - 当通过代理对象调用 Bean 方法的时候，会触发对应的 AOP 增强拦截器，声明式事务是一种环绕增强，对应接口为`MethodInterceptor`

## 声明式事务失效的情况

- **`rollbackFor`** 设置错误，Spring默认没有任何设置（**`RuntimeException`** 或者 **`Error`** 才能捕获），则方法内抛出其他异常则不会回滚
- 同一个类中方法调用，因此事务是基于动态代理实现的，同类的方法调用不会走代理方法，因此事务自然就失效了。
- **`@Transactional`** 应用在非 public 修饰的方法上，Spring 事务管理器判断非公共方法则不应用事务。