---
date : '2025-02-19T18:47:15+08:00'
draft : false
title : '模拟'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "模拟题的常见操作"
math : true
---

## 数组旋转

### leetcode 48 旋转数组

#### 题目描述

给定一个 *n* × *n* 的二维矩阵 `matrix` 表示一个图像。请你将图像顺时针旋转 90 度。

你必须在**[ 原地](https://baike.baidu.com/item/原地算法)** 旋转图像，这意味着你需要直接修改输入的二维矩阵。**请不要** 使用另一个矩阵来旋转图像。

 

**示例 1：**

![img](mat1.jpg)

```
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[[7,4,1],[8,5,2],[9,6,3]]
```

**示例 2：**

![img](mat2.jpg)

```
输入：matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
输出：[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
```

#### 思路解析

对于矩阵中第*i*行的第*j*个元素，在旋转后，它出现在倒数第*i*列的第*j*个位置

因此对于矩阵中的元素 **`matrix[row][col]`** ，在旋转后，它的新位置为 **`matrix_new[col][n−row−1]`** 。

**辅助数组法**

```java
class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        int[][] matrix_new = new int[n][n];
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                matrix_new[j][n - i - 1] = matrix[i][j];
            }
        }
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                matrix[i][j] = matrix_new[i][j];
            }
        }
    }
}
```

**翻转法**

可以先将矩阵通过水平轴翻转，再通过主对角线翻转
$$
对于水平轴翻转而言，我们只需要枚举矩阵上半部分的元素，和下半部分的元素进行交换，即\\
matrix[row][col]\to^{水平轴翻转}matrix[n−row−1][col]
$$

$$
对于主对角线翻转而言，我们只需要枚举对角线左侧的元素，和右侧的元素进行交换，即\\
matrix[row][col] \to^{主对角线翻转}matrix[col][row]
$$

```java
class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        // 水平翻转
        for (int i = 0; i < n / 2; ++i) {
            for (int j = 0; j < n; ++j) {
                int temp = matrix[i][j];
                matrix[i][j] = matrix[n - i - 1][j];
                matrix[n - i - 1][j] = temp;
            }
        }
        // 主对角线翻转
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < i; ++j) {
                int temp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = temp;
            }
        }
    }
}

```

## 数学

### 位运算

- 逻辑左移：**`<<`** 末尾补0等价于乘2
- 逻辑右移：**`>>>`** 左端补0
- 算术右移：**`>>`** 左端最低位填充
- 按位求与：**`&`**
- 按位求或：**`|`**
- 按位异或： **`^`** 
- 按位求非： **`~`**

### leetcode 338 比特位计数

#### 题目描述

给你一个整数 `n` ，对于 `0 <= i <= n` 中的每个 `i` ，计算其二进制表示中 **`1` 的个数** ，返回一个长度为 `n + 1` 的数组 `ans` 作为答案。



**示例 1：**

```
输入：n = 2
输出：[0,1,1]
解释：
0 --> 0
1 --> 1
2 --> 10
```

**示例 2：**

```
输入：n = 5
输出：[0,1,1,2,1,2]
解释：
0 --> 0
1 --> 1
2 --> 10
3 --> 11
4 --> 100
5 --> 101
```

#### 思路解析

将n与1进行与操作，等价于得到n的二进制位的最后一位，然后再让n右移一位

#### 参考代码

```java
class Solution {
    public int[] countBits(int n) {
        int[]res=new int[n+1];
        for(int i=0;i<=n;i++)
        {
            res[i]=count(i);
        }
        return res;
    }
    public int count(int n)
    {
        int count=0;
        while(n>0)
        {
            count+=n&1;
            n>>=1;
        }
        return count;
    }
}
```

