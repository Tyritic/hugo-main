---
date : '2025-02-18T11:43:20+08:00'
draft : false
title : '回溯算法'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "回溯算法在算法题中的应用"
math : true
---

## 回溯算法的经典问题

回溯法，一般可以解决如下几种问题：

- 组合问题：N个数里面按一定规则找出k个数的集合
- 切割问题：一个字符串按一定规则有几种切割方式
- 子集问题：一个N个数的集合里有多少符合条件的子集
- 排列问题：N个数按一定规则全排列，有几种排列方式
- 棋盘问题：N皇后，解数独等等

## 回溯算法的统一解题模板

- 确定回溯函数模板返回值以及参数

  ```java
  void backtracking(参数)
  ```

  - 回溯算法中函数返回值一般为void。结果集合使用全局变量
  - 回溯算法需要的参数所以一般是先写逻辑，然后需要什么参数，就填什么参数。

- 确定回溯算法的终止条件

  ```java
  if (终止条件) {
      存放结果;
      return;
  }
  ```

  - 一般来说搜到叶子节点了，也就找到了满足条件的一条答案，把这个答案存放起来，并结束本层递归。

- 确定单次遍历过程

  ```java
  for (选择：本层集合中元素（树中节点孩子的数量就是集合的大小）) {
      处理节点;
      backtracking(路径，选择列表); // 递归
      回溯，撤销处理结果
  }
  ```

  - 处理节点
  - 递归处理
  - 回溯

## 组合问题

### leetcode  77 组合

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/combinations/)

给定两个整数 n 和 k，返回 1 ... n 中所有可能的 k 个数的组合。

示例: 输入: n = 4, k = 2 输出: [ [2,4], [3,4], [2,3], [1,2], [1,3], [1,4], ]

#### 思路解析

- 确定回溯函数模板返回值以及参数
  - 返回值为 **`void`**
  - 参数为n，k，startIndex（记录下一层递归，搜索的起始位置）
- 确定回溯算法的终止条件
  - 当path的大小为k时，将path加入res
- 确定单次遍历过程
  - 遍历1...n
    - 将数字i加入路径中
    - 递归处理i+1
    - 回溯处理数字i，将i从path中移除
- 遍历过程中可以进行剪枝处理
  - 已经选择的元素个数：path.size();
  - 还需要的元素个数为: k - path.size();
  - 在集合n中至多要从该起始位置 : n - (k - path.size()) + 1，开始遍历

#### 参考代码

```java
class Solution {
    List<List<Integer>>res;
    List<Integer>path;
    public List<List<Integer>> combine(int n, int k) {
        res=new ArrayList<>();
        path=new ArrayList<>();
        backtracking(n,k,1);
        return res;
    }

    public void backtracking(int n,int k,int startIndex)
    {
        // 终止条件
        if(path.size()==k)
        {
            res.add(new ArrayList<>(path));
            return;
        }
        for(int i=startIndex;i<=n-(k-path.size())+1;i++)
        {
            path.add(i);
            backtracking(n,k,i+1);
            path.remove(path.size()-1);
        }
    }
}
```

### leetcode 216 组合总和III

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/combination-sum-iii/)

找出所有相加之和为 n 的 k 个数的组合。组合中只允许含有 1 - 9 的正整数，并且 **每种组合中不存在重复的数字** 。

说明：

- 所有数字都是正整数。
- 解集不能包含重复的组合。

示例 1: 输入: k = 3, n = 7 输出: [[1,2,4]]

示例 2: 输入: k = 3, n = 9 输出: [[1,2,6], [1,3,5], [2,3,4]]

#### 思路解析

- 确定回溯函数模板返回值以及参数
  - 返回值为 **`void`**
  - 参数为n，k，startIndex（记录下一层递归，搜索的起始位置）
- 确定回溯算法的终止条件
  - 当path的大小为k时判断是否sum==n
- 确定单次遍历过程
  - 遍历1...9
    - 处理数字i
      - 将数字i加入路径中
      - sum+=i
    - 递归处理i+1
    - 回溯处理数字i
      - 将i从path中移除
      - sum-=i
- 遍历过程中可以进行剪枝处理
  - 已经选择的元素个数：path.size();
  - 还需要的元素个数为: k - path.size();
  - 在集合n中至多要从该起始位置 : 9 - (k - path.size()) + 1，开始遍历

#### 参考代码

