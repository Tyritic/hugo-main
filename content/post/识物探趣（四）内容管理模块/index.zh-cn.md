---
date : '2025-01-13T18:13:37+08:00'
draft : false
title : '识物探趣（四）内容管理模块的设计过程'
image : ""
categories : ["个人项目"]
tags : ["后端开发"]
description : "识物探趣项目中内容管理模块中的缓存问题"
math : true
---

## 内容模块库表设计

### 单一文章

#### 文章表

| 字段名         | 数据类型        | 默认值  | 描述           |
| :------------: | :-------------: | :-----: | :------------: |
| `id`           | `int(10) unsigned` | `AUTO_INCREMENT` | 主键ID         |
| `user_id`      | `int(10) unsigned` | `0`     | 用户ID         |
| `article_type` | `tinyint(4)`     | `1`     | 文章类型（1-博文，2-问答） |
| `title`        | `varchar(120)`   | `''`    | 文章标题       |
| `short_title`  | `varchar(120)`   | `''`    | 短标题         |
| `picture`      | `varchar(128)`   | `''`    | 文章头图       |
| `summary`      | `varchar(300)`   | `''`    | 文章摘要       |
| `category_id`  | `int(10) unsigned` | `0`     | 类目ID         |
| `source`       | `tinyint(4)`     | `1`     | 来源（1-原创，2-AI，3-翻译） |
| `source_url`   | `varchar(128)`   | `'1'`   | 原文链接       |
| `offical_stat` | `int(10) unsigned` | `0`     | 官方状态（0-非官方，1-官方） |
| `topping_stat` | `int(10) unsigned` | `0`     | 置顶状态（0-不置顶，1-置顶） |
| `cream_stat`   | `int(10) unsigned` | `0`     | 加精状态（0-不加精，1-加精） |
| `status`       | `tinyint(4)`     | `0`     | 状态（0-未发布，1-已发布） |
| `deleted`      | `tinyint(4)`     | `0`     | 是否删除       |
| `create_time`  | `timestamp`      | `CURRENT_TIMESTAMP` | 创建时间       |
| `update_time`  | `timestamp`      | `CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 最后更新时间   |

---

#### 文章详情表

| 字段名         | 数据类型        | 默认值  | 描述           |
| :------------: | :-------------: | :-----: | :------------: |
| `id`           | `int(10) unsigned` | `AUTO_INCREMENT` | 主键ID         |
| `article_id`   | `int(10) unsigned` | `0`     | 文章ID         |
| `version`      | `int(10) unsigned` | `0`     | 版本号         |
| `content`      | `longtext`       | `NULL`  | 文章内容       |
| `deleted`      | `tinyint(4)`     | `0`     | 是否删除       |
| `create_time`  | `timestamp`      | `CURRENT_TIMESTAMP` | 创建时间       |
| `update_time`  | `timestamp`      | `CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 最后更新时间   |

#### 分类表

文章对应的分类，要求一个文章只能挂在一个分类下。分类表和文章表之间通过

| 字段名         | 数据类型        | 默认值  | 描述           |
| :------------: | :-------------: | :-----: | :------------: |
| `id`           | `int(10) unsigned` | `AUTO_INCREMENT` | 主键ID         |
| `category_name`| `varchar(64)`   | `''`    | 类目名称       |
| `status`       | `tinyint(4)`     | `0`     | 状态（0-未发布，1-已发布） |
| `rank`         | `tinyint(4)`     | `0`     | 排序           |
| `deleted`      | `tinyint(4)`     | `0`     | 是否删除       |
| `create_time`  | `timestamp`      | `CURRENT_TIMESTAMP` | 创建时间       |
| `update_time`  | `timestamp`      | `CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 最后更新时间   |

### 专栏文章

专栏主要是一系列文章的合集，通过专栏-文章表建立专栏和文字之间的映射关系

#### 专栏表

| 字段名           | 数据类型        | 默认值  | 描述           |
| :--------------: | :-------------: | :-----: | :------------: |
| `id`             | `int(10) unsigned` | `AUTO_INCREMENT` | 专栏ID         |
| `column_name`    | `varchar(64)`    | `''`    | 专栏名称       |
| `user_id`        | `int(10) unsigned` | `0`     | 作者ID         |
| `introduction`   | `varchar(256)`   | `''`    | 专栏简述       |
| `cover`          | `varchar(128)`   | `''`    | 专栏封面       |
| `state`          | `tinyint(3) unsigned` | `0` | 状态（0-审核中，1-连载，2-完结） |
| `publish_time`   | `timestamp`      | `'1970-01-02 00:00:00'` | 上线时间       |
| `create_time`    | `timestamp`      | `CURRENT_TIMESTAMP` | 创建时间       |
| `update_time`    | `timestamp`      | `CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 最后更新时间   |
| `section`        | `int(10) unsigned` | `0`     | 排序           |
| `nums`           | `int(10) unsigned` | `0`     | 专栏预计的更新的文章数 |
| `type`           | `int(10) unsigned` | `0`     | 专栏类型（0-免费，1-登录阅读，2-限时免费） |
| `free_start_time`| `timestamp`      | `'1970-01-02 00:00:00'` | 限时免费开始时间 |
| `free_end_time`  | `timestamp`      | `'1970-01-02 00:00:00'` | 限时免费结束时间 |

