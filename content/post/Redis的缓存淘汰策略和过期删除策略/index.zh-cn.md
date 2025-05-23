---
date : '2025-03-01T17:51:38+08:00'
draft : false
title : 'Redis的缓存淘汰策略和过期删除策略'
image : ""
categories : ["Redis"]
tags : ["数据库"]
description : "Redis的缓存淘汰策略和过期删除策略"
math : true
---

## 过期删除策略

Redis 数据过期主要有两种删除策略，分别为 **定期删除、惰性删除** 两种：

- **定期删除**：Redis 每隔一定时间（默认是 100 毫秒）会随机检查一定数量的键，如果发现过期键，则将其删除。这种方式能够在后台持续清理过期数据，防止内存膨胀。
- **惰性删除**：在每次访问键时，Redis 检查该键是否已过期，如果已过期，则将其删除。这种策略保证了在使用过程中只删除不再需要的数据，但在不访问过期键时不会立即清除。
- **定时删除** ：在设置 key 的过期时间时，同时创建一个定时事件，当时间到达时，由事件处理器自动执行 key 的删除操作。

### Key过期的判定

每当对一个 key 设置了过期时间时，Redis 会把该 key 带上过期时间存储到一个 **过期字典** 中，也就是说 **过期字典** 保存了数据库中所有 key 的过期时间。

字典实际上是哈希表。当我们查询一个 key 时，Redis 首先检查该 key 是否存在于过期字典中：

- 如果不在，则正常读取键值；
- 如果存在，则会获取该 key 的过期时间，然后与当前系统时间进行比对，如果比系统时间大，那就没有过期，否则判定该 key 已过期。

### 定期删除策略

定期删除策略的做法：**每隔一段时间随机从数据库中取出一定数量的 key 进行检查，并删除其中的过期key。**

#### 优缺点

**优点**：

- 通过限制删除操作执行的时长和频率，来减少删除操作对 CPU 的影响，同时也能删除一部分过期的数据减少了过期键对空间的无效占用。

**缺点**：

- 内存清理方面没有定时删除效果好，同时没有惰性删除使用的系统资源少。
- 难以确定删除操作执行的时长和频率。如果执行的太频繁，定期删除策略对CPU不友好；如果执行的太少，那又和惰性删除一样了，过期 key 占用的内存不会及时得到释放。

#### 执行过程

- 从过期字典中随机抽取 20 个 key；
- 检查这 20 个 key 是否过期，并删除已过期的 key；
- 如果本轮检查的已过期 key 的数量，超过 5 个（20/4），也就是 **已过期 key 的数量**占比 **随机抽取 key 的数量** 大于 25%，则继续重复步骤 1；如果已过期的 key 比例小于 25%，则停止继续删除过期 key，然后等待下一轮再检查。

### 惰性删除策略

惰性删除策略的做法是：**不主动删除过期键，每次从数据库访问 key 时，都检测 key 是否过期，如果过期则删除该 key。**

#### 优缺点

**优点**：

- **CPU友好**：因为每次访问时，才会检查 key 是否过期，所以此策略只会使用很少的系统资源，因此，惰性删除策略对 CPU 时间最友好。

**缺点**：

- **内存不友好**：如果一个 key 已经过期，而这个 key 又仍然保留在数据库中，那么只要这个过期 key 一直没有被访问，它所占用的内存就不会释放，造成了一定的内存空间浪费。所以，惰性删除策略对内存不友好。

#### 执行过程

- Redis 在访问或者修改 key 之前，都会调用 expireIfNeeded 函数对其进行检查，检查 key 是否过期：
  - 如果过期，则删除该 key，至于选择异步删除，还是选择同步删除，根据 `lazyfree_lazy_expire` 参数配置决定（Redis 4.0版本开始提供参数），然后返回 null 客户端；
  - 如果没有过期，不做任何处理，然后返回正常的键值对给客户端；

## 内存淘汰策略

内存淘汰策略是在内存满了的时候，redis 会触发内存淘汰策略，来淘汰一些不必要的内存资源，以腾出空间，来保存新的内容

Redis 的内存淘汰策略一共有 8 种。 分为以下几类

- **开启数据淘汰**
  - **基于过期时间的淘汰策略**
    - **volatile-random**：随机淘汰设置了过期时间的任意键值；
    - **volatile-ttl**：优先淘汰更早过期的键值。
    - **volatile-lru** ：淘汰所有设置了过期时间的键值中，最久未使用的键值；
    - **volatile-lfu** ：淘汰所有设置了过期时间的键值中，最少使用的键值；
  - **全部数据的淘汰策略**
    - **allkeys-random**：随机淘汰任意键值;
    - **allkeys-lru**：淘汰整个键值中最久未使用的键值；
    - **allkeys-lfu** ：淘汰整个键值中最少使用的键值。
- **不开启数据淘汰** 
  - **noeviction** ：当运行内存超过最大设置内存的时候，不会淘汰数据，而是直接返回报错禁止写入