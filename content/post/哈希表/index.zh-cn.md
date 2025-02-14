---
date : '2025-02-11T16:24:13+08:00'
draft : false
title : '哈希表'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "算法题中哈希表的应用"
math : true
---

## 数组作哈希表

数组就是简单的哈希表，但是数组的大小是受限的。通常用于在字母计数问题中

### 经典例题

#### leetcode 242 有效的字母异位词

题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/valid-anagram/)

给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。

示例 1: 输入: s = "anagram", t = "nagaram" 输出: true

示例 2: 输入: s = "rat", t = "car" 输出: false

**说明:** 你可以假设字符串只包含小写字母。



**思路解析**

小写字母的数量只有26个，故考虑使用数组作为哈希表。**因为字符a到字符z的ASCII是26个连续的数值，所以字符a映射为下标0，相应的字符z映射为下标25。**

- 使用一个数组 **`record`** 作为哈希表对字符串 **s** 进行字母计数，记录字符串中每个字符的出现次数
- 遍历另一个字符串 **t** ，每遇到一个字符将 **`record`** 中对应的计数减一
- 遍历 **`record`** ，如果出现不为零的元素代表多了或者少了字母，不是字母异位词

**参考代码**

```java
class Solution {
    public boolean isAnagram(String s, String t) {
        int[] record = new int[26];
        for(int i=0;i<s.length();i++)
        {
            record[s.charAt(i)-'a']++;
        }
        for(int i=0;i<t.length();i++)
        {
            record[t.charAt(i)-'a']--;
        }
        for(int count:record)
        {
            if(count!=0)
                return false;
        }
        return true;

    }
}
```

#### leetcode 383 赎金信

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/ransom-note/)

给定一个赎金信 (ransom) 字符串和一个杂志(magazine)字符串，判断第一个字符串 ransom 能不能由第二个字符串 magazines 里面的字符构成。如果可以构成，返回 true ；否则返回 false。

(题目说明：为了不暴露赎金信字迹，要从杂志上搜索各个需要的字母，组成单词来表达意思。杂志字符串中的每个字符只能在赎金信字符串中使用一次。)

**注意：**

你可以假设两个字符串均只含有小写字母。

canConstruct("a", "b") -> false
canConstruct("aa", "ab") -> false
canConstruct("aa", "aab") -> true



**思路解析**

与 **有效的字母异位词** 类似，将 **`magazines`** 中的字母出现次数进行记录，再遍历 **`ransom`** 修改哈希表中的字母出现次数，检验是否存在负数即可

**参考代码**

```java
class Solution {
    public boolean canConstruct(String ransomNote, String magazine) {
        int ch[]=new int[26];
        for(int i=0;i<magazine.length();i++)
        {
            ch[magazine.charAt(i)-'a']++;
        }
        for(int i=0;i<ransomNote.length();i++)
        {
            ch[ransomNote.charAt(i)-'a']--;
        }
        for(int i:ch)
        {
            if(i<0)return false;
        }
        return true;
    }
}
```



## Set做哈希表

### 经典例题

#### leetcode 349 两个数组的交集

