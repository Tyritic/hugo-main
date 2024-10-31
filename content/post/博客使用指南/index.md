+++
date = '2024-10-31T21:07:07+08:00'
draft = false
title = '博客使用指南'
image ="OpenGraph.jpg"
categories = ["博客相关"]
tags =[""]
description="博客的使用指南"
+++

# 博客使用教程

## 文章存储位置

本博客的所有文章都存放在E/MyBlog/content/post文件夹中![image-20241031190526917](image-20241031190526917.png)

## 如何添加文章

### 命令行操作

在MyBlog主文件夹的cmd中运行以下命令

```
hugo new content <SECTIONNAME>\<FileName>/<FORMAT>
```

#### 参数解释

<SECTIONNAME>为当前文章保存的文件路径

<FileName>为当前文章所在的文件夹名

<FORMAT> 为当前文章的语言格式

​	中文：index.zh-cn.md

​	英文：index.md

![微信截图_20241031192624](微信截图_20241031192624.png)

## 文章内修改

###  插入照片

将需要的图片放入文章的文件夹中即可

### 头文字参数

- data：创建时间

- draft：是否草稿

- title：文章标题

- image：博客网站的开头图片

- categories：文章的分类

- tags：文章的标签

- description：文章的描述

  
