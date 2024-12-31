---
date : '2024-12-30T15:29:22+08:00'
draft : false
title : '双指针法-滑动窗口法'
image : ""
categories : [""]
tags : [""]
description : ""
math : true
---

## 题目描述

通常用于在数组，链表中求解窗口的最值问题

## 算法模板

### 最小滑动窗口

#### 题目前提

给定数组 nums，定义滑窗的左右边界 i, j，求满足某个条件的滑窗的最小长度。

#### 思路解析

- 先固定左指针不动
- 一开始滑窗不满足条件，向右移动右指针直到窗口满足题目条件
- 迭代左移左指针同时更新结果

#### 代码模板

```java
class solution{
    public result<T> search(int[]nums)
    {
        int left=0;
        for(int right=0;right<nums.length;right++)
        {
            // 判断[i, j]是否满足条件
    		while 满足条件
            {
                // 不断更新结果(注意在while内更新！)
                left++; //最大程度的压缩左边界，使得滑窗尽可能的小
            }
        }
        return result;
    }
}

```

### 最大滑动窗口

#### 题目前提

给定数组 nums，定义滑窗的左右边界 i, j，求满足某个条件的滑窗的最大长度。

#### 思路解析

- 先固定左指针不动
- 一开始滑窗满足条件，向右移动右指针直到