---
date : '2024-11-06T17:26:14+08:00'
draft : false
title : 'MyBatis基本使用'
image : ""
categories : ["MyBatis"]
tags : ["数据库"]
description : "MyBatis框架的基本使用"
---

## 在Mapper接口中基于注解书写sql语句

### 设置动态参数

```java
#{参数名}
```



### 删除操作

#### sql语句

```sql
delete from emp where id=#{id}
```

#### 接口方法

```java
@Mapper
public interface EmpMapper
//根据ID删除数据
@Delete("delete from emp where id=#{id}")
public void delete(Integer id):
```

### 添加操作

#### sql语句

```sql
insert into emp(username, name, gender, image, job, entrydate, dept_id, create_time, update_time) 
values(#{username), #{name}, #{gender}, #{image}, #{job}, #{entrydate}, #{deptld}, #{createTime}, #{updateTime}
```

#### 接口方法

```java
@Mapper
public interface EmpMapper
//根据ID添加数据
@Insert("insert into emp(username, name, gender, image, job, entrydate, dept_id, create_time, update_time)" +"values(#{username), #{name}, #{gender}, #{image}, #{job}, #{entrydate}, #{deptld}, #{createTime}, #{updateTime}")
public void insert(Emp emp);
```

#### 主键返回

描述：在数据添加成功后，需要获取插入数据库数据的主键。

实现：在@Insert上添加注解 **@Options(keyProperty = "id", useGeneratedKeys = true)** 会自动将生成的主键值赋给id属性

### 更新操作

#### sql语句

```sql
update emp set username=#{username),name=#{name}, gender=#{gender}, image=#{image}, job=#{job}, entrydate=#{entrydate}, dept_Id=#{deptld}, create_time=#{createTime}, update_time=#{updateTime} where id=#{id}
```

#### 接口方法

```java
@Mapper
public interface EmpMapper
@Update("update emp set username=#{username), name=#{name}, gender=#{gender}, image=#{image}, job=#{job}, entrydate=#{entrydate}, dept_Id=#{deptld}, create_time=#{createTime}, update_time=#{updateTime} where id=#{id}")
public void update(Emp emp);
```

{{<notice tip>}}

数据封装

- 实体类属性名和数据库表查询返回的字段名一致，mybatis会自动封装。
- 如果实体类属性名 和 数据库表查询返回的字段名不一致，不能自动封装。

解决方案

- 方案一：给字段起别名与实体类属性名相同

- 方案二：使用@Results注解手动指定映射，@Result封装映射

  - column属性指定数据库字段
  - property属性指定实体类属性

  ```java
  @Results({
      @Result(column="数据库字段",property="实体类属性")
  })
  ```

{{</notice>}}

### 查询操作

#### sql语句

```sql
select *
from emp
where name like '%李%'
```

### 接口方法

```java
@Mapper
public interface EmpMapper
@Select("select * from emp where name like '%#{name}%'")
public List<User> list(String name)
```

{{<notice warning>}}

在模糊匹配中%#{name}%不建议使用（不是预编译sql语句）

可以使用concat(‘%','#{name}','%')

{{</notice>}}



## 在Mapper.xml中基于映射文件属性sql语句

### 使用规范

- XML映射文件的名称与Mapper接口名称一致，并且将XML映射文件和Mapper接口放置在相同包下(同包同名)。

- XML映射文件的namespace属性为Mapper接口全限定名一致。

- XML映射文件中sql语句的id与Mapper 接口中的方法名一致，并保持返回类型一致。

- 编写sql语句的格式

  ```xml
  <操作名 id="函数名" resultType="单条记录的实体类全类名">
      sql语句
  </操作名>
  ```

  {{<notice tip>}}

  只有select操作需要resultType

  {{</notice>}}

### 动态SQL语句

####  \< if \>标签

​	描述：用于判断条件是否成立。使用test属性进行条件判断，如果条件为true，则拼接SQL

​	示例代码

```xml
<select id="list" resultType="com.itheima.pojo.Emp">
	select *
	from omp
	where
	<if test="name !=null">
		name like concat("%",#{name},"%")
	</if>
</select>
```

#### \<where\>标签

​	描述：动态生成where子句，若子标签的条件都不满足则不会生成where子句，同时会删除子句开头的条件运算符

​	示例代码

```xml
<select id="list" resultType="com.itheima.pojo.Emp">
	select *
	from emp
	<where>
        <if test="name !=null">
		name like concat("%",#{name},"%")
		</if>
    </where>
</select>
```

#### \<set\>标签

描述：动态生成set子句

示例代码

```xml
<update id="update">
    update emp
    <set>
        <if test="name !=null">
			name=#{name}
		</if>
    </set>
    where id=#{id}
</update>
```

#### \<foreach\>标签

描述：用于遍历元素

属性

- collection：遍历的集合
- item：集合中的元素
- separator：分隔符
- open：遍历开始前的SQL语句
- close：遍历结束后的SQL语句

示例代码

```xml
<delete id="delete">
    delete from emp where id in
    <foreach collection="遍历的集合",item="集合中的元素",separator="分隔符",open="(",close=")">
        #{id}
    </foreach>
</delete>
```

#### \<sql\>标签和\<include\>标签

- \<sql\>:定义可重用的 SQL片段。
- \<include\>:通过属性refid，指定包含的sql片段。

示例代码

```xml
<sql id="commonSelect">
select id, username
from emp
</sql>


<select id="getById" resultTypea"com.itheima.pojo.Emp">
    <include refid="commonselect"/>
    where id = #{id}
</select>
```

