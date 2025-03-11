---
date : '2024-12-30T15:29:22+08:00'
draft : false
title : '双指针法-滑动窗口法'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "算法题中滑动窗口法的应用"
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
- 迭代右移左指针同时更新结果（更新结果和移动左边界处于同一个while循环中）

#### 代码模板

```java
class solution{
    public result<T> search(int[]nums)
    {
        int left=0;
        for(int right=0;right<nums.length;right++)
        {
            calculate();// 计算约束条件
            // 判断[i, j]是否满足条件
    		while 满足条件
            {
                update(result); // 不断更新结果(注意在while内更新！)
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
- 一开始滑窗满足条件，向右移动右指针直到不满足条件
- 迭代右移右边界的过程中更新结果（更新结果和移动左边界不在一个while循环内）
- 最保守的压缩左边界，一旦满足条件了就退出压缩左边界的过程，使得滑窗尽可能的大

#### 代码模板

```java
class solution{
    public result<T> search(int[]nums)
    {
        int left=0;
        for(int right=0;right<nums.length;right++)
        {
            calculate();// 计算约束条件
            // 判断[i, j]是否满足条件
    		while 不满足条件
            {
                left++; //（最保守的压缩左边界，一旦满足条件了就退出压缩左边界的过程，使得滑窗尽可能的大）
            }
            update(result);
        }
        return result;
    }
}
```

### 固定滑动窗口

#### 题目前提

题目中出现显式的窗口长度或字符串长度可以考虑使用

#### 代码模板

```java
class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        int left=0;
        for(int right=0;right<s.length();right++){
           	// 将右侧元素加入窗口
            if(right<pLen-1){ //窗口大小不足
                continue;
            }
            // 更新答案
            // 窗口左侧元素离开队列
            left++;
        }
        return ans;
    }
}
```



## 经典例题

### leetcode 209. 长度最小的子数组

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/minimum-size-subarray-sum/)

给定一个含有 n 个正整数的数组和一个正整数 s ，找出该数组中满足其和 ≥ s 的长度最小的 连续 子数组，并返回其长度。如果不存在符合条件的子数组，返回 0。

示例：

- 输入：s = 7, nums = [2,3,1,2,4,3]
- 输出：2
- 解释：子数组 [4,3] 是该条件下的长度最小的子数组。

提示：

- 1 <= target <= 10^9
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^5

#### 思路解析

题目前提条件为

- 给定数组 nums
- 求满足某个条件的滑窗的最小长度。
- 窗口一开始不满足条件

故采用最小滑动窗口策略

#### 参考代码

```java
class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int left=0;
        int sum=0;
        int result=Integer.MAX_VALUE;
        for(int right=0;right<nums.length;right++)
        {	
            // 1.计算约束条件
            sum+=nums[right];
            // 2.当窗口满足条件
            while(sum>=target) 
            {
                // 3. 更新结果
                result=Math.min(result,right-left+1); 
                // 4. 右移右边界
                sum-=nums[left];
                left++;
            }
        }
        return result;
    }
}
```

### leetcode 904. 水果成篮

#### 题目描述

[力扣题目链接](https://leetcode.cn/problems/fruit-into-baskets/description/)

你正在探访一家农场，农场从左到右种植了一排果树。这些树用一个整数数组 `fruits` 表示，其中 `fruits[i]` 是第 `i` 棵树上的水果 **种类** 。

你想要尽可能多地收集水果。然而，农场的主人设定了一些严格的规矩，你必须按照要求采摘水果：

- 你只有 **两个** 篮子，并且每个篮子只能装 **单一类型** 的水果。每个篮子能够装的水果总量没有限制。
- 你可以选择任意一棵树开始采摘，你必须从 **每棵** 树（包括开始采摘的树）上 **恰好摘一个水果** 。采摘的水果应当符合篮子中的水果类型。每采摘一次，你将会向右移动到下一棵树，并继续采摘。
- 一旦你走到某棵树前，但水果不符合篮子的水果类型，那么就必须停止采摘。

给你一个整数数组 `fruits` ，返回你可以收集的水果的 **最大** 数目。

**示例 1：**

```
输入：fruits = [1,2,1]
输出：3
解释：可以采摘全部 3 棵树。
```

**示例 2：**

```
输入：fruits = [0,1,2,2]
输出：3
解释：可以采摘 [1,2,2] 这三棵树。
如果从第一棵树开始采摘，则只能采摘 [0,1] 这两棵树。
```

**示例 3：**

```
输入：fruits = [1,2,3,2,2]
输出：4
解释：可以采摘 [2,3,2,2] 这四棵树。
如果从第一棵树开始采摘，则只能采摘 [1,2] 这两棵树。
```

**示例 4：**

```
输入：fruits = [3,3,3,1,2,1,1,2,3,3,4]
输出：5
解释：可以采摘 [1,2,1,1,2] 这五棵树。
```

 

**提示：**

- `1 <= fruits.length <= 105`
- `0 <= fruits[i] < fruits.length`

#### 思路解析

本题可以抽象为求解一个滑动窗口，滑动窗口内只有两种数字，求解滑动窗口长度的最大值

题目前提条件

- 给定数组 nums
- 求满足某个条件的滑窗的最大长度。
- 窗口一开始满足条件

故采用最大滑动窗口策略

#### 参考代码

```java
class Solution {
    public int totalFruit(int[] fruits) {
        int n=fruits.length;
        if(n==1)return 1;
        if(n==2)return 2;
        int left=0;
        int ans=0;
        int result=1;
        HashMap<Integer,Integer>map=new HashMap<>();
        for(int right=0;right<fruits.length;right++)
        {
            // 1.计算约束条件（水果的种类数）
            map.put(fruits[right],map.getOrDefault(fruits[right],0)+1);
            // 2.若不满足条件
            while(map.size()>2)
            {
                // 3.右移左边界
                map.put(fruits[left],map.get(fruits[left])-1);
                if(map.get(fruits[left])==0)
                    map.remove(fruits[left]);
                left++;
            }
            // 4.更新结果
           result=Math.max(result,right-left+1);
        }
        return result;
    }
}
```

### leetcode 76 最小覆盖子串

#### 题目描述

给你一个字符串 `s` 、一个字符串 `t` 。返回 `s` 中涵盖 `t` 所有字符的最小子串。如果 `s` 中不存在涵盖 `t` 所有字符的子串，则返回空字符串 `""` 。

**注意：**

- 对于 `t` 中重复字符，我们寻找的子字符串中该字符数量必须不少于 `t` 中该字符数量。
- 如果 `s` 中存在这样的子串，我们保证它是唯一的答案。

 

**示例 1：**

```
输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
解释：最小覆盖子串 "BANC" 包含来自字符串 t 的 'A'、'B' 和 'C'。
```

**示例 2：**

```
输入：s = "a", t = "a"
输出："a"
解释：整个字符串 s 是最小覆盖子串。
```

**示例 3:**

```
输入: s = "a", t = "aa"
输出: ""
解释: t 中两个字符 'a' 均应包含在 s 的子串中，
因此没有符合条件的子字符串，返回空字符串。
```

 

**提示：**

- `m == s.length`
- `n == t.length`
- `1 <= m, n <= 105`
- `s` 和 `t` 由英文字母组成

####  思路解析

本题可以将覆盖子串抽象为一个滑动窗口，求解该滑动窗口的最小值

故采用最小滑动窗口策略

#### 参考代码

```java
class Solution {
    public String minWindow(String s, String t) {
       	int[]cnS=new int[128];
       	int[]cnT=new int[128];
       	char[]S=s.toCharArray();
       	char[]T=t.toCharArray();
       	for(char e:T)
       	{
           cnT[e]++;
       	}
       	int left=0;
 		int ansLeft=-1;
        int ansRight=s.length-1;
        for(int right=0;right<s.length;right++)
        {
            // 1.计算约束条件
            cnS[S[right]]++;
            // 2.若满足条件
            while(isCover(cnS,cnT))
            {
                // 3.更新结果
                if(right-left+1<ansRight-ansLeft+1)
                {
                    ansLeft=left;
                    ansRight=right;
                }
                // 4.右移左边界
                cnT[S[left]]--;
                left++;
            }
        }
        return ansLeft<0?"":s.substring(ansLeft,ansRight+1);
    }
    
