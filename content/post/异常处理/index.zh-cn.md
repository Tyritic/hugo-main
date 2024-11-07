---
date : '2024-11-07T16:33:35+08:00'
draft : false
title : '异常处理'
image : ""
categories : ["项目技术"]
tags : ["后端开发"]
description : "项目中对于异常的处理办法"
---

项目开发过程中会遇到异常问题

## 全局异常处理器

![](微信截图_20241107164515.png)

**@RestControllerAdvice**：用于修饰类表示全局异常处理器

**@ExceptionHandler**：用于修饰异常处理方法

示例代码

```java
@RestControllerAdvice
puhlic class GlobalExceptionHandler {
	@ExceptionHandler(Exception.class)
    public Result ex(Exception ex){ex.printstackTrace();
		return Result.error(”对不起,操作失败,请联系管理员");
}
```

## 全局异常

在common包下定义基本异常BaseException，其余的异常为这个类的子类

示例代码

```java
public class BaseException extends RuntimeException {

    public BaseException() {
    }

    public BaseException(String msg) {
        super(msg);
    }

}
```

