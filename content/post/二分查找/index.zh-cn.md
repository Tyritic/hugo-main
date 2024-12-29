---
date : '2024-12-29T10:52:54+08:00'
draft : false
title : '二分查找'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "二分查找的算法模板和题解思路"
---

## 题目特征

前提条件

- 数组为有序数组
- 强调数组中无重复元素

题目的前提是数组为有序数组，同时题目还强调数组中无重复元素，因为一旦有重复元素，使用二分查找法返回的元素下标可能不是唯一的，这些都是使用二分法的前提条件，当大家看到题目描述满足如上条件的时候，可要想一想是不是可以用二分法了。

## 算法模板

### 左闭右闭（推荐使用）

定义 target 是在一个在左闭右闭的区间里，也就是[left, right] 。

#### 临界条件的变化

- while (left <= right) 要使用 <= ，因为left == right是有意义的，所以使用 <=
- if (nums[middle] > target) right 要赋值为 middle - 1，因为当前这个nums[middle]一定不是target，那么接下来要查找的左区间结束下标位置就是 middle - 1

#### 代码模板

```java
class solution{
    public int search(int[]nums,int target)
    {
        //定义target处于区间[left,right]中
        int left=0; //左边界
        int right=nums.length-1; //右边界
        while(left<=right)
        {
            int mid=left+(right-left)/2; //防止溢出 等同于(left + right)/2
            if(nums[mid]>target)
                right=mid-1; //查找区间为[left,mid-1]
            else if(nums[mid]<target)
                left=mid+1; //查找区间为[mid+1.right]
            else //nums[mid]==target
                return mid;
        }
        return -1; //若未找到返回-1，表示数组中不存在该元素
    }
}
```

#### 结果分析

若数组中找不到元素此时满足条件

- **left=right+1**
- 同时nums[left]是大于target的元素中最小的，nums[right]是小于target元素中最大的

### 左闭右开

定义 target 是在一个在左闭右开的区间里，也就是[left, right） 。

#### 临界条件的变化

- while (left < right) 要使用 < ，因为left == right是没有意义的
- if (nums[middle] > target) right 要赋值为 middle ，因为当前这个nums[middle]一定不是target，那么接下来要查找的左区间结束下标位置就是 middle，下一个查询区间不会去比较nums[middle]

#### 代码模板

```java
class solution{
    public int search(int[]nums,int target)
    {
        //定义target处于区间[left,right)中
        int left=0; //左边界
        int right=nums.length; //右边界
        while(left<right)
        {
            int mid=left+(right-left)/2; //防止溢出 等同于(left + right)/2
            if(nums[mid]>target)
                right=mid; //查找区间为[left,mid-1]
            else if(nums[mid]<target)
                left=mid+1; //查找区间为[mid+1.right]
            else //nums[mid]==target
                return mid;
        }
        return -1; //若未找到返回-1，表示数组中不存在该元素
    }
}
```

#### 结果分析

若数组中找不到元素此时满足条件

- **left=right**
- 同时nums[left]=nums[right]是大于target的元素中最小的

## 经典例题

### leetcode 704. 二分查找

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/binary-search/)

给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target  ，写一个函数搜索 nums 中的 target，如果目标值存在返回下标，否则返回 -1。

示例 1:

```text
输入: nums = [-1,0,3,5,9,12], target = 9     
输出: 4       
解释: 9 出现在 nums 中并且下标为 4     
```

示例 2:

```text
输入: nums = [-1,0,3,5,9,12], target = 2     
输出: -1        
解释: 2 不存在 nums 中因此返回 -1        
```

提示：

- 你可以假设 nums 中的所有元素是不重复的。
- n 将在 [1, 10000]之间。
- nums 的每个元素都将在 [-9999, 9999]之间。

#### 思路分析

直接嵌套算法模板即可

#### 参考代码

左闭右闭版本

```java
class Solution {
    public int search(int[] nums, int target) {
        int left=0,right=nums.length-1;
        while(left<=right)
        {
            int mid=left+(right-left)/2;
            if(nums[mid]<target)
                left=mid+1;
            else if(nums[mid]>target)
                right=mid-1;
            else
                return mid;
        }
        return -1;
    }
}
```

左闭右开版本

```java
class Solution {
    public int search(int[] nums, int target) {
        int left=0,right=nums.length;
        while(left<right)
        {
            int mid=left+(right-left)/2;
            if(nums[mid]<target)
                left=mid+1;
            else if(nums[mid]>target)
                right=mid;
            else
                return mid;
        }
        return -1;
    }
}
```

### leetcode 35. 搜索插入位置

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/search-insert-position/)

给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。如果目标值不存在于数组中，返回它将会被按顺序插入的位置。

你可以假设数组中无重复元素。

示例 1:

- 输入: [1,3,5,6], 5
- 输出: 2

示例 2:

- 输入: [1,3,5,6], 2
- 输出: 1

示例 3:

- 输入: [1,3,5,6], 7
- 输出: 4

示例 4:

- 输入: [1,3,5,6], 0
- 输出: 0

#### 思路分析

注意这道题目的前提是数组是有序数组

同时题目还强调数组中无重复元素，因为一旦有重复元素，使用二分查找法返回的元素下标可能不是唯一的。

分别处理四种可能情况

- 目标值在数组所有元素之前  [0, -1]
- 目标值等于数组中某一个元素  return middle
- 目标值插入数组中的位置 [left, right]，return  right + 1
- 目标值在数组所有元素之后的情况 [left, right]， 因为是右闭区间，所以 return right + 1

