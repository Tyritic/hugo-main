---
date : '2024-12-29T16:21:01+08:00'
draft : false
title : '双指针法—快慢指针法'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "算法题中双指针法的应用"
math : true
---

## 题目描述

通常当使用蛮力法需要两个for循环时，将两个for循环削减成一个for循环的优化方法。时间复杂度$O(n^2)$可以优化为$O(n)$

## 算法模板

### 方法步骤

双指针法（快慢指针法）： **通过一个快指针和慢指针在一个for循环下完成两个for循环的工作。**

新数组指在旧数组的基础上修改后的数组

定义快慢指针

- 快指针：通过遍历旧数组来寻找新数组的元素 ，新数组就是不含有目标元素的数组
- 慢指针：指向更新后新数组下标的位置

### 代码模板

```java
class solution{
    public int solution(int[]nums,int val)
    {
        int slowIndex=0;
        for(int fastIndex=0;fastIndex<nums.length;fastIndex++)
        {
            //题目要求的操作,用于构建新数组，if条件内是符合新数组要求的谓词
            //fastIndex用于遍历原数组
            //slowIndex用于插入新数组
        }
        return slowIndex;
    }
}
```

### 结果分析

slowIndex是新数组的元素个数。

## 经典例题

### leetcode 27. 移除元素

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/remove-element/)

给你一个数组 nums 和一个值 val，你需要**原地**移除所有数值等于 val 的元素，并返回移除后数组的新长度。

不要使用额外的数组空间，你必须仅使用 O(1) 额外空间并**原地**修改输入数组。

元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。

示例 1: 给定 nums = [3,2,2,3], val = 3, 函数应该返回新的长度 2, 并且 nums 中的前两个元素均为 2。 你不需要考虑数组中超出新长度后面的元素。

示例 2: 给定 nums = [0,1,2,2,3,0,4,2], val = 2, 函数应该返回新的长度 5, 并且 nums 中的前五个元素为 0, 1, 3, 0, 4。

**你不需要考虑数组中超出新长度后面的元素。**



#### 思路解析

题目条件中**原地**一词提示使用快慢指针法，将$O(n^2)$的操作转变为$O(n)$的操作



#### 参考代码

```java
class Solution {
    public int removeElement(int[] nums, int val) {
        int slowIndex=0;
        for(int fastIndex=0;fastIndex<nums.length;fastIndex++)
        {
            if(nums[fastIndex]!=val)
            {
                nums[slowIndex++]=nums[fastIndex];
            }
        }
        return slowIndex;
    }
}
```



### leetcode 26. 删除有序数组的重复项

#### 题目描述