    //通过统计子串中字符的出现次数来判断是否覆盖
    public static boolean isCover(int[]cnS,int[]cnT)
    {
        for(int i='a';i<='z';i++)
        {
            if(cnS[i]<cnT[i])
            {
                return false;
            }
        }
        for(int i='A';i<='Z';i++)
        {
            if(cnS[i]<cnT[i])
            {
                return false;
            }
        }
        return true;
    }
}
```

### leetcode 438 找到字符串中所有的字母异位词

#### 题目描述

[题目链接](https://leetcode.cn/problems/find-all-anagrams-in-a-string/description/)

给定两个字符串 `s` 和 `p`，找到 `s` 中所有 `p` 的 

**异位词** 的子串，返回这些子串的起始索引。不考虑答案输出的顺序。

**示例 1:**

```
输入: s = "cbaebabacd", p = "abc"
输出: [0,6]
解释:
起始索引等于 0 的子串是 "cba", 它是 "abc" 的异位词。
起始索引等于 6 的子串是 "bac", 它是 "abc" 的异位词。
```

 **示例 2:**

```
输入: s = "abab", p = "ab"
输出: [0,1,2]
解释:
起始索引等于 0 的子串是 "ab", 它是 "ab" 的异位词。
起始索引等于 1 的子串是 "ba", 它是 "ab" 的异位词。
起始索引等于 2 的子串是 "ab", 它是 "ab" 的异位词。
```

**提示:**

- `1 <= s.length, p.length <= 3 * 104`
- `s` 和 `p` 仅包含小写字母

#### 思路解析

可以考虑设置一个长度为字符串p的长度的滑动窗口，移动滑动窗口比较窗口内的子串是否是p的字母异位词

#### 参考代码

```java
class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer>ans=new ArrayList<>();
        int sLen=s.length();
        int pLen=p.length();
        if(sLen<pLen)return ans;
        // 设置两个哈希表，分别记录s和p的字母出现次数
        int[]sCount=new int[26];
        int[]pCount=new int[26];
        // 比较起始位置是否是字母异位词
        for(int i=0;i<pLen;i++)
        {
            pCount[p.charAt(i)-'a']++;
        }
        int left=0;
        for(int right=0;right<s.length();right++){
            sCount[s.charAt(right)-'a']++;
            if(right<pLen-1){
                continue;
            }
            if(Arrays.equals(sCount,pCount)){
                ans.add(left);
            }
            sCount[s.charAt(left)-'a']--;
            left++;
        }
        return ans;
    }
}
```

### leetcode 3 无重复字符的最长子串

#### 题目描述

[题目链接](https://leetcode.cn/problems/longest-substring-without-repeating-characters/description/)

给定一个字符串 `s` ，请你找出其中不含有重复字符的 **最长 子串** 的长度。

**示例 1:**

```
输入: s = "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
```

**示例 2:**

```
输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
```

**示例 3:**

```
输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
```

#### 思路解析

- 题目前提条件

  - 给定数组 nums
  - 求满足某个条件的滑窗的最大长度。
  - 窗口一开始满足条件

  故采用最大滑动窗口策略

#### 参考代码

```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        if(s.isEmpty())return 0;
        HashMap<Character,Integer>map=new HashMap<>();
        int left=0;
        int res=Integer.MIN_VALUE;
        for(int right=0;right<s.length();right++){
            // 计算约束条件
            char ch=s.charAt(right);
            map.put(ch,map.getOrDefault(ch,0)+1);
            // 不满足条件
            while(map.get(ch)>1){
                // 压缩左边界
                map.put(s.charAt(left),map.get(s.charAt(left))-1);
                left++;
            }
            res=Math.max(res,right-left+1);
        }
        return res;
    }
}
```

