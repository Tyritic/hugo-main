---
date : '2025-01-14T10:19:12+08:00'
draft : false
title : 'BigDecimal保证精度不丢失的机制'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "BigDecimal如何保证精度不丢失"
math : true
---

## 回答重点

BigDecimal 能够保证精度，是因为它使用了任意精度的整数表示法，而不是浮动的二进制表示。

BigDecimal 内部使用两个字段存储数字，一个是整数部分 intVal，另一个是用来表示小数点的位置 scale，避免了浮点数转化过程中可能的精度丢失。

计算时通过整数计算，再结合小数点位置和设置的精度与舍入行为，控制结果精度，避免了由默认浮点数舍入导致的误差。

```java
public class BigDecimal extends Number implements Comparable<BigDecimal> {
    private final BigInteger intVal;  // 存储整数部分
    private final int scale;          // 存储小数点的位置

    public BigDecimal(String val) {
        // 使用 BigInteger 来表示数值
        intVal = new BigInteger(val.replace(".", ""));
        scale = val.contains(".") ? val.length() - val.indexOf(".") - 1 : 0;
    }
}
```

