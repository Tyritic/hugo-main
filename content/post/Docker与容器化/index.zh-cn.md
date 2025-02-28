---
date : '2025-02-25T20:36:53+08:00'
draft : false
title : 'Docker与容器化'
image : ""
categories : ["云原生"]
tags : ["后端开发"]
description : "云原生的载体-容器化"
math : true
---

## Docker的定义

Docker 本质上就是一个将 **程序和环境打包并运行** 的工具软件。具体点来说就是，它通过 Dockerfile 描述环境和应用程序的依赖关系， docker build 构建镜像， docker pull/push 跟 Docker Registry 交互实现存储和分发镜像，docker run 命令基于镜像启动容器，基于容器技术运行程序和它对应的环境，从而解决环境依赖导致的各种问题。

{{<notice tip>}}

程序和环境

- 程序是在操作系统上运行的
- 环境是操作系统上装了各种不同版本的依赖库和配置，这些被程序所依赖的信息

{{</notice>}}

## Docker的基本概念

### 镜像

#### 基础镜像

Docker 容器的基础镜像（Base Image）是创建新容器时使用的起始点。基础镜像是一个层叠的文件系统，包含了一系列操作系统的基础层，这些层可以包含操作系统、运行时环境、工具和库等。

- 选中一个基础操作系统和语言后，将对应的文件系统
- 依赖库
- 配置

将以上部分放一起打包成一个类似压缩包的文件，这就是所谓的 **基础镜像** (Base Image)。

#### 容器镜像

当我们用命令行执行 **docker build** 的时候，Docker 软件就会按着 Dockerfile 的说明，一行行构建环境+应用程序。最终将这个环境+程序，打包成一个类似"压缩包"的东西，就是 **容器镜像** (container image)。只要将容器镜像传到任意一台服务器上，对这个"压缩包"执行"解压缩"，就能同时运行环境和程序。总而言之，Docker 镜像是 Docker 容器的源代码，是镜像是一个只读的模板。，Docker 镜像用于创建容器。使用build 命令创建镜像。

### Dockerfile

Dockerfile相当于一个 **todo list** 。有了基础镜像之后还需要安装一些依赖，比如 `yum install gcc`，甚至还要创建一些文件夹。最后才是运行我们的目标 **应用程序**。创建自定义镜像的文件。通过编写 Dockerfile，你可以定义镜像中应该包含哪些内容以及如何配置。

### 容器

在目的服务器上，执行 **`docker pull`** 拿到容器镜像。然后执行 **`docker run`** 命令，将这个类似"压缩包"的容器镜像给"解压缩"，获得一个 **独立的环境和应用程序** 并运行起来。这样一个独立的环境和应用程序，就是所谓的 **容器** (container)。我们可以在一个操作系统上同时跑多个容器。且这些容器之间都是互相独立，互相隔离的。

总而言之，Docker 容器包括应用程序及其所有依赖项，作为操作系统的独立进程运行。容器是动态的、可变的，可以启动、停止、移动和删除。在运行时，它拥有独立的文件系统、网络和进程空间，但与物理主机共享操作系统内核。

### 镜像仓库

Docker 可以组建 **镜像仓库** ，通过 **docker push** 将镜像推到仓库，有需要的时候再通过 **docker pull** 将镜像拉到机器上。这个负责管理镜像仓库推拉能力的服务，就叫 **Docker Registry**。

## Docker的构建过程

- 编写 Dockerfile：Dockerfile 是一个文本文件，其中包含了一系列的指令，描述了如何构建一个 Docker 镜像。 
- 构建镜像：使用 `docker build` 命令，通过读取 Dockerfile 的内容，逐步执行其中的指令，最终生成一个 Docker 镜像。 
- 保存镜像：构建完成的镜像会被保存到本地的 Docker 镜像库中，可以使用 `docker images` 命令查看。 
- 发布镜像：如果需要共享镜像，可以将其推送到 Docker Hub 或其他镜像仓库，使用 `docker push` 命令完成发布。 
- 使用镜像：最终用户可以使用 `docker run` 命令来启动基于该镜像的容器，完成应用的部署和运行。

## Docker的数据管理

在容器中管理数据主要有两种方式：

- 数据卷（Volumes）
- 挂载主机目录 (Bind mounts)

### 数据卷挂载

数据卷是一个虚拟目录，将宿主机的目录映射到容器内目录。具有以下特点

- 可以在容器之间共享和重用。
- 即使容器被删除，数据卷中的数据也不会被自动删除，从而确保数据的持久性。
- 对数据卷的修改会立马生效。
- 对数据卷的更新，不会影响镜像。

挂载数据卷命令

```shell
docker run -v 数据卷名:目录名 镜像名称
docker run -itd
-- name 容器名字
-- mount source=数据卷名,target=容器中目录
镜像名
```

常见命令

```shell
# 创建一个数据卷
docker volume create my-vol
# 查看所有的数据卷
docker volume ls
# 查看数据卷的具体信息
docker inspect web
# 删除指定的数据卷
docker volume rm my-vol
```



### 目录挂载

目录挂载是直接将宿主机上的目录挂载到容器中，直接使用宿主机的文件系统

挂载目录命令

```shell
docker run -v 宿主机目录:容器内目录 镜像名称
docker run -itd 
-- name 容器名
-- mount type=bind,source=宿主机目录,target=容器中的目录
镜像名
```



## Docker的底层原理

Docker是经典的 Client/Server 架构。Client 对应 Docker-cli， Server 对应 Docker daemon。

### 架构原理