#### 参考代码

```java
class Solution {
    public int searchInsert(int[] nums, int target) {
        int left=0;
        int right=nums.length-1;
        while(left<=right)
        {
            int mid=left+(right-left)/2;
            if(nums[mid]<target)
            {
                left=mid+1;
            }
            else if(nums[mid]>target)
            {
                right=mid-1;
            }
            else{
                return mid;
            }
        }
        // 2.目标值在数组所有元素之前 
        // 3.目标值插入数组中 
        // 4.目标值在数组所有元素之后 
        return right+1;
    }
}
```

### leetcode 34. 在排序数组中查找元素的第一个和最后一个位置

#### 题目描述

[力扣链接(opens new window)](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)

给定一个按照升序排列的整数数组 nums，和一个目标值 target。找出给定目标值在数组中的开始位置和结束位置。

如果数组中不存在目标值 target，返回 [-1, -1]。

进阶：你可以设计并实现时间复杂度为 $O(\log n)$ 的算法解决此问题吗？

示例 1：

- 输入：nums = [5,7,7,8,8,10], target = 8
- 输出：[3,4]

示例 2：

- 输入：nums = [5,7,7,8,8,10], target = 6
- 输出：[-1,-1]

示例 3：

- 输入：nums = [], target = 0
- 输出：[-1,-1]

#### 思路分析

题目条件

- 给定一个按照升序排列的整数数组 nums
- 一个目标值 target。

符合二分查找的前提条件考虑使用二分查找

具体思路如下

- 首先，在 nums 数组中二分查找 target；
- 如果二分查找失败，则 binarySearch 返回 -1，表明 nums 中没有 target。此时，searchRange 直接返回 {-1, -1}；
- 如果二分查找成功，则 binarySearch 返回 nums 中值为 target 的一个下标。然后，通过左右滑动指针，来找到等于target的区间

#### 参考代码

```java
class Solution {
    public int[] searchRange(int[] nums, int target) {
        int index=BinarySearch(nums,target); // 1.先进行二分查找
        if(index==-1)
            return new int[]{-1,-1};
        int left=index; //左边界
        int right=index; //右边界
        // 2.移动左边界
        while(left>0&&nums[left-1]==nums[index])
            left--;
        // 3.移动右边界
        while(right<nums.length-1&&nums[right+1]==nums[index])
            right++;
        return new int[]{left,right};
        
    }
    public static int BinarySearch(int[] nums, int target) {
        int left=0;
        int right=nums.length-1;
        while(left<=right)
        {
            int mid=left+(right-left)/2;
            if(nums[mid]<target)
            {
                left=mid+1;
            }
            else if(nums[mid]>target)
            {
                right=mid-1;
            }
            else{
                return mid;
            }
        }
        return -1;
    }
}
```



### leetcode 69. x的平方根

#### 题目描述

[力扣题目链接](https://leetcode.cn/problems/sqrtx/description/)

给你一个非负整数 `x` ，计算并返回 `x` 的 **算术平方根** 。

由于返回类型是整数，结果只保留 **整数部分** ，小数部分将被 **舍去 。**

**注意：**不允许使用任何内置指数函数和算符，例如 `pow(x, 0.5)` 或者 `x ** 0.5` 。

 

**示例 1：**

```
输入：x = 4
输出：2
```

**示例 2：**

```
输入：x = 8
输出：2
解释：8 的算术平方根是 2.82842..., 由于返回类型是整数，小数部分将被舍去。
```

 

**提示：**

- `0 <= x <= 231 - 1`

#### 思路分析

题目中隐含条件，平方根在[1,x]中且该区域为有序递增数组，考虑使用二分查找

#### 参考代码

```java
class Solution {
    public int mySqrt(int x) {
        if(x==0)return 0;
        if(x==1)return 1;
        int left=0,right=x/2;
        while(left<=right)
        {
            int mid=left+(right-left)/2;
            if(nums[mid]<target)
                left=mid+1;
            else if(nums[mid]>target)
                right=mid-1;
            else
                return mid;
        }
        return right; //结果为比x小的最大整数
    }
}
```



### leetcode 367. 有效的完全平方数

#### 题目描述

[力扣题目链接](https://leetcode.cn/problems/valid-perfect-square/description/)

给你一个正整数 `num` 。如果 `num` 是一个完全平方数，则返回 `true` ，否则返回 `false` 。

**完全平方数** 是一个可以写成某个整数的平方的整数。换句话说，它可以写成某个整数和自身的乘积。

不能使用任何内置的库函数，如 `sqrt` 。

 

**示例 1：**

```
输入：num = 16
输出：true
解释：返回 true ，因为 4 * 4 = 16 且 4 是一个整数。
```

**示例 2：**

```
输入：num = 14
输出：false
解释：返回 false ，因为 3.742 * 3.742 = 14 但 3.742 不是一个整数。
```

 

**提示：**

- `1 <= num <= 231 - 1`

#### 思路分析

同上一题，注意细节：mid*mid非常容易溢出，所以采取的策略是用除法代替乘法

#### 参考代码

```java
class Solution {
    public boolean isPerfectSquare(int num) {
        int left=0;
        int right=num;
        if(num==0||num==1)return true;// 1.特殊值判断
        while(left<=right)
        {
            int mid=left+(right-left)/2;
            if(mid==num/(mid*1.0))
                return true;
            else if (mid>num/(mid*1.0))
                right=mid-1;
            else 
                left=mid+1;
        }
        return false;
    }
}
```

