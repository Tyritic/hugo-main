
---
date : '2024-11-07T17:14:44+08:00'
draft : false
title : 'MyBatis-Plus'
image : ""
categories : ["MyBatis"]
tags : ["数据库","后端开发"]
description : "MyBatis-Plus相关知识"
---

## 🎯 MyBatis-Plus简介

MyBatis-Plus（简称 MP）是一个 MyBatis 的增强工具，在 MyBatis 的基础上只做增强不做改变，为简化开发、提高效率而生。

**愿景**：成为 MyBatis 最好的搭档，就像 魂斗罗 中的 1P、2P，基友搭配，效率翻倍。

---

### ✨ 特性

- 无侵入：只做增强不做改变，引入它不会对现有工程产生影响，如丝般顺滑
- 损耗小：启动即会自动注入基本 CURD，性能基本无损耗，直接面向对象操作
- 强大的 CRUD 操作：内置通用 Mapper、通用 Service，仅仅通过少量配置即可实现单表大部分 CRUD 操作，更有强大的条件构造器，满足各类使用需求
- 支持 Lambda 形式调用：通过 Lambda 表达式，方便的编写各类查询条件，无需再担心字段写错
- 支持主键自动生成：支持多达 4 种主键策略（内含分布式唯一 ID 生成器 - Sequence），可自由配置，完美解决主键问题
- 支持 ActiveRecord 模式：支持 ActiveRecord 形式调用，实体类只需继承 Model 类即可进行强大的 CRUD 操作
- 支持自定义全局通用操作：支持全局通用方法注入（ Write once, use anywhere ）
- 内置代码生成器：采用代码或者 Maven 插件可快速生成 Mapper 、 Model 、 Service 、 Controller 层代码，支持模板引擎，更有超多自定义配置等您来使用
- 内置分页插件：基于 MyBatis 物理分页，开发者无需关心具体操作，配置好插件之后，写分页等同于普通 List 查询
- 分页插件支持多种数据库：支持 MySQL、MariaDB、Oracle、DB2、H2、HSQL、SQLite、Postgre、SQLServer 等多种数据库
- 内置性能分析插件：可输出 SQL 语句以及其执行时间，建议开发测试时启用该功能，能快速揪出慢查询
- 内置全局拦截插件：提供全表 delete 、 update 操作智能分析阻断，也可自定义拦截规则，预防误操作

---

### 🔗 框架结构

&lt;div align="center"&gt;
  &lt;img src="WechatIMG9017.jpg" alt="框架结构" width="82%"&gt;
&lt;/div&gt;

---

### 🔧 快速开始

1. 在pom.xml中引入MyBatis-Plus的依赖

   ```xml
   &lt;dependency&gt;
       &lt;groupId&gt;com.baomidou&lt;/groupId&gt;
       &lt;artifactId&gt;mybatis-plus-boot-starter&lt;/artifactId&gt;
       &lt;version&gt;3.4.3&lt;/version&gt;
   &lt;/dependency&gt;
   ```

2. 在application.yml中配置数据库相关信息

   ```yaml
   spring:
     datasource:
       type: com.alibaba.druid.pool.DruidDataSource
       driver-class-name: com.mysql.cj.jdbc.Driver
       url: jdbc:mysql://localhost:3306/ssm_db?serverTimezone=UTC
       username: root
       password: 123456
   ```

3. 在mapper文件夹下编写接口继承于BaseMapper，参数为对应的实体类

   ```java
   @Mapper
   public interface UserMapper extends BaseMapper&lt;User&gt; {
   }
   ```

4. 在启动类中添加@MapperScan("mapper文件对应的包名")

   ```java
   @SpringBootApplication
   @MapperScan("com.itheima.mapper")
   public class MybatisplusDemo1Application {
       public static void main(String[] args) {
           SpringApplication.run(MybatisplusDemo1Application.class, args);
       }
   }
   ```

5. 编写实体类

   ```java
   @Data
   public class User {
       private Long id;
       private String name;
       private String password;
       private Integer age;
       private String tel;
   }
   ```