```java
class Solution {
    List<List<Integer>>res;
    List<Integer>path;
    public List<List<Integer>> combinationSum3(int k, int n) {
        res=new ArrayList<>();
        path=new ArrayList<>();
        backtracking(k,n,1,0);
        return res;
    }

    public void backtracking(int k,int n,int startIndex,int sum)
    {
        // 终止条件
        if(path.size()==k)
        {
            if(sum==n)
                res.add(new ArrayList<>(path));
            return;
        }
        // 单次遍历
        for(int i=startIndex;i<=9-(k-path.size())+1;i++)
        {
            sum+=i;
            path.add(i);
            backtracking(k,n,i+1,sum);
            path.remove(path.size()-1);
            sum-=i;
        }
    }
}
```



### leetcode 17 电话号码的数字组合

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/)

给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。

给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。

![17.电话号码的字母组合](2020102916424043.png)

示例:

- 输入："23"
- 输出：["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].

说明：尽管上面的答案是按字典序排列的，但是你可以任意选择答案输出的顺序。

#### 思路解析

- 建立数字和字母的映射关系
- 确定回溯函数模板返回值以及参数
  - 返回值为 **`void`**
  - 参数为index（记录选择遍历的第几个字母）
- 确定回溯算法的终止条件
  - 当遍历的数字下标等于字符串长度，将局部字符串加入结果
- 确定单次遍历过程
  - 获取遍历到的数字对应的字符串
  - 遍历字符串的每个字符
    - 将字符加入局部字符串
    - 递归处理index+1
    - 回溯处理

#### 参考代码

```java
class Solution {
    List<String>res=new ArrayList<>();
    StringBuffer temp=new StringBuffer();
    String[]map=new String[]{" "," ","abc","def","ghi","jkl","mno",
    "pqrs","tuv","wxyz"};
    public List<String> letterCombinations(String digits) {
        if (digits == null || digits.length() == 0) {
            return res;
        }
        backtrack(digits,0);
        return res;
    }

    public void backtrack(String digits,int index)
    {
        // 终止条件
        if(index==digits.length())
        {
            res.add(temp.toString());
            return;
        }
        //单次递归
        char ch=digits.charAt(index);
        String str=map[ch-'0'];
        for(int i=0;i<str.length();i++)
        {
            temp.append(str.charAt(i));
            backtrack(digits,index+1);
            temp.deleteCharAt(temp.length()-1);
        }

    }
}
```

### leetcode 39 组合总和

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/combination-sum/)

给定一个无重复元素的数组 candidates 和一个目标数 target ，找出 candidates 中所有可以使数字和为 target 的组合。

**candidates 中的数字可以无限制重复被选取。**

说明：

- 所有数字（包括 target）都是正整数。
- 解集不能包含重复的组合。

示例 1：

- 输入：candidates = [2,3,6,7], target = 7,
- 所求解集为： [ [7], [2,2,3] ]

示例 2：

- 输入：candidates = [2,3,5], target = 8,
- 所求解集为： [ [2,2,2,2], [2,3,3], [3,5] ]

#### 思路解析

- 先对数组进行排序
- 确定回溯函数模板返回值以及参数
  - 返回值为 **`void`**
  - 参数为candidates，sum，target，startIndex（记录下一层递归，搜索的起始位置）
- 确定回溯算法的终止条件
  - 当sum==target将path加入res
- 确定单次遍历过程
  - 从startIndex开始遍历
    - 若sum+candidates[i]>target可以直接停止循环
    - 处理数字i
      - 将数字i加入路径中
      - sum+=i
    - 递归处理i
    - 回溯处理数字i
      - 将i从path中移除
      - sum-=i

#### 参考代码

```java
class Solution {
    List<List<Integer>>res=new ArrayList<>();
    List<Integer>path=new ArrayList<>();
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        Arrays.sort(candidates); // 先进行排序
        backtrack(candidates,target,0,0);
        return res;
    }

    public void backtrack(int[]candidates,int target,int startIndex,int sum)
    {
        if(sum==target)
        {
            res.add(new ArrayList<>(path));
            return;
        }
        for(int i=startIndex;i<candidates.length;i++)
        {
            if(sum+candidates[i]>target)
                break;
            path.add(candidates[i]);
            sum+=candidates[i];
            backtrack(candidates,target,i,sum);
            sum-=candidates[i];
            path.removeLast();
        }
    }
}
```

### leetcode 40 组合总和II

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/combination-sum-ii/)

给定一个数组 candidates 和一个目标数 target ，找出 candidates 中所有可以使数字和为 target 的组合。

candidates 中的每个数字在每个组合中只能使用一次。

说明： 所有数字（包括目标数）都是正整数。**解集不能包含重复的组合**。

