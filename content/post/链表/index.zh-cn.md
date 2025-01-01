---
date : '2024-12-29T17:25:11+08:00'
draft : false
title : '链表'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "算法题中链表的经典模型和操作"
math : true
---

## 虚拟头节点

### 方法描述

**设置一个虚拟头结点**，这样原链表的所有节点就都可以按照统一的方式进行操作了。

### 经典例题

#### leetcode 203. 移除链表元素

[力扣题目链接(opens new window)](https://leetcode.cn/problems/remove-linked-list-elements/)

题意：删除链表中等于给定值 val 的所有节点。

示例 1： 输入：head = [1,2,6,3,4,5,6], val = 6 输出：[1,2,3,4,5]

示例 2： 输入：head = [], val = 1 输出：[]

示例 3： 输入：head = [7,7,7,7], val = 7 输出：[]

**参考代码**

```java
/**
 * 时间复杂度 O(n)
 * 空间复杂度 O(1)
 * @param head
 * @param val
 * @return
 */
public ListNode removeElements(ListNode head, int val) {
    // 设置一个虚拟的头结点
    ListNode dummy = new ListNode();
    dummy.next = head;

    ListNode cur = dummy;
    while (cur.next != null) {
        if (cur.next.val == val) {
            cur.next = cur.next.next;
        } else {
            cur = cur.next;        
        }
    }
    return dummy.next;
}
```

#### leetcode 24. 两两交换的节点

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/swap-nodes-in-pairs/)

给定一个链表，两两交换其中相邻的节点，并返回交换后的链表。

你不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。

![24.两两交换链表中的节点-题意](24.两两交换链表中的节点-题意.jpg)

**思路解析**

![24.两两交换链表中的节点1](24.两两交换链表中的节点1.png)



**参考代码**

```java
class Solution {
  public ListNode swapPairs(ListNode head) {
       ListNode dummy = new ListNode(-1); // 设置一个虚拟头结点
       dummy.next = head; // 将虚拟头结点指向head，这样方便后面做删除操作
       ListNode curr=dummy;
       ListNode temp; //保存两个节点后的节点
       ListNode firstNode; //保存curr后的第一个节点
       ListNode secondNode; //保存curr后的第二个节点
       while(curr.next!=null&&curr.next.next!=null)
       {
           firstNode=curr.next;
           secondNode=firstNode.next;
           temp=secondNode.next;
           curr.next=secondNode; // 步骤一
           secondNode.next=firstNode; //步骤二
           firstNode.next=temp; // 步骤三
           curr=firstNode; //重新设置为原先在secondNode位置上的节点
       }
      return dummy.next;
       
    }
}
```



#### leetcode 19. 删除链表的倒数第N个节点

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/)

给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。

进阶：你能尝试使用一趟扫描实现吗？

示例 1：

![19.删除链表的倒数第N个节点](20210510085957392.png)

输入：head = [1,2,3,4,5], n = 2 输出：[1,2,3,5]

示例 2：

输入：head = [1], n = 1 输出：[]

示例 3：

输入：head = [1,2], n = 1 输出：[1]

**思路解析**

使用快慢指针和虚拟头节点，让快节点从虚拟头节点开始，提前移动**n+1**步。![img](19.删除链表的倒数第N个节点1.png)

然后再让快节点和慢节点同时移动直到快节点移动到最后一个节点的后一个位置（**null**)

![img](19.删除链表的倒数第N个节点2.png)

此时快节点和慢节点之间间隔n个节点，慢节点位于要删除的节点的前一个节点位置

直接删除即可

```java
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        //新建一个虚拟头节点指向head
        ListNode dummyNode = new ListNode(0);
        dummyNode.next = head;
        //快慢指针指向虚拟头节点
        ListNode fastIndex = dummyNode;
        ListNode slowIndex = dummyNode;

        // 快指针移动n+1步，使得快慢指针相差 n 个结点即可
        for (int i = 0; i <= n; i++) {
            fastIndex = fastIndex.next;
        }
        // 两个指针同时移动，直到快指针移动到最后一个节点的后一个位置（null)
        while (fastIndex != null) {
            fastIndex = fastIndex.next;
            slowIndex = slowIndex.next;
        }

        // 检查 slowIndex.next 是否为 null，以避免空指针异常
        if (slowIndex.next != null) {
            slowIndex.next = slowIndex.next.next; // 直接删除节点
        }
        return dummyNode.next;
    }
}
```



## 反转操作

### 思路解析