6. 在test中编写测试方法

   ```java
   @SpringBootTest
   class MybatisplusDemo1ApplicationTests {
       @Autowired
       private UserMapper userMapper;
       @Test
       void testGetAll() {
           List&lt;User&gt; users = userMapper.selectList(null);
           System.out.println(users);
       }
   }
   ```

---

## 📌 常用注解

- @TableName：表名注解，标识实体类对应的表，参数为表名
- @TableId：主键注解，标识主键，当主键名和属性名不一致时必须用此注解，参数value设置字段名，参数type设置主键生成策略
- @TableField：字段注解，标识普通字段，参数为字段名，存在该注解时优先使用注解参数内的名称，参数exist设置是否查询该字段

---

## 🔄 主键生成策略

在实体类中的主键上添加@TableId注解的type参数设置主键生成策略

```java
@TableId(type=主键生成策略)
```

主键生成策略

- IdType.AUTO：使用数据库自增策略生成主键
- IdType.NONE：不设置主键生成策略，使用雪花算法生成主键
- IdType.INPUT：用户手动输入主键值
- IdType.ASSIGN_ID：使用雪花算法生成主键（可以用于数值类型和String）
- IdType.ASSIGN_UUID：使用UUID生成主键（只能用于String）

{{&lt;notice tip&gt;}}

可以在配置文件中通过mybatis-plus.global-config.db-config.id-type设置默认主键生成策略

{{&lt;/notice&gt;}}

---

## 🔗 条件查询器

### 🧠 基本条件查询

1. 创建条件查询对象的格式

   ```java
   QueryWrapper&lt;实体类&gt; 变量名 = new QueryWrapper&lt;&gt;();
   ```

2. 具体查询条件

   - ge：大于等于 &gt;=，参数为字段名和值
   - gt：大于 &gt;，参数为字段名和值
   - le：小于等于 &lt;=，参数为字段名和值
   - lt：小于 &lt;，参数为字段名和值
   - eq：等于 =，参数为字段名和值
   - ne：不等于 !=，参数为字段名和值
   - between：在范围之间，参数为字段名和两个值
   - notBetween：不在范围之间，参数为字段名和两个值
   - like：模糊查询，参数为字段名和值（%值%）
   - notLike：模糊查询，参数为字段名和值（不含%值%）
   - likeLeft：模糊查询，参数为字段名和值（%值）
   - likeRight：模糊查询，参数为字段名和值（值%）
   - isNull：查询为空的数据，参数为字段名
   - isNotNull：查询不为空的数据，参数为字段名
   - in：包含，参数为字段名和一个List集合或数组
   - notIn：不包含，参数为字段名和一个List集合或数组

   示例

   ```java
   QueryWrapper&lt;User&gt; qw1 = new QueryWrapper&lt;&gt;();
   //查询年龄大于等于18岁的人
   qw1.ge("age",18);
   List&lt;User&gt; users = userMapper.selectList(qw1);
   System.out.println(users);
   ```

3. select：设置查询的字段，参数为字段名

   ```java
   QueryWrapper&lt;User&gt; qw2 = new QueryWrapper&lt;&gt;();
   qw2.select("name","age");
   List&lt;User&gt; users2 = userMapper.selectList(qw2);
   System.out.println(users2);
   ```

4. orderBy：设置排序，参数为是否升序（false为降序），和字段名

   ```java
   QueryWrapper&lt;User&gt; qw3 = new QueryWrapper&lt;&gt;();
   qw3.orderBy(true,true,"age");
   List&lt;User&gt; users3 = userMapper.selectList(qw3);
   System.out.println(users3);
   ```

5. or：设置多条件查询用or连接（默认and连接）

   ```java
   QueryWrapper&lt;User&gt; qw4 = new QueryWrapper&lt;&gt;();
   qw4.eq("age",18).or().eq("age",19);
   List&lt;User&gt; users4 = userMapper.selectList(qw4);
   System.out.println(users4);
   ```

---

### 💫 条件查询器的链式写法

条件查询器支持链式写法