- 示例 1:
- 输入: candidates = [10,1,2,7,6,1,5], target = 8,
- 所求解集为:

```text
[
  [1, 7],
  [1, 2, 5],
  [2, 6],
  [1, 1, 6]
]
```



- 示例 2:
- 输入: candidates = [2,5,2,1,2], target = 5,
- 所求解集为:

```text
[
  [1,2,2],
  [5]
]
```

#### 思路解析

本题的重点在于如何去重，以及去重的角度。

元素在同一个组合内是可以重复的，但两个组合不能相同。

**所以我们要去重的是同一树层上的“使用过”，同一树枝上的都是一个组合里的元素，不用去重**。

- used[i - 1] == true，说明同一树枝candidates[i - 1]使用过
- used[i - 1] == false，说明同一树层candidates[i - 1]使用过

![40.组合总和II](20230310000918.png)

- 先对数组进行排序
- 确定回溯函数模板返回值以及参数
  - 返回值为 **`void`**
  - 参数为candidates，sum，target，startIndex（记录下一层递归，搜索的起始位置）
- 确定回溯算法的终止条件
  - 当sum==target将path加入res
- 确定单次遍历过程
  - 从startIndex开始遍历
    - 若sum+candidates[i]>target可以直接停止循环
    - 若used[i - 1] == false，说明同一树层candidates[i - 1]使用过，continue之后的操作
    - 处理数字i
      - 将数字i加入路径中
      - sum+=i
      - used[i]=true
    - 递归处理i
    - 回溯处理数字i
      - 将i从path中移除
      - sum-=i
      - used[i]=false

#### 参考代码

```java
class Solution {
    List<List<Integer>>res=new ArrayList<>();
    List<Integer>path=new ArrayList<>();
    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        boolean[]used=new boolean[candidates.length];
        Arrays.sort(candidates);
        backtrack(candidates,target,0,0,used);
        return res;
    }

    public void backtrack(int[]candidates,int target,int sum,int startIndex,boolean[]used)
    {
        if(target==sum)
        {
            res.add(new ArrayList<>(path));
        }
        for(int i=startIndex;i<candidates.length;i++)
        {
            if (sum + candidates[i] > target) {
                break;
            }
            if(i>0&&candidates[i]==candidates[i-1]&&used[i-1]==false)
                continue;
            sum+=candidates[i];
            path.add(candidates[i]);
            used[i]=true;
            backtrack(candidates,target,sum,i+1,used);
            used[i]=false;
            path.removeLast();
            sum-=candidates[i];
        }

    }
}
```

### leetcode 131 分割回文串

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/palindrome-partitioning/)

给定一个字符串 s，将 s 分割成一些子串，使每个子串都是回文串。

返回 s 所有可能的分割方案。

示例: 输入: "aab" 输出: [ ["aa","b"], ["a","a","b"] ]

#### 思路解析

**切割问题类似组合问题**。

对于字符串abcdef：

- 组合问题：选取一个a之后，在bcdef中再去选取第二个，选取b之后在cdef中再选取第三个.....。
- 切割问题：切割一个a之后，在bcdef中再去切割第二段，切割b之后在cdef中再切割第三段.....。

总体思路

- 递归函数参数
  - 全局变量数组path存放切割后回文的子串，二维数组result存放结果集。
  - startIndex作为截取位置
- 递归函数终止条件
  - 切割线切到了字符串最后面是本层递归的终止条件。
- 单次遍历
  - 从startIndex开始遍历字符串
    - 截取子串[startIndex，i]作为子串
    - 验证是否为回文串若是
      - 将子串加入结果集
      - 递归处理i+1
      - 回溯

#### 参考代码

```java
class Solution {
    List<List<String>>res=new ArrayList<>();
    List<String>path=new ArrayList<>();
    public List<List<String>> partition(String s) {
        backtrack(s,0);
        return res;
    }
    public boolean check(String str)
    {
        int left=0;
        int right=str.length()-1;
        while(left<=right)
        {
            if(str.charAt(left)!=str.charAt(right))
                return false;
            left++;
            right--;
        }
        return true;
    }

    public void backtrack(String s,int startIndex)
    {
        //终止条件
        if(startIndex>=s.length())
        {
            res.add(new ArrayList<>(path));
            return;
        }
        for(int i=startIndex;i<s.length();i++)
        {
            String str=s.substring(startIndex,i+1);
            if(check(str))
            {
                path.add(str);
                backtrack(s,i+1);
                path.removeLast();
            }

        }
    }
}
```