Docker-cli 会解析我们输入的 cmd 命令，然后调用 Docker daemon 守护进程提供的 RESTful API，守护进程收到命令后，会根据指令创建和管理各个容器。

Docker Daemon 内部分为 Docker Server、Engine 两层。

- Docker Server 本质上就是个 HTTP 服务，负责对外提供操作容器和镜像的 api 接口，接收到 API 请求后，会分发任务给 Engine 层
- Engine 层负责创建 Job，由 Job 实际执行各种工作。这是 Docker 的核心，它是一个轻量级的运行时和工具集，用于管理容器。Docker引擎包括服务器端的守护进程（daemon）、API，以及CLI工具。

### 容器化技术

**Namespace 和 Cgroups**：这两个是 Docker 能够实现隔离的核心 Linux 技术。

- Namespace 提供了进程、网络、挂载等资源的隔离，
- Cgroups 则负责限制和优先级分配，限制它能使用的计算资源，确保容器不会耗尽主机资源。

每个容器运行在它自己的命名空间中，但是，确实与其它运行中的容器共用相同的系统内核。隔离的产生是由于系统内核清楚地知道命名空间及其中的进程，且这些进程调用系统 API 时，内核保证进程只能访问属于其命名空间中的资源。

{{<notice tip>}}

Docker和虚拟机的关系

- 传统虚拟机自带一个完整操作系统，虚拟出一套硬件后，在其上运行一个完整操作系统，在该系统上再运行所需应用进程
- 容器本身不带完整操作系统，容器的基础镜像实际上只包含了操作系统的核心依赖库和配置文件等必要组件。容器本质上只是个自带独立运行环境的 **特殊进程** ，底层用的其实是 **宿主机的操作系统内核** 。

{{</notice>}}

## VPS和ECS

云厂商一般会 **将一台物理服务器分割成多个虚拟机** 。每个虚拟机都拥有独立的操作系统、资源（比如 CPU、内存、存储空间）和公网 IP 地址。然后对外出售，这样的虚拟机就是所谓的 **VPS**（Virtual Private Server，虚拟专用服务器）。

但传统 VPS 有个缺点，不支持用户**自主升降级**，它的资源是预先分配的，不易动态调整。

而支持VPS自主升降级的功能就成了 **ECS**（Elastic Compute Service，弹性计算服务）。用户可以根据需要随时调整 CPU、内存、磁盘和带宽，主打一个"**弹性**"。

而通常 **物理服务器上跑 ecs，ecs 跑 Docker 容器。多个 Docker 容器共享一个 ecs 实例 操作系统内核** 。

## 容器服务编排——Docker Compose

使用场景：一次部署在同一个物理服务器 **多个** 容器组成的一套服务，且对这些容器的顺序有一定要求呢

**Docker Compose** 是用于定义和运行多容器 Docker 应用程序的工具。Compose 使用 YAML 文件定义服务、网络和卷，通过一条简单的命令 `docker-compose up` 就可以启动并运行整个配置的应用环境。

**示例**

```yaml
version: "3.8"

services:
  A:
    image: "some-image-for-a"
    deploy:
      resources:
        limits:
          cpus: "0.50" # 限制 CPU 使用率为 50%
          memory: 256M # 限制内存使用量为 256MB

  B:
    image: "some-image-for-b"
    depends_on:
      - A

  C:
    image: "some-image-for-c"
    depends_on:
      - B

```

### 常见命令

#### 启动命令

```shell
# 在当前目录下寻找 docker-compose.yml 文件，并根据其中定义的服务启动应用程序
docker-compose up
# 后台启动
docker-compose up -d
# 强制重新创建所有容器，即使它们已经存在
docker-compose up --force-recreate
# 重新构建镜像
docker-compose up --build
# 指定要启动的服务名称，而不是启动所有服务
# 可以同时指定多个服务，用空格分隔。
docker-compose up service_name
```

#### 暂停和停止命令

```shell
# 在当前目录下寻找 docker-compose.yml 文件
# 根据其中定义移除启动的所有容器，网络和卷。
docker-compose down
# 停止容器但不移除
docker-compose down --stop
# 指定要停止和移除的特定服务，而不是停止和移除所有服务
# 可以同时指定多个服务，用空格分隔。
docker-compose down service_name
```

#### 查看命令

```shell
# 查看所有容器的状态信息
docker-compose ps
# 只显示服务名称
docker-compose ps --services
# 查看指定服务的容器
docker-compose ps service_name
```



## Docker 常见命令

### 基本命令

```shell
docker version # 查看docker版本
docker images # 查看所有已下载镜像，等价于：docker image ls 命令
docker container ls # 查看所有容器
docker ps #查看正在运行的容器
docker image prune # 清理临时的、没有被使用的镜像文件。-a, --all: 删除所有没有用的镜像，而不仅仅是临时文件；
```

### 拉取镜像

```shell
docker search mysql # 查看mysql相关镜像
docker pull mysql:5.7 # 拉取mysql镜像
docker image ls # 查看所有已下载镜像
```

### 构建镜像

```shell
# imageName 是镜像名称，1.0.0 是镜像的版本号或标签
docker build -t imageName:1.0.0 .
```

### 删除镜像

- 先将运行该镜像的容器暂停：**`docker stop CONTAINER ID`**
- 然后删除镜像：**`docker rmi IMAGE ID`**   或者 **`docker rmi REPOSITORY`** 

### 推送镜像

```shell
docker push url/image_name:version
```

### 启动容器

```shell
docker run [Option] image_name
-- name 容器名
-d 后台运行
-it 直接进入容器
-p 主机端口:容器端口
```

