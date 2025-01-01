---
date : '2024-12-31T20:35:31+08:00'
draft : false
title : '前缀和'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "前缀和思想在算法中的应用"
math : true
---

## 一维前缀和

### 题目描述

用于计算一维数组的区间和，将时间复杂度从$O(n * m) ,m 是查询的次数$简化到$O(n)$

### 算法思想

前缀和的思想是重复利用计算过的子数组之和，从而降低区间查询需要累加计算的次数。

例如，统计 vec[i] 这个数组上的区间和。

- 先做累加，即 p[i] 表示 下标 0 到 i 的 vec[i] 累加 之和。
- 统计vec数组上 下标 i 到下标 j 之间的累加和时使用**p[j]-p[i-1]**即可

```
p[i] = vec[0] + vec[1] + ... vec[i];
p[j] = vec[0] + vec[1] + vec[2] + vec[3] + vec[4] + vec[5] + ..vec[j];
p[j] - p[i] = vec[i+1] + vec[i+2] + vec[i+3] + ... +vec[j];
```

![img](20240627111319.png)

### 经典例题

#### 题目描述

[题目链接(opens new window)](https://kamacoder.com/problempage.php?pid=1070)

题目描述

给定一个整数数组 Array，请计算该数组在每个指定区间内元素的总和。

输入描述

第一行输入为整数数组 Array 的长度 n，接下来 n 行，每行一个整数，表示数组的元素。随后的输入为需要计算总和的区间，直至文件结束。

输出描述

输出每个指定区间内元素的总和。

输入示例

```text
5
1
2
3
4
5
0 1
1 3
```



输出示例

```text
3
9
```



数据范围：

0 < n <= 100000



#### 参考代码

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        int[] vec = new int[n];
        int[] p = new int[n];

        int presum = 0;
        for (int i = 0; i < n; i++) {
            vec[i] = scanner.nextInt();
            presum += vec[i];
            p[i] = presum;
        }

        while (scanner.hasNextInt()) {
            int a = scanner.nextInt();
            int b = scanner.nextInt();

            int sum;
            if (a == 0) {
                sum = p[b];
            } else {
                sum = p[b] - p[a - 1];
            }
            System.out.println(sum);
        }

        scanner.close();
    }
}
```