[力扣题目链接(opens new window)](https://leetcode.cn/problems/intersection-of-two-arrays/)

题意：给定两个数组，编写一个函数来计算它们的交集。

![349. 两个数组的交集](https://code-thinking-1253855093.file.myqcloud.com/pics/20200818193523911.png)

**说明：** 输出结果中的每个元素一定是唯一的。 我们可以不考虑输出结果的顺序。

**思路解析**

对于集合的运算可以直接考虑使用set集合，使用两个set，一个set用于记录 **`nums1`** 中出现的不重复数字，一个set用于在遍历**`nums2`** 时记录前一个set和 **`nums2`** 的相同数字，转换为数组后作为答案返回

**参考代码**

```java
class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        HashSet<Integer> set=new HashSet<Integer>();
        HashSet<Integer> ans=new HashSet<Integer>();
        // 记录nums1的不重复数字
        for(Integer num1:nums1)
            set.add(num1);
        // 遍历nums2
        for(Integer num2:nums2)
        {
            //若是和set具有相同的数字
            if(set.contains(num2))
                ans.add(num2);
        }
        // 将set转换为数组返回
        int arr[]=new int[ans.size()];
        int index=0;
        for(Integer i:ans)
        {
            arr[index]=i;
            index++;
        }
        return arr;
    }
}
```



#### leetcode 202 快乐数

[力扣题目链接(opens new window)](https://leetcode.cn/problems/happy-number/)

编写一个算法来判断一个数 n 是不是快乐数。

「快乐数」定义为：对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和，然后重复这个过程直到这个数变为 1，也可能是 无限循环 但始终变不到 1。如果 可以变为 1，那么这个数就是快乐数。

如果 n 是快乐数就返回 True ；不是，则返回 False 。

**示例：**

输入：19
输出：true
解释：
1^2 + 9^2 = 82
8^2 + 2^2 = 68
6^2 + 8^2 = 100
1^2 + 0^2 + 0^2 = 1

**思路解析**

题目中说了会 **无限循环**，那么也就是说 **求和的过程中，sum会重复出现** ，由此可以转换成sum是否重复在一个集合中的问题

**参考代码**

```java
class Solution {
    public boolean isHappy(int n) {
        // 保存sum的出现情况
        HashSet<Integer>set=new HashSet<>();
        // 循环直到n=1或者出现重复的sum
        while(n!=1&&!set.contains(n))
        {
            set.add(n);
            n=getNext(n);
        }
        return n==1;
    }

    // 获取下一个数
    public static int getNext(int n)
    {
        int ans=0;
        while(n!=0)
        {
            int temp=n%10;
            ans+=temp*temp;
            n/=10;
        }
        return ans;
    }
}
```



## Map做哈希表

### 经典例题

#### leetcode 49 字母异位词分组

[力扣题目链接(opens new window)](https://leetcode.cn/problems/group-anagrams/description/)

给你一个字符串数组，请你将 **字母异位词** 组合在一起。可以按任意顺序返回结果列表。

**字母异位词** 是由重新排列源单词的所有字母得到的一个新单词。

**示例 1:**

```
输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

**示例 2:**

```
输入: strs = [""]
输出: [[""]]
```

**示例 3:**

```
输入: strs = ["a"]
输出: [["a"]]
```

 

**提示：**

- `1 <= strs.length <= 104`
- `0 <= strs[i].length <= 100`
- `strs[i]` 仅包含小写字母



**思路解析**

对于此类分组问题，首先要明确分组的标准。题目显式指出分组标准：使用相同的字母。明确了分组标准，只要以分组标准为键，

以分组内容为值，放入map中。

分组标准可以从以下角度表示

- 将每个字符串进行排序，字母异位词的排序结果相同
- 利用数组收集每个字母出现次数并拼接成字符串，字母异位词的字符串相同

**参考代码**

```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        HashMap<String,List<String>>map=new HashMap<String, List<String>>();
        for(String str:strs)
        {
            // 将每个字符串排序
            char[] arr=str.toCharArray();
            Arrays.sort(arr);
            // 将排序后的结果作为键
            String key=new String(arr);
            // 将键值对放入map中
            List<String> val=map.getOrDefault(key,new ArrayList<String>());
            val.add(str);
            map.put(key,val);
        }
        // 分组结果为map的值集合
        return new ArrayList<List<String>>(map.values());
    }
}
```

#### leetcode 350 两个数组的交集II

**题目描述**

[题目链接](https://leetcode.cn/problems/intersection-of-two-arrays-ii/description/)

给你两个整数数组 `nums1` 和 `nums2` ，请你以数组形式返回两数组的交集。返回结果中每个元素出现的次数，应与元素在两个数组中都出现的次数一致（如果出现次数不一致，则考虑取较小值）。可以不考虑输出结果的顺序。

**示例 1：**

```
输入：nums1 = [1,2,2,1], nums2 = [2,2]
输出：[2,2]
```

**示例 2:**

```
输入：nums1 = [4,9,5], nums2 = [9,4,9,8,4]
输出：[4,9] 
```

**提示：**

- `1 <= nums1.length, nums2.length <= 1000`
- `0 <= nums1[i], nums2[i] <= 1000`

**思路解析**

题目中出现了“出现次数”，故考虑使用map集合做哈希表。设计算法如下

- 使用一个map集合记录 **`nums1`**中数字的出现频率
- 遍历 **`nums2`** 获取 **`nums2`** 中的数字在map中的出现次数、
  - 如果出现次数大于0
    - 放入答案集中
    - 将map中的出现次数减一，当出现次数为0时移除该键值对

**参考代码**

```java
class Solution {
    public int[] intersect(int[] nums1, int[] nums2) {
        HashMap<Integer,Integer>map=new HashMap<>();
        int[]ans=new int[nums1.length];
        // 记录nums1中的数字出现频率
        for(Integer num1:nums1)
        {
            map.put(num1, map.getOrDefault(num1,0)+1);
        }
        // 记录交集的长度
        int index=0;
        // 遍历nums2
        for(Integer num2:nums2)
        {
            // 获取nums2中的数字在nums1中的出现次数
            int count=map.getOrDefault(num2,0);
            if(count>0)
            {
                // 将nums2中的数字加入答案集
                ans[index++]=num2;
                // nums2中的数字在nums1中的出现次数减一
                count--;
                // 更新map
                if(count>0)
                {
                    map.put(num2,count);
                }
                else {
                    map.remove(num2);
                }
            }
        }
        return Arrays.copyOf(ans,index);
    }
}
```

#### leetcode 1 两数之和

[力扣题目链接(opens new window)](https://leetcode.cn/problems/two-sum/)

给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。

**示例:**

给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9

所以返回 [0, 1]

**思路解析**

本题需要遍历 **`nums`** 数组 ，然后判断 **`target-nums[i]`** 是否在哈希表中。由于本题需要记录数组下标，所以需要使用map集合记录元素下标

**参考代码**

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        // 使用map集合记录前面的数组元素
        HashMap<Integer,Integer>map=new HashMap<>();
        int[]res=new int[2];
        if(nums == null || nums.length == 0){
            return res;
        }
        for(int i=0;i<nums.length;i++)
        {
            // 寻找temp是否在哈希表中
            int temp=target-nums[i];
            if(map.containsKey(temp))
            {
                res[0]=map.get(temp);
                res[1]=i;
                break;
            }
            map.put(nums[i],i);
        }
        return res;
    }
}
```

#### leetcode 454 四数相加

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/4sum-ii/)

给定四个包含整数的数组列表 A , B , C , D ,计算有多少个元组 (i, j, k, l) ，使得 A[i] + B[j] + C[k] + D[l] = 0。

为了使问题简单化，所有的 A, B, C, D 具有相同的长度 N，且 0 ≤ N ≤ 500 。所有整数的范围在 -2^28 到 2^28 - 1 之间，最终结果不会超过 2^31 - 1 。

**例如:**

输入:

- A = [ 1, 2]
- B = [-2,-1]
- C = [-1, 2]
- D = [ 0, 2]

输出:

2

**解释:**

两个元组如下:

1. (0, 0, 0, 1) -> A[0] + B[0] + C[0] + D[1] = 1 + (-2) + (-1) + 2 = 0
2. (1, 1, 0, 0) -> A[1] + B[1] + C[0] + D[0] = 2 + (-1) + (-1) + 0 = 0

**思路解析**

本题不需要列举出具体的四元组，只需要列举了组合数。这里需要建立sum和出现次数的映射关系，于是需要map集合

- 遍历 **`nums1`** 和 **`nums2`** 记录两个数组的元素之和与出现次数的映射关系
- 遍历 **`nums3`** 和 **`nums4`** ，查询map集合是否存在键为 **`0-nums3-nums4`** 的键值对

**参考代码**

```java
class Solution {
    public int fourSumCount(int[] nums1, int[] nums2, int[] nums3, int[] nums4) {
        int res=0;
        HashMap<Integer,Integer>map=new HashMap<>();
        // 统计nums1和nums2的元素之和以及出现次数
        for(Integer i:nums1)
        {
            for(Integer j:nums2)
            {
                int sum=i+j;
                map.put(sum,map.getOrDefault(sum,0)+1);
            }
        }
        // 统计nums3和nums4的元素之和的相反数是否在map中出现
        for(Integer i:nums3)
        {
            for(Integer j:nums4)
            {
                res+=map.getOrDefault(0-i-j,0);
            }
        }
        return res;
    }
}
```

