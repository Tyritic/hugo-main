+++
date = '2024-11-01T13:28:03+08:00'
draft = false
title = 'Test'
image =""
categories= [""]
tags= [""]
description=""
lastmod= '2024-11-01T13:28:03+08:00'
+++

# 博客使用教程

## 文章存储位置

本博客的所有文章都存放在E/MyBlog/content/post文件夹中![image-20241031190526917](image-20241031190526917.png)

## 如何添加文章

### 命令行操作

在MyBlog主文件夹的cmd中运行以下命令

```
hugo new content post\<FileName>/index.md
```

#### 参数解释

**post**：所有文章保存的文件路径

**FileName**为当前文章所在的文件夹名

**index.md**为当前文章的markdown文件

## 文章内修改

###  插入照片

将需要的图片放入文章的文件夹中即可

### 头文字参数

- **data**：创建时间

- **draft**：是否草稿

- **title**：文章标题

- **image**：博客网站的开头图片

- **categories**：文章的分类

- **tags**：文章的标签

- **description**：文章的描述

## 创建分组（categories）

在 `content/categories/分类名` 下新建文件 `_index.md`

可以使用命令行工具

```
hugo new content categories/<分组名>/_index.md
```

### 参数解释

- **categories**：所有分组的所在目录
- **_index.md**：分组的配置文件

## 创建标签（Tags)

在 `content/tags/分类名` 下新建文件 `_index.md`

可以使用命令行工具

```
hugo new content tags/<标签名>/_index.md
```

### 参数解释

- **tags**：所有标签所在的目录
- **_index.md**：分组的配置文件