[力扣题目链接](https://leetcode.cn/problems/backspace-string-compare/description/)

给你一个 **非严格递增排列** 的数组 `nums` ，请你**[ 原地](http://baike.baidu.com/item/原地算法)** 删除重复出现的元素，使每个元素 **只出现一次** ，返回删除后数组的新长度。元素的 **相对顺序** 应该保持 **一致** 。然后返回 `nums` 中唯一元素的个数。

考虑 `nums` 的唯一元素的数量为 `k` ，你需要做以下事情确保你的题解可以被通过：

- 更改数组 `nums` ，使 `nums` 的前 `k` 个元素包含唯一元素，并按照它们最初在 `nums` 中出现的顺序排列。`nums` 的其余元素与 `nums` 的大小不重要。
- 返回 `k` 。

**判题标准:**

系统会用下面的代码来测试你的题解:

```
int[] nums = [...]; // 输入数组
int[] expectedNums = [...]; // 长度正确的期望答案

int k = removeDuplicates(nums); // 调用

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
```

如果所有断言都通过，那么您的题解将被 **通过**。

 

**示例 1：**

```
输入：nums = [1,1,2]
输出：2, nums = [1,2,_]
解释：函数应该返回新的长度 2 ，并且原数组 nums 的前两个元素被修改为 1, 2 。不需要考虑数组中超出新长度后面的元素。
```

**示例 2：**

```
输入：nums = [0,0,1,1,1,2,2,3,3,4]
输出：5, nums = [0,1,2,3,4]
解释：函数应该返回新的长度 5 ， 并且原数组 nums 的前五个元素被修改为 0, 1, 2, 3, 4 。不需要考虑数组中超出新长度后面的元素。
```

 

**提示：**

- `1 <= nums.length <= 3 * 104`
- `-104 <= nums[i] <= 104`
- `nums` 已按 **非严格递增** 排列

#### 思路解析

题目条件中**原地**一词提示使用快慢指针法，将$O(n^2)$的操作转变为$O(n)$的操作

**`slow`** 指针指向新数组中被更新元素下一个位置

**`fast`** 指针遍历原数组

根据题意，第一个元素 **`nums[0]`** 一定会被保留故 **`slow`** 从 **1** 开始，于是 **fast** 从 **1** 开始，当遇到与新数组的最后一个有效元素不重复的元素就更新数组

#### 参考代码

```java
class Solution {
    public int removeDuplicates(int[] nums) {
        int slow=1;
        for(int fast=1;fast<nums.length;fast++)
        {
            if(nums[fast]!=nums[slow-1])
            {
                nums[slow++]=nums[fast];
            }
        }
        return slow;
    }
}
```



### leetcode 283. 移动零

#### 题目描述

[力扣题目链接](https://leetcode.cn/problems/move-zeroes/)

给定一个数组 `nums`，编写一个函数将所有 `0` 移动到数组的末尾，同时保持非零元素的相对顺序。

**请注意** ，必须在不复制数组的情况下原地对数组进行操作。



**示例 1:**

```
输入: nums = [0,1,0,3,12]
输出: [1,3,12,0,0]
```

**示例 2:**

```
输入: nums = [0]
输出: [0]
```

 

**提示**:

- `1 <= nums.length <= 104`
- `-231 <= nums[i] <= 231 - 1`

#### 思路解析

- 将所有不等于0的元素放入原先的数组中
- 在新数组的尾部全部置为零

#### 参考代码

```java
class Solution {
    public void moveZeroes(int[] nums) {
        int slowIndex=0;
        for(int fastIndex=0;fastIndex<nums.length;fastIndex++)
        {
            if(nums[fastIndex]!=0)
            {
                nums[slowIndex++]=nums[fastIndex];
            }
        }
        for(int i=slowIndex;i<nums.length;i++)
        {
            nums[i]=0;
        }
    }
}
```



### leetcode 844. 比较含退格的字符串

#### 题目描述

[力扣题目链接](https://leetcode.cn/problems/backspace-string-compare/description/)

给定 `s` 和 `t` 两个字符串，当它们分别被输入到空白的文本编辑器后，如果两者相等，返回 `true` 。`#` 代表退格字符。

**注意：**如果对空文本输入退格字符，文本继续为空。

 

**示例 1：**

```
输入：s = "ab#c", t = "ad#c"
输出：true
解释：s 和 t 都会变成 "ac"。
```

**示例 2：**

```
输入：s = "ab##", t = "c#d#"
输出：true
解释：s 和 t 都会变成 ""。
```

**示例 3：**

```
输入：s = "a#c", t = "b"
输出：false
解释：s 会变成 "c"，但 t 仍然是 "b"。
```

 

**提示：**

- `1 <= s.length, t.length <= 200`
- `s` 和 `t` 只含有小写字母以及字符 `'#'`

#### 思路解析

基本思路

- 将s和t经过退格操作后的字符串求解出（封装成一个函数）
- 对比求解后的字符串来判断（主函数中进行）

退格操作的求解思路

- 定义快慢指针fastIndex和slowIndex
- fastIndex从左往右遍历
  - 当遇到非退格符号时slowIndex正常记录数组元素
  - 当遇到退格符号时slowIndex向后退一位

#### 参考代码

```java
class Solution {
    public boolean backspaceCompare(String s, String t) {
        String s1=checked(s);
        String s2=checked(t);
        if(s1.equals(s2))
        {
            return true;
        }
        return false;
    }
    
	//求解退格处理后的字符串
    public static String checked(String s)
    {
        char[]chars=s.toCharArray(s);
        int slowIndex=0;
        for(int fastIndex=0;fastIndex<chars.length;fastIndex++)
        {
            //遍历旧数组，不为退格符#的字符保留
            if(chars[fastIndex]!='#')
                chars[slowIndex++]=chars[fastIndex];
            //遍历旧数组，为退格符#的字符进行退格处理
            else if(chars[fastIndex]=='#')
            {
                //slowIndex是新数组的长度
                if(slowIndex>0)
                    slowIndex--;
            }
        }
        return new String(chars).substring(0,slow);
    }
}
```