只需要改变链表的next指针的指向，直接将链表反转 ，而不用重新定义一个新的链表

定义节点

- curr：当前节点
- prev：当前节点的上一个节点
- temp：当前节点的下一个节点

操作

- 记录curr的下一个指针temp
- 将指针反转，让curr指向prev
- 将prev节点设置为curr
- 将curr设置为temp

![](20210218090901207.png)

### 经典例题

#### leetcode 206. 翻装链表

[力扣题目链接(opens new window)](https://leetcode.cn/problems/reverse-linked-list/)

题意：反转一个单链表。

示例: 输入: 1->2->3->4->5->NULL 输出: 5->4->3->2->1->NULL

**参考代码**

```java
class Solution {
    public ListNode reverseList(ListNode head) {
       	ListNode prev=null;
        ListNode curr=head;
        ListNode temp=null;
        while(curr!=null)
        {
            temp=curr.next;
            curr.next=prev;
            prev=curr;
            curr=temp;
        }
        
    }
}
```

## 判断链表是否相交

### 思路解析

- 求出A链表和B链表的长度
- 让currB到currA对齐的位置
- 此时比较curA和curB是否相同，如果不相同，同时向后移动curA和curB，如果遇到curA == curB，则找到交点。

### 经典例题

#### leetcode 160. 链表相交

[力扣题目链接(opens new window)](https://leetcode.cn/problems/intersection-of-two-linked-lists-lcci/)

给你两个单链表的头节点 headA 和 headB ，请你找出并返回两个单链表相交的起始节点。如果两个链表没有交点，返回 null 。

图示两个链表在节点 c1 开始相交：

![img](20211219221657.png)

题目数据 保证 整个链式结构中不存在环。

注意，函数返回结果后，链表必须 保持其原始结构 。

示例 1：

![img](20211219221723.png)

示例 2：

![img](20211219221749.png)

示例 3：

![img](20211219221812.png)

## 

**参考代码**

```java
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode currA = headA;
        ListNode currB = headB;
        int lenA = 0, lenB = 0;
        while (currA != null) { // 求链表A的长度
            lenA++;
            currA = currA.next;
        }
        while (currB != null) { // 求链表B的长度
            lenB++;
            currB = currB.next;
        }
        // 将当前指针回到头节点
        currA = headA;
        currB = headB;
        // 让currA为最长链表的头，lenA为其长度
        if (lenB > lenA) {
            //1. swap (lenA, lenB); 交换长度
            int tmpLen = lenA;
            lenA = lenB;
            lenB = tmpLen;
            //2. swap (currA, currB); 交换节点
            ListNode tmpNode = currA;
            currA = currB;
            currB = tmpNode;
        }
        // 求长度差
        int gap = lenA - lenB;
        // 让currA和currB在同一起点上（末尾位置对齐）
        for(int i=0;i<gap;i++)
        {
            currA=currA.next;
        }
        // 遍历currA 和 currB，遇到相同则直接返回
        while (currA != null) {
            if (currA == currB) {
                return currA;
            }
            currA = currA.next;
            currB = currB.next;
        }
        return null;
    }

}
```

## 环形链表

### 思路解析

#### 判断是否是环形链表

使用快慢指针法，设置一个快指针和慢指针，让快指针一次移动两步，慢指针一次移动一步，若两个指针能相遇则该链表是环形链表

**证明过程**

fast指针一定先进入环中，如果fast指针和slow指针相遇的话，一定是在环中相遇

其实相对于slow来说，fast是一个节点一个节点的靠近slow的

#### **如何找到环的入口**

从头结点出发一个指针，从相遇节点 也出发一个指针，这两个指针每次只走一个节点， 那么当这两个指针相遇的时候就是 环形入口的节点。

### 经典例题

#### leetcode 142. 环形链表II

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/linked-list-cycle-ii/)

题意： 给定一个链表，返回链表开始入环的第一个节点。 如果链表无环，则返回 null。

为了表示给定链表中的环，使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。

**说明**：不允许修改给定的链表。

![循环链表](20200816110112704.png)

## 

**参考代码**

```java
public class Solution {
    public ListNode detectCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {// 有环
                ListNode index1 = fast;
                ListNode index2 = head;
                // 两个指针，从头结点和相遇结点，各走一步，直到相遇，相遇点即为环入口
                while (index1 != index2) {
                    index1 = index1.next;
                    index2 = index2.next;
                }
                return index1;
            }
        }
        return null;
    }
}
```

