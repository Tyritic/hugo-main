---
date : '2024-11-17T15:48:33+08:00'
draft : false
title : 'Java的文件操作'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## File类

File类是文件的抽象表示，用于文件与目录的创建，查找，删除，只能对文件本身操作，不能对文件内容操作

## 构造方法

- `public File(String pathname)`  // 根据路径创建文件对象 
- `public File(String parent, String child)`  // 根据父路径和子路径创建文件对象 
- `public File(File parent, String child)`  // 根据父目录 File 对象和子路径创建文件对象

**注意事项**

- `File`对象代表硬盘中实际存在的文件和目录
- `File`类的构造方法不检查是否存在该路径

## 常见操作

### 判断文件/目录

- `public boolean isFile()`：判断是否是文件
- `public boolean isDirectory()`：判断是否为目录

### 获取文件/目录的基本信息

- `public String getName()`：获取文件名
- `public String getAbsolutePath()`：获取绝对路径
- `public String getParent()`：获取父目录
- `public long length()`：获取文件大小（以B为单位）
- `public long lastModified()`：获取最后修改时间
- 检查读/写/可执行权限
  - `public boolean canRead()`
  - `public boolean canWrite()`
  - `public boolean canExecute()`

### 创建文件/目录

- `public boolean createNewFile() throws IOException`：创建文件
  - 原先文件不存在则创建成功返回`true`
  - 原先文件存在则创建失败返回`false`
- 创建目录
  - `public boolean mkdir()`：创建单级目录，父目录不存在则创建失败
  - `public boolean mkdirs()`：创建多级目录，父目录不存在则一并创建

### 删除文件目录

- `public boolean delete()`

### 列举目录文件

- `public String[] list()`：列出目录中的文件名
- `public File[] listFiles()`：列出目录中的`File`对象