#### 专栏-文章表

| 字段名         | 数据类型        | 默认值  | 描述           |
| :------------: | :-------------: | :-----: | :------------: |
| `id`           | `int(10) unsigned` | `AUTO_INCREMENT` | 主键ID         |
| `column_id`    | `int(10) unsigned` | `0`     | 专栏ID         |
| `article_id`   | `int(10) unsigned` | `0`     | 文章ID         |
| `section`      | `int(10) unsigned` | `0`     | 章节顺序（越小越靠前） |
| `create_time`  | `timestamp`      | `CURRENT_TIMESTAMP` | 创建时间       |
| `update_time`  | `timestamp`      | `CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 最后更新时间   |

## 文章的发布流程

- 用户登录，进入发布页面
- 输入标题、文章内容
- 选择分类，封面、简介
- 提交文章，进入待审核状态，仅用户可看详情
- 管理员审核通过，所有人可看详情

## 点赞功能和点赞排行榜的实现过程

在本项目中规定每位用户只能对一篇文章点赞一次，再次点击则取消点赞。同时后续还要实现点赞排行榜的功能

具体实现应用到了Redis的zset数据结构，该数据结构具有排序的功能

- 给 **`Article`** 类中添加一个 **`isLike`** 字段，标示是否被当前用户点赞
- 利用Redis的Zset集合判断是否点赞过，未点赞过则点赞数+1，已点赞过则点赞数-1
- 通过查询Zset集合的TOP5来进行点赞排行榜的实现

```
Key: article:liked:<文章ID>
Value (ZSet): 用户ID -> Score（点赞时间）
```

### 点赞的相关逻辑

```java
@Override
    public Result likeArticle(Long id) {
        // 1.获取登录用户
        Long userId = UserHolder.getUser().getId();
        // 2.判断当前登录用户是否已经点赞
        String key = article_LIKED_KEY + id;
        Double score = stringRedisTemplate.opsForZSet().score(key, userId.toString());
        if (score == null) {
            // 3.如果未点赞，可以点赞
            // 3.1.数据库点赞数 + 1
            boolean isSuccess = update().setSql("liked = liked + 1").eq("id", id).update();
            // 3.2.保存用户到Redis的set集合  zadd key value score
            if (isSuccess) {
                stringRedisTemplate.opsForZSet().add(key, userId.toString(), System.currentTimeMillis());
            }
        } else {
            // 4.如果已点赞，取消点赞
            // 4.1.数据库点赞数 -1
            boolean isSuccess = update().setSql("liked = liked - 1").eq("id", id).update();
            // 4.2.把用户从Redis的set集合移除
            if (isSuccess) {
                stringRedisTemplate.opsForZSet().remove(key, userId.toString());
            }
        }
        return Result.ok();
    }


    private void isArticleLiked(Article article) {
        // 1.获取登录用户
        UserDTO user = UserHolder.getUser();
        if (user == null) {
            // 用户未登录，无需查询是否点赞
            return;
        }
        Long userId = user.getId();
        // 2.判断当前登录用户是否已经点赞
        String key = "article:liked:" + article.getId();
        Double score = stringRedisTemplate.opsForZSet().score(key, userId.toString());
        article.setIsLike(score != null);
    }
