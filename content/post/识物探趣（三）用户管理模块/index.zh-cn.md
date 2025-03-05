---
date : '2025-01-07T13:28:40+08:00'
draft : false
title : '识物探趣（三）用户管理模块'
image : ""
categories : ["个人项目"]
tags : [""]
description : "软著文档的留档和开发过程的收获"
math : true
---

## 项目文件结构

后端工程基于 maven 进行项目构建，并且进行分模块开发。

```
-- cloud_urban
|---cloud-common
| |---constant 常量类
| |---context 应用上下文进程
| |---result 后端统一返回结果
| |---utils 工具类
| |---exception 自定义业务相关异常
| |---properties 参数模板类
|---cloud-pojo
| |---dto 数据库传输对象
| |---vo 视图对象
| |---entity 业务实体对象
|---cloud-server
| |---controller 控制器类
| |---service 业务接口和业务类
| |---mapper 数据持久层
| |---config bean配置类
| |---handler 异常处理
| |---interceptor 拦截器
```

| **序号** |   **名称**   |                          **说明**                           |
| :------: | :----------: | :---------------------------------------------------------: |
|    1     | cloud_urban  |        maven父工程，统一管理依赖版本，聚合其他子模块        |
|    2     | cloud-common |     子模块，存放公共类，例如：工具类、常量类、异常类等      |
|    3     |  cloud-pojo  |                子模块，存放Entity、VO、DTO等                |
|    4     | cloud-server | 子模块，存放业务逻辑的相关类、Controller、Service、Mapper等 |

## 管理端

### 表结构设计

#### admin管理人员表

| **字段名**  | **数据类型** |   **说明**   |  **备注**   |
| :---------: | :----------: | :----------: | :---------: |
|     id      |    bigint    |     主键     |    自增     |
|    name     | varchar(32)  |     姓名     |             |
|  username   | varchar(32)  |    用户名    |    唯一     |
|  password   | varchar(64)  |     密码     |             |
|    phone    | varchar(11)  |    手机号    |             |
|     sex     |  varchar(2)  |     性别     |             |
|  id_number  | varchar(18)  |   身份证号   |             |
|   status    |     Int      |   账号状态   | 1正常 0锁定 |
| create_time |   Datetime   |   创建时间   |             |
| update_time |   datetime   | 最后修改时间 |             |
| create_user |    bigint    |   创建人id   |             |
| update_user |    bigint    | 最后修改人id |             |

### 登录流程设计

相对于 **`Cookie`** 和 **`Session`** 不适用于分布式集群，本项目选择 JWT 令牌方案作为登录的鉴权机制。

具体鉴权机制的方案对比参考[往期博客](https://tyritic.github.io/p/%E7%99%BB%E5%BD%95%E9%89%B4%E6%9D%83%E6%9C%BA%E5%88%B6/)

#### JWT无法主动失效的安全问题

但是JWT 令牌的无状态特性导致服务端不会主动跟踪JWT令牌的状态，无法让令牌提前失效。在某些场景中会导致潜在的安全问题，比如当用户登出之后，使用相同的JWT令牌依然成功访问服务。

**解决方案**

通过引入redis缓存中间件来形成黑名单机制，将已经失效的JWT令牌放入redis缓存中并根据该令牌的过期时间为Redis键值对设置过期时间，当已经登出的用户带着被纳入黑名单的令牌访问服务时将被拒绝提供服务

**具体实现**

黑名单基于jwt标识来实现对令牌的处理

JWT 令牌通常包含一个 `jti`（JWT ID），它是一个唯一标识，可以用来跟踪和管理 JWT。
具体实现

- **JWT 生成时，包含唯一的 `jti` 字段。**
- **当用户登出或 Token 需要失效时，将 `jti` 存入 Redis 黑名单。**
- **每次请求时，解析 Token，检查其 `jti` 是否在黑名单中，如果存在，则拒绝访问。**

## 用户端



