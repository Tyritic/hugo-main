---
date : '2024-12-30T11:44:58+08:00'
draft : false
title : '双指针法 左右指针法'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "算法题中左右指针的应用"
math : true
---

## 题目描述

通常当使用蛮力法需要两个for循环时，将两个for循环削减成一个for循环的优化方法。时间复杂度$O(n^2)$可以优化为$O(n)$

同时数组排序为两端大，中间小

## 算法模板

### 方法步骤

双指针法（左右指针法）： **通过一个左指针和右指针在一个for循环下完成两个for循环的工作。**

定义左右指针

- 左指针：定义在数组左侧的指针
- 右指针：定义在数组尾部的指针

### 代码模板

```
class solution{
    public int solution(int[]nums,int val)
    {
        int leftIndex=0;
        int rightIndex=nums.length-1;
        while(left<=right)
        {
        	
        }
    }
}
```

## 经典例题

### leetcode 977. 有序数组的平方

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/squares-of-a-sorted-array/)

给你一个按 非递减顺序 排序的整数数组 nums，返回 每个数字的平方 组成的新数组，要求也按 非递减顺序 排序。

示例 1：

- 输入：nums = [-4,-1,0,3,10]
- 输出：[0,1,9,16,100]
- 解释：平方后，数组变为 [16,1,0,9,100]，排序后，数组变为 [0,1,9,16,100]

示例 2：

- 输入：nums = [-7,-3,2,3,11]
- 输出：[4,9,9,49,121]

#### 思路解析

数组其实是有序的， 只不过负数平方之后可能成为最大数了。

那么数组平方的最大值就在数组的两端，不是最左边就是最右边，不可能是中间。

此时可以考虑双指针法了，i指向起始位置，j指向终止位置。

定义一个新数组result，和A数组一样的大小，让k指向result数组终止位置。比较左指针和右指针的平方大小

#### 参考代码

```java
class Solution {
    public int[] sortedSquares(int[] nums) {
        int leftIndex=0;
        int rightIndex=nums.length-1;
        int numsIndex=nums.length-1;
        int[]result=new int[nums.length];
        while(leftIndex<=rightIndex)
        {
            if(nums[leftIndex]*nums[leftIndex]>=nums[rightIndex]*nums[rightIndex])
            {
                result[numsIndex]=nums[leftIndex]*nums[leftIndex];
                leftIndex++;
            }
            else{
                result[numsIndex]=nums[rightIndex]*nums[rightIndex];
                rightIndex--;
            }
            numsIndex--;
        }
        return result;
    }
}
```