```



## 缓存设计

本项目在内存管理模块中将热点数据进行缓存到Redis中，以减轻数据库的压力

热点数据如下

- 展馆方发布的文章：此类文章属于热点文章，用户访问频率较高优先缓存
- 文章列表：用户的文章列表需要频繁显示但是改动频率较低
- 文章分类：文章的分类列表也是需要频繁显示但是改动频率比较低

## 缓存问题

### 缓存击穿问题

#### 问题描述

当本项目中热点数据例如展馆方发布的文章，文章分类突然因为过期失效导致大量请求会访问数据库，造成数据库压力过大

#### 解决方案

可以使用互斥锁的思路来解决这个问题。当大量用户同时访问同一篇文章时，只允许一个用户去MySQL中获取数据。当该用户从数据库中获得相关信息后重新构建缓存，再返回给用户。

本项目中采用Redis实现互斥锁

核心思路就是利用redis的setnx方法来表示获取锁

- **查询缓存**：首先检查 Redis 是否已缓存该文章，若缓存命中则直接返回。
- **空值缓存**：如果缓存中存在空值（表示该文章数据不存在），则返回 `null`。
- **加锁防止并发**：使用分布式锁保证同一时间只有一个请求去查询数据库并重建缓存。
- **缓存写入**：数据库查询成功后，将文章数据缓存到 Redis 中；如果文章不存在，缓存一个空值以避免重复查询。

```java
// 加锁和解锁
private boolean tryLock(String key) {
    Boolean flag = stringRedisTemplate.opsForValue().setIfAbsent(key, "1", 10, TimeUnit.SECONDS);
    return BooleanUtil.isTrue(flag);
}

private void unlock(String key) {
    stringRedisTemplate.delete(key);
}
```



```java
public Article queryWithMutex(Long id) {
    String key = CACHE_ARTICLE_KEY + id;
    // 从redis中查询文章缓存
    String articleJson = stringRedisTemplate.opsForValue().get(key);
    
    // 判断是否存在
    if (StrUtil.isNotBlank(articleJson)) {
        // 存在,直接返回
        return JSONUtil.toBean(articleJson, Article.class);
    }

    // 判断命中的值是否是空值
    if (articleJson != null) {
        // 返回一个错误信息
        return null;
    }

    // 实现缓存重构
    String lockKey = "lock:article:" + id;
    Article article = null;
    try {
        boolean isLock = tryLock(lockKey);
        // 判断是否获取成功
        if (!isLock) {
            // 失败，则休眠重试
            Thread.sleep(50);
            return queryWithMutex(id);
        }

        // 成功，根据id查询数据库
        article = getById(id);
        
        // 不存在，返回错误
        if (article == null) {
            // 将空值写入redis
            stringRedisTemplate.opsForValue().set(key, "", CACHE_NULL_TTL, TimeUnit.MINUTES);
            // 返回错误信息
            return null;
        }

        // 写入redis
        stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(article), CACHE_NULL_TTL, TimeUnit.MINUTES);

    } catch (Exception e) {
        throw new RuntimeException(e);
    } finally {
        // 释放互斥锁
        unlock(lockKey);
    }
    
    return article;
}

```



### 缓存穿透问题

#### 问题描述

当用户访问到已经被删除的文章（文章已经不存在于数据库和Redis中）这样缓存永远不会生效，这些请求都会打到数据库

#### 解决方案

可以使用布隆过滤器加缓存空值来解决这个问题。布隆过滤器是一种高效的数据结构，能够快速判断某个元素是否存在于一个集合中。但是具有误判率。被判定为存在的对象不一定存在但是被判定为不存在的对象一定不存在。因此可以有缓存空值的策略来解决误判的问题

具体流程如下

- **初始化布隆过滤器** ：将数据库内所有的文字ID都加入布隆过滤器中
- **查询布隆过滤器** ：当用户查询文章时先查询布隆过滤器，若被布隆过滤器判定为不存在则直接返回为空（文章一定不存在数据库中）
- **查询Redis** ：被判定为存在的文章不一定存在于数据库。先查询缓存，若缓存命中则直接返回
- **查询数据库** ：若缓存未命中则查询数据库，若数据库命中则重构缓存，反之则在redis缓存中缓存空值（这样，下次用户过来访问这个不存在的数据，那么在redis中也能找到这个数据就不会进入到数据库了）

```java
public class ArticleService {

