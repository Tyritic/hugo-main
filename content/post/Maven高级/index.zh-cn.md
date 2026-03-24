
---
date : '2024-11-09T12:27:38+08:00'
draft : false
title : 'Maven高级'
image : ""
categories : ["Spring系列"]
tags : ["后端开发"]
description : "Maven的高级应用"
---

## 🏗️ 分模块设计与开发

&lt;div align="center"&gt;
  &lt;img src="微信截图_20241109164003.png" alt="分模块设计" width="82%"&gt;
&lt;/div&gt;

将项目的不同业务功能划分为不同的Maven模块

优点

- 方便项目的维护拓展
- 方便模块的相互调用

---

## 👨‍👩‍👧‍👦 继承

概念：继承描述的是两个工程间的关系，与java中的继承相似，子工程可以继承父工程中的配置信息，常见于依赖关系的继承。

作用：简化依赖配置、统一管理依赖（所有子工程共有的依赖配置在父工程中）

所有的SpringBoot项目都继承一个统一的父工程spring-boot-starter-parent

---

### 🔧 具体实现：

1. 创建maven模块，该工程为父工程，设置打包方式pom(默认jar)

   ```xml
   &lt;parent&gt;
   	&lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
   	&lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
   	&lt;version&gt;2.7.5&lt;/version&gt;
   	&lt;relativePath/&gt;
   &lt;/parent&gt;
   
   &lt;groupId&gt;com.itheima&lt;/groupId&gt;
   &lt;artifactId&gt;tlias-parent&lt;/artifactId&gt;
   &lt;version&gt;1.8-SNAPSHOT&lt;/version&gt;
   &lt;packaging&gt;pom&lt;/packaging&gt;
   ```

2. 在子工程的pom.xml文件中，配置继承关系。

   ```xml
   &lt;parent
   	&lt;groupId&gt;com.itheima&lt;/groupId&gt;
   	&lt;artifactId&gt;tlias-parent&lt;/artifactId&gt;
   	&lt;version&gt;1.0-SNAPSHOT&lt;/version&gt;
   	&lt;relativePath&gt;../ tlias-parent/pom,xml&lt;/relativePath&gt;
   &lt;/parent&gt;
   ```

   {{&lt;notice tip&gt;}}

   - 在子工程中，配置了继承关系之后，坐标中的groupId是可以省略的，因为会自动继承父工程的
   - relativePath指定父工程的pom文件的相对位置(如果不指定，将从本地仓库/远程仓库查找该工程)。

   {{&lt;/notice&gt;}}

3. 在父工程中配置各个工程共有的依赖(子工程会自动继承父工程的依赖)。
    {{&lt;notice tip&gt;}}
    若子工程和父工程的依赖版本不同，以子工程的为准
    {{&lt;/notice&gt;}}

---

### 📦 打包方式

- pom：父工程，该模块无代码只进行依赖管理
- jar：内嵌Tomcat服务器
- war：普通web程序，部署在在外部Tomcat服务器

---

### 🔒 版本锁定

在maven中，可以在父工程的pom文件中通过`&lt;dependencyManagement &gt;`来统一管理依赖版本。

在父工程的pom文件中指定依赖版本后，子工程引入依赖时不需要指定依赖版本，变更依赖版本时在父工程的pom文件中统一更改

示例

```xml
#父工程
&lt;dependencyManagement&gt;
    &lt;dependencies&gt;
        &lt;!--JWT令牌--&gt;
		&lt;dependency&gt;
            &lt;groupId&gt;io.jsonwebtoken&lt;/groupId&gt;
            &lt;artifactId&gt;jjwt&lt;/artifactId&gt;
            &lt;version&gt;0.9.1&lt;/version&gt;
		&lt;/dependency&gt;
    &lt;/dependencies&gt;
&lt;/dependencyManagement&gt;
```

```xml
#子工程
&lt;dependencies&gt;
	&lt;dependency&gt;
		&lt;groupId&gt;io.jsonwebtoken&lt;/groupId&gt;
		&lt;artifactId&gt;jjwt&lt;/artifactId&gt;
	&lt;/dependency&gt;
&lt;/dependencies&gt;
```

{{&lt;notice tip&gt;}}

&lt; dependencies &gt;和&lt; dependencyManage &gt;的区别

- &lt; dependencies &gt;是直接依赖，子工程的pom无须引入
- &lt; dependencyManage &gt;是版本管理，子工程的pom依然需要引入

{{&lt;/notice&gt;}}

---

### ⚙️ 自定义属性/引用属性

可以在pom文件中使用标签`&lt;properties&gt;`标签来自定义属性

```xml
&lt;properties&gt;
	&lt;lombok.versiqn&gt;1.18.24&lt;/lombok.version&gt;
	&lt;jjwt.version&gt;8.9.0&lt;/jjwt.version&gt;
&lt;/properties&gt;
```

然后使用${}来引用自定义属性

```xml
&lt;dependencies&gt;
	&lt;dependency&gt;
		&lt;groupId&gt;org.projectlombok&lt;/groupId&gt;
		&lt;artifactId&gt;lombok&lt;/artifactId&gt;
		&lt;version&gt;${lombok.version}&lt;/version&gt;
	&lt;/dependency&gt;
&lt;/dependencies&gt;
```

---

## 🔗 聚合

概述：将多个模块组织成一个整体，同时进行项目的构建。

聚合工程：一个不具有业务功能的"空"工程(有且仅有一个pom文件)通常是继承中的父工程

具体实现：在父工程中使用标签`&lt;module&gt;`指定子模块

```xml
&lt;modules&gt;
	&lt;module&gt;../tlias-pojo&lt;/module&gt;
	&lt;module&gt;,./tlias-utils&lt;/module&gt;
	&lt;module&gt;../tlias-web-management&lt;/module&gt;
&lt;/modules&gt;
```

{{&lt;notice tip&gt;}}

聚合工程中所包含的模块，在构建时，会自动根据模块间的依赖关系设置构建顺序，与聚合工程中模块的配置书写位置无关。

{{&lt;/notice&gt;}}

---

## 🤝 继承和聚合的区别

作用

- 聚合用于快速构建项目
- 继承用于简化依赖配置、统一管理依赖

相同点

- 聚合与继承的pom.xml文件打包方式均为pom，可以将两种关系制作到同一个pom文件中
- 聚合与继承均属于设计型模块，并无实际的模块内容

不同点

- 聚合是在聚合工程中配置关系，聚合可以感知到参与聚合的模块有哪些
- 继承是在子模块中配置关系，父模块无法感知哪些子模块继承了自己