```java
QueryWrapper&lt;User&gt; qw1 = new QueryWrapper&lt;&gt;();
qw1.ge("age",18).le("age",30);
List&lt;User&gt; users = userMapper.selectList(qw1);
System.out.println(users);
```

---

### 🔍 lambda条件查询器

创建lambda条件查询器的格式

```java
LambdaQueryWrapper&lt;实体类&gt; 变量名 = new LambdaQueryWrapper&lt;&gt;();
```

{{&lt;notice tip&gt;}}

lambda条件查询器的方法参数中，字段名以实体类的getter方法的形式出现

{{&lt;/notice&gt;}}

示例

```java
LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;&gt;();
lqw.ge(User::getAge,18);
List&lt;User&gt; users = userMapper.selectList(lqw);
System.out.println(users);
```

---

### 🔒 条件判断

在lambda条件查询器中所有条件查询方法都可以添加一个条件判断参数，只有条件判断参数为true时才会执行该条件查询方法

示例

```java
//模拟前端传来的数据
Integer age1 = 10;
Integer age2 = 30;
LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;&gt;();
lqw.ge(age1 != null,User::getAge,age1);
lqw.le(age2 != null,User::getAge,age2);
List&lt;User&gt; users = userMapper.selectList(lqw);
System.out.println(users);
```

---

### 📝 条件更新和条件删除

- 使用条件查询器进行条件删除，在delete方法中传入条件查询对象

  ```java
  LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;&gt;();
  lqw.eq(User::getName,"Tom");
  userMapper.delete(lqw);
  ```

- 使用条件查询器进行条件更新，在update方法中传入条件查询对象

  ```java
  LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;&gt;();
  lqw.eq(User::getName,"Tom");
  User user = new User();
  user.setAge(30);
  userMapper.update(user,lqw);
  ```

---

## 📄 条件查询接口

条件查询接口提供了比条件查询器更复杂的条件查询方法

创建条件查询接口的格式

```java
QueryWrapper&lt;实体类&gt; 变量名 = new QueryWrapper&lt;&gt;();
```

{{&lt;notice tip&gt;}}

selectOne方法只能查询出一条数据，查询多条数据会报错，selectCount方法会查询出符合条件的数据的数量

{{&lt;/notice&gt;}}

---

## 🔌 Service层接口

MyBatis-Plus在Service层提供了一个Service层的接口IService和一个Service层的实现类ServiceImpl，可以让我们继承使用，ServiceImpl有两个泛型，第一个是对应的mapper接口，第二个是对应的实体类

---

### 🔧 快速使用

1. 编写Service接口继承于IService

   ```java
   public interface UserService extends IService&lt;User&gt; {
   }
   ```

2. 编写Service实现类继承于ServiceImpl并实现Service接口

   ```java
   @Service
   public class UserServiceImpl extends ServiceImpl&lt;UserMapper, User&gt; implements UserService {
   }
   ```

3. 在测试类中编写测试方法

   ```java
   @SpringBootTest
   class MybatisplusDemo1ApplicationTests {
       @Autowired
       private UserService userService;
       @Test
       void testGetAll() {
           List&lt;User&gt; users = userService.list();
           System.out.println(users);
       }
   }
   ```

---

### 📌 常用方法

- list：查询所有数据
- getById：根据id查询数据
- save：添加数据
- saveBatch：批量添加数据
- removeById：根据id删除数据
- removeByIds：根据id批量删除数据
- updateById：根据id更新数据
- count：查询数据数量

---

## 📊 MyBatis-Plus分页功能

1. 配置分页拦截器并注入到Spring容器中

   ```java
   @Configuration
   public class MPConfig {
       @Bean
       public MybatisPlusInterceptor mybatisPlusInterceptor(){
           MybatisPlusInterceptor mpInterceptor = new MybatisPlusInterceptor();
           mpInterceptor.addInnerInterceptor(new PaginationInnerInterceptor());
           return mpInterceptor;
       }
   }
   ```

2. 在测试类中编写测试方法，创建Page对象并传入selectPage方法中，Page对象有两个参数，第一个为当前页码，第二个为每页显示的条数

   ```java
   @SpringBootTest
   class MybatisplusDemo1ApplicationTests {
       @Autowired
       private UserMapper userMapper;
       @Test
       void testGetPage() {
           Page&lt;User&gt; page = new Page&lt;&gt;(1, 3);
           userMapper.selectPage(page, null);
           System.out.println(page.getCurrent());//当前页码
           System.out.println(page.getSize());//每页显示的条数
           System.out.println(page.getTotal());//总条数
           System.out.println(page.getPages());//总页数
           System.out.println(page.getRecords());//每页的具体数据
       }
   }
   ```

---

## 📝 MyBatis-Plus映射数据库字段和实体类属性

在配置文件中通过mybatis-plus.global-config.db-config.table-prefix设置实体类对应表的前缀名，避免每一个实体类都要设置@TableName注解

```yaml
mybatis-plus:
  global-config:
    db-config:
      table-prefix: tbl_
```

---

## 🔒 MyBatis-Plus乐观锁

1. 在数据库表中添加version字段，设置初始值为1

2. 在实体类中添加version属性，并用@Version注解修饰

   ```java
   @Data
   public class User {
       private Long id;
       private String name;
       private String password;
       private Integer age;
       private String tel;
       @Version
       private Integer version;
   }
   ```

3. 配置乐观锁拦截器并注入到Spring容器中

   ```java
   @Configuration
   public class MPConfig {
       @Bean
       public MybatisPlusInterceptor mybatisPlusInterceptor(){
           MybatisPlusInterceptor mpInterceptor = new MybatisPlusInterceptor();
           mpInterceptor.addInnerInterceptor(new PaginationInnerInterceptor());
           mpInterceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());
           return mpInterceptor;
       }
   }
   ```

4. 在测试类中编写测试方法

   ```java
   @SpringBootTest
   class MybatisplusDemo1ApplicationTests {
       @Autowired
       private UserMapper userMapper;
       @Test
       void testGetPage() {
           User user = userMapper.selectById(1L);
           User user2 = userMapper.selectById(1L);
           user.setAge(20);
           user2.setAge(30);
           userMapper.updateById(user);
           userMapper.updateById(user2);
       }
   }
   ```

---

## 🔐 MyBatis-Plus逻辑删除

1. 在数据库表中添加deleted字段，设置初始值为0

2. 在实体类中添加deleted属性，并用@TableLogic注解修饰

   ```java
   @Data
   public class User {
       private Long id;
       private String name;
       private String password;
       private Integer age;
       private String tel;
       @Version
       private Integer version;
       @TableLogic
       private Integer deleted;
   }
   ```

3. 在配置文件中设置逻辑删除的值，没删除为0，删除为1（该步可以省略，有默认值）

   ```yaml
   mybatis-plus:
     global-config:
       db-config:
         logic-delete-field: deleted
         logic-delete-value: 1
         logic-not-delete-value: 0
   ```

4. 在测试类中编写测试方法

   ```java
   @SpringBootTest
   class MybatisplusDemo1ApplicationTests {
       @Autowired
       private UserMapper userMapper;
       @Test
       void testLogicDelete() {
           userMapper.deleteById(1L);
       }
   }
   ```

---

## 🔧 MyBatis-Plus性能分析

1. 在配置文件中设置日志输出，mybatis-plus.configuration.log-impl设置日志输出

   ```yaml
   mybatis-plus:
     configuration:
       log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
   ```

2. 配置性能分析拦截器并注入到Spring容器中

   ```java
   @Configuration
   public class MPConfig {
       @Bean
       public MybatisPlusInterceptor mybatisPlusInterceptor(){
           MybatisPlusInterceptor mpInterceptor = new MybatisPlusInterceptor();
           mpInterceptor.addInnerInterceptor(new PaginationInnerInterceptor());
           mpInterceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());
           mpInterceptor.addInnerInterceptor(new BlockAttackInnerInterceptor());
           return mpInterceptor;
       }
   }
   ```