    private static final String CACHE_ARTICLE_KEY = "article:";
    private static final long CACHE_NULL_TTL = 10;  // 缓存空值的有效时间，单位：分钟
    private static final long CACHE_TTL = 60;  // 缓存文章的有效时间，单位：分钟

    private StringRedisTemplate stringRedisTemplate;
    private BloomFilterService bloomFilterService;

    public ArticleService(StringRedisTemplate stringRedisTemplate, BloomFilterService bloomFilterService) {
        this.stringRedisTemplate = stringRedisTemplate;
        this.bloomFilterService = bloomFilterService;
    }

    // 从布隆过滤器获取文章ID的有效性
    private BitMapBloomFilter getBloomFilter() {
        return bloomFilterService.createBloomFilter();
    }

    public Article queryWithBloomFilter(Long id) {
        String key = CACHE_ARTICLE_KEY + id;

        // 查询布隆过滤器判断文章ID是否存在
        BitMapBloomFilter bloomFilter = getBloomFilter();
        
        // 如果布隆过滤器判断文章ID不存在，直接返回null
        if (!bloomFilter.contains(id.toString())) {
            return null;
        }

        // 查询缓存
        String articleJson = stringRedisTemplate.opsForValue().get(key);
        
        // 如果缓存命中，直接返回文章数据
        if (StrUtil.isNotBlank(articleJson)) {
            return JSONUtil.toBean(articleJson, Article.class);
        }

        // 如果缓存中没有，继续查询数据库
        Article article = articleMapper.getById(id);
        
        // 如果数据库中没有该文章，缓存空值
        if (article == null) {
            stringRedisTemplate.opsForValue().set(key, "", CACHE_NULL_TTL, TimeUnit.MINUTES);
            return null;
        }

        // 如果数据库中存在，将文章缓存
        stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(article), CACHE_TTL, TimeUnit.MINUTES);
        return article;
    }
  
```



### 缓存一致性问题

#### 问题描述

使用 Redis 作为缓存系统时，数据在缓存（Redis）和数据库（MySQL）之间可能会出现不同步或不一致的情况。这种不一致性会导致系统在读取数据时获取到过时的数据，或者在更新数据时没有及时更新缓存，从而影响系统的准确性和稳定性。

#### 解决方案

本项目采用以下策略

- 写操作：先更新数据库，再删除缓存，后续等查询把数据库的数据回种到缓存中
- 读操作：先查询缓存，若缓存不命中则查询数据库，然后将数据回种到缓存中

#### 采用理由

本项目对一致性要求不高，可以容忍短时间的不一致性

## Kafka实现异步处理

### 异步处理的必要性

在本项目中使用Kafka消息队列，能够使我们项目异步加速（只负责投递）。同时避免传统的同步处理带来的高延迟和同步调用链条过长的问题。

### 具体实现方案

#### Kafka生产者

由于本项目的内容模块的消息类型只有以下几种

- **点赞**
- **取消点赞**
- **评论**
- **取消评论**

因此可以通过AOP来整合消息实现环绕通知，将消息投入Kafka队列中

#### Kafka消费者

kafka消费者则监听队列中指定主题的消息，进行业务逻辑的消费。

### 遇到的问题

众所周知，Kafka作为消息队列具有消息重复消费的问题。而解决该问题的方法就是实现消费的幂等性。消费的幂等性是指 **无论一条消息被消费多少次，最终的业务结果都应该与消费一次时的结果相同。** 而消费的幂等性通常可以通过 **去重** 来实现。策略如下

- 每次消费时，先检查 Redis **是否已处理** 该 ID。
- 如果已存在，则跳过处理，避免数据重复写入。

本项目使用先前的雪花算法生成全局唯一的消息ID

