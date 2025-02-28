---
date : '2025-02-27T16:57:13+08:00'
draft : false
title : 'Redis的Java客户端和与SpringBoot的集成'
image : ""
categories : ["Redis"]
tags : [""]
description : "Redis的Java客户端和与SpringBoot的集成"
math : true
---

## Redis的Java客户端

- **`Jedis`** 适用于简单的同步操作和单线程环境。
- **`Lettuce`** 适用于高并发、高性能和多线程环境，尤其是需要异步和响应式编程的场景。
- **`Redisson`** 适用于复杂的分布式系统，提供丰富的分布式对象和服务，简化开发。

### Jedis

Jedis 是一款比较经典的 Java 客户端了，提供了比较全面的 Redis 命令。

- 简单易用：提供了直观的 API，使得开发者能够方便地与 Redis 进行交互。
- 使用广泛：在 Java 社区中被广泛采用，有丰富的文档和示例可供参考。
- 性能良好：在大多数情况下能够提供高效的 Redis 操作。
- 功能丰富：支持常见的 Redis 操作，如字符串、列表、哈希、集合等数据结构的操作。

缺点

- 线程安全问题：线程不安全，每个线程需独立使用 Jedis 实例。
- 不支持自动重连：在网络异常或 Redis 服务器重启时，需要手动处理重连。
- 阻塞操作：同步的 API，因此高并发下可能会发生阻塞

### Lettuce

Lettuce 其相对于 Jedis，其最突出的点就是线程安全，且其扩展性较高，它支持异步和响应式 API，底层基于 Netty 实现。

Lettuce 具有以下优点：

- **多线程安全** ：在多线程环境中可以安全使用。
- **自动重连** ：当网络连接出现问题时，能够自动重新连接。
- 支持多种编程模型：同步、异步、响应式，适应不同的应用场景

### Redisson

Redisson 是一个高级的 Redis 客户端，提供分布式和并行编程的支持，提供了丰富的分布式对象和服务，底层也是基于 Netty 实现通信。

优点：

- **高级特性** ：支持分布式锁、缓存、队列等常见场景。

- **支持集群** ：支持 Redis 集群模式，适应大规模分布式应用。

- **线程安全** ：无需手动处理多线程问题。

  

## SpringBoot集成Redis

**`SpringData`** 是Spring中数据操作的模块，包含对各种数据库的集成，其中对Redis的集成模块 **`SpringDataRedis`**

- 提供了对不同Redis客户端的整合（Lettuce和Jedis）
- 提供了RedisTemplate统一API来操作Redis
- 支持Redis的发布订阅模型
- 支持Redis哨兵和Redis集群
- 支持基于Lettuce的响应式编程
- 支持基于JDK、JSON、字符串、Spring对象的数据序列化及反序列化
- 支持基于Redis的JDKCollection实现

### 使用过程

- 引入对应依赖

  ```xml
  <!--Redis依赖-->
  <dependency>    
      <groupId>org.springframework.boot</groupId>    
      <artifactId>spring-boot-starter-data-redis</artifactId>
  </dependency>
  <!--连接池依赖-->
  <dependency>    
      <groupId>org.apache.commons</groupId>    
      <artifactId>commons-pool2</artifactId></dependency>
  
  ```

- 修改 **`application.yml`** 的spring.data.redis的字段配置连接信息

- 将 **`RedisTemplate`** 进行依赖注入和泛型

### 常用方法

|             **API**             | **返回值类型**  | **说明**              |
| :-----------------------------: | --------------- | --------------------- |
| **redisTemplate**.opsForValue() | ValueOperations | 操作String类型数据    |
| **redisTemplate**.opsForHash()  | HashOperations  | 操作Hash类型数据      |
| **redisTemplate**.opsForList()  | ListOperations  | 操作List类型数据      |
|  **redisTemplate**.opsForSet()  | SetOperations   | 操作Set类型数据       |
| **redisTemplate**.opsForZSet()  | ZSetOperations  | 操作SortedSet类型数据 |
|        **redisTemplate**        |                 | 通用的命令            |

### 对象序列化

RedisTemplate可以接收任意Object作为值写入Redis，只不过写入前会把Object序列化为字节形式，默认是采用JDK序列化

缺点：

- 可读性差
- 内存占用较大

#### 自定义序列化

RedisTemplate可以自定义序列化方式。设置一个配置类来自定义RedisTemplate的序列方式

- 通常对key采用string序列化
- 对value采用json序列化

```java
@Bean
public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory)throws UnknownHostException 
{	
    // 创建Template
    RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>();    
    // 设置连接工厂   
    redisTemplate.setConnectionFactory(redisConnectionFactory);// 设置序列化工具 
    GenericJackson2JsonRedisSerializer jsonRedisSerializer = new GenericJackson2JsonRedisSerializer();
    // key和 hashKey采用 string序列化   
    redisTemplate.setKeySerializer(RedisSerializer.string());
    redisTemplate.setHashKeySerializer(RedisSerializer.string());
    // value和 hashValue采用 JSON序列化    
	redisTemplate.setValueSerializer(jsonRedisSerializer); 
    redisTemplate.setHashValueSerializer(jsonRedisSerializer);
    return redisTemplate;
}
```

保存结果

```
{"@class":"org.example.redisdemo.pojo.User","name":"zhangsan","age":18,"id":1}
```



#### 使用StringRedisTemplate

- 使用StringRedisTemplate
- 写入Redis时，使用 **`ObjectMapping`** 手动把对象序列化为JSON
- 读取Redis时，**`ObjectMapping`**  手动把读取到的JSON反序列化为对象