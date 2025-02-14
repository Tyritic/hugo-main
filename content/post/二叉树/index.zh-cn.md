---
date : '2025-02-13T17:30:22+08:00'
draft : false
title : '二叉树'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "二叉树在算法题中的使用"
math : true
---

## 二叉树的统一解题模板

本质上二叉树的题目是递归的一种，与树相关的递归思路可以从以下方式思考

- **确定递归函数的参数和返回值：** 确定哪些参数是递归的过程中需要处理的，那么就在递归函数里加上这个参数， 并且还要明确每次递归的返回值是什么进而确定递归函数的返回类型。
- **确定终止条件：** 写完了递归算法, 运行的时候，经常会遇到栈溢出的错误，就是没写终止条件或者终止条件写的不对，操作系统也是用一个栈的结构来保存每一层递归的信息，如果递归没有终止，操作系统的内存栈必然就会溢出。
- **确定单层递归的逻辑：** 确定每一层递归需要处理的信息。在这里也就会重复调用自己来实现递归的过程。

## 二叉树的遍历方式

二叉树的大部分题目都是基于遍历来解决。二叉树的遍历方式有以下四种

- 前序遍历：根左右
- 后序遍历：左右根
- 中序遍历：左根右
- 层序遍历：将树按照层次进行遍历

### 递归遍历思路

以前序遍历为例

- 前序遍历
  - **确定递归函数的参数和返回值**：不需要再处理什么数据了也不需要有返回值，所以递归函数返回类型就是void
  - **确定终止条件**：当前遍历的节点是空了，那么本层递归就要结束了，所以如果当前遍历的这个节点是空，就直接return
  - **确定单层递归的逻辑**：前序遍历是中左右的顺序，所以在单层递归的逻辑，是要先取中节点的数值

#### leetcode 144 二叉树的前序遍历

**题目描述**

[题目链接](https://leetcode.cn/problems/binary-tree-preorder-traversal/description/)

给你二叉树的根节点 `root` ，返回它节点值的 **前序** 遍历。

**示例 1：**

**输入：** root = [1,null,2,3]

**输出：**[1,2,3]

**解释：**

![img](screenshot-2024-08-29-202743.png)

**示例 2：**

**输入：** root = [1,2,3,4,5,null,8,null,null,6,7,9]

**输出：**[1,2,4,5,6,7,3,8,9]

**解释：**

![img](tree_2.png)

**示例 3：**

**输入：** root = []

**输出：**[]

**示例 4：**

**输入：** root = [1]

**输出：**[1]

**参考代码**

```java
class Solution {
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer>res=new ArrayList<>();
        preorder(root,res);
        return res;
    }
    public void preorder(TreeNode root,List<Integer>res)
    {
        // 终止条件
        if(root==null)
            return;
        // 遍历过程
        res.add(root.val);
        preorder(root.left,res);
        preorder(root.right,res);
    }
}
```

#### leetcode 145 二叉树的后序遍历

**题目描述**

[题目链接](https://leetcode.cn/problems/binary-tree-postorder-traversal/)

给你一棵二叉树的根节点 `root` ，返回其节点值的 **后序遍历** 。

 

**示例 1：**

**输入：** root = [1,null,2,3]

**输出：** [3,2,1]

**解释：**

![img](https://assets.leetcode.com/uploads/2024/08/29/screenshot-2024-08-29-202743.png)

**示例 2：**

**输入：** root = [1,2,3,4,5,null,8,null,null,6,7,9]

**输出：** [4,6,7,5,2,9,8,3,1]

**解释：**

![img](https://assets.leetcode.com/uploads/2024/08/29/tree_2.png)

**示例 3：**

**输入：** root = []

**输出：** []

**示例 4：**

**输入：** root = [1]

**输出：** [1]

 

**提示：**

- 树中节点的数目在范围 `[0, 100]` 内
- `-100 <= Node.val <= 100`

**参考代码**

```java
class Solution {
    public List<Integer> postorderTraversal(TreeNode root) {
        List<Integer>res=new ArrayList<>();
        transfer(root,res);
        return res;
    }
    public void transfer(TreeNode root,List<Integer>res)
    {
        // 终止条件
        if(root==null)
            return;
        transfer(root.left,res);
        transfer(root.right,res);
        res.add(root.val);
    }

}
```

#### leetcode 94 二叉树的中序遍历

**题目描述**

[题目链接](https://leetcode.cn/problems/binary-tree-inorder-traversal/description/)

给定一个二叉树的根节点 `root` ，返回 *它的 **中序** 遍历* 。

**示例 1：**

![img](inorder_1.jpg)

```
输入：root = [1,null,2,3]
输出：[1,3,2]
```

**示例 2：**

```
输入：root = []
输出：[]
```

**示例 3：**

```
输入：root = [1]
输出：[1]
```

 

**提示：**

- 树中节点数目在范围 `[0, 100]` 内
- `-100 <= Node.val <= 100`



**参考代码**

```java
class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer>res=new ArrayList<>();
        transfer(root,res);
        return res;
    }

    public void transfer(TreeNode root,List<Integer>res)
    {
        if(root==null)
            return;
        transfer(root.left,res);
        res.add(root.val);
        transfer(root.right,res);
    }

}
```

### 迭代遍历思路

使用一个栈作为存储结构，但是栈存在 **无法同时解决访问节点（遍历节点）和处理节点（将元素放进结果集）不一致的情况** 。**那我们就将访问的节点放入栈中，把要处理的节点也放入栈中但是要做标记。** 通常可以将要处理的节点后面放入一个空指针

#### 前序遍历

栈中的行为

- 放入根节点，然后直接出栈，但是保留根节点的引用
- 右节点入栈，栈中元素[右节点]
- 左节点入栈，栈中元素[右节点，左节点]
- 根节点入栈，栈中元素[右节点，左节点，根节点]
- 出栈顺序：根节点，左节点，右节点

```java
class Solution {
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> result = new LinkedList<>();
        Stack<TreeNode> st = new Stack<>();
        if (root != null) st.push(root);
        while (!st.empty()) {
            TreeNode node = st.peek();
            if (node != null) {
                st.pop(); // 将该节点弹出，避免重复操作，下面再将右中左节点添加到栈中
                if (node.right!=null) st.push(node.right);  // 添加右节点（空节点不入栈）
                if (node.left!=null) st.push(node.left);    // 添加左节点（空节点不入栈）
                st.push(node);                          // 添加中节点
                st.push(null); // 中节点访问过，但是还没有处理，加入空节点做为标记。
                
            } else { // 只有遇到空节点的时候，才将下一个节点放进结果集
                st.pop();           // 将空节点弹出
                node = st.peek();    // 重新取出栈中元素
                st.pop();
                result.add(node.val); // 加入到结果集
            }
        }
        return result;
    }
}
```

#### 中序遍历

栈中行为

- 放入根节点，然后直接出栈，但是保留根节点的引用
- 右节点入栈，栈中元素[右节点]
- 根节点入栈，栈中元素[右节点，根节点]
- 左节点入栈，栈中元素[右节点，根节点，左节点]
- 出栈顺序：左节点，根节点，右节点

```java
class Solution {
public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new LinkedList<>();
    Stack<TreeNode> st = new Stack<>();
    if (root != null) st.push(root);
    while (!st.empty()) {
        TreeNode node = st.peek();
        if (node != null) {
            st.pop(); // 将该节点弹出，避免重复操作，下面再将右中左节点添加到栈中
            if (node.right!=null) st.push(node.right);  // 添加右节点（空节点不入栈）
            st.push(node);                          // 添加中节点
            st.push(null); // 中节点访问过，但是还没有处理，加入空节点做为标记。

            if (node.left!=null) st.push(node.left);    // 添加左节点（空节点不入栈）
        } else { // 只有遇到空节点的时候，才将下一个节点放进结果集
            st.pop();           // 将空节点弹出
            node = st.peek();    // 重新取出栈中元素
            st.pop();
            result.add(node.val); // 加入到结果集
        }
    }
    return result;
}
}
```

#### 后序遍历

栈中行为

- 放入根节点，然后直接出栈，但是保留根节点的引用
- 根节点入栈，栈中元素[根节点]
- 右节点入栈，栈中元素[根节点，右节点]
- 左节点入栈，栈中元素[根节点，右节点，左节点]
- 出栈顺序：左节点，右节点，根节点

```java
class Solution {
   public List<Integer> postorderTraversal(TreeNode root) {
        List<Integer> result = new LinkedList<>();
        Stack<TreeNode> st = new Stack<>();
        if (root != null) st.push(root);
        while (!st.empty()) {
            TreeNode node = st.peek();
            if (node != null) {
                st.pop(); // 将该节点弹出，避免重复操作，下面再将中右左节点添加到栈中
                st.push(node);                          // 添加中节点
                st.push(null); // 中节点访问过，但是还没有处理，加入空节点做为标记。
                if (node.right!=null) st.push(node.right);  // 添加右节点（空节点不入栈）
                if (node.left!=null) st.push(node.left);    // 添加左节点（空节点不入栈）         
                               
            } else { // 只有遇到空节点的时候，才将下一个节点放进结果集
                st.pop();           // 将空节点弹出
                node = st.peek();    // 重新取出栈中元素
                st.pop();
                result.add(node.val); // 加入到结果集
            }
        }
        return result;
   }
}
```

### 层次遍历思路

使用一个队列来模拟遍历，每次出队时将节点的左右子节点放入队列中

#### 代码模板

```java
		Queue<TreeNode>queue=new LinkedList<>();
        queue.add(root);
        while (!queue.isEmpty())
        {
            int size=queue.size();
            // 以层为单位的操作，size是每一层的元素个数
            for(int i=0;i<size;i++)
            {
                TreeNode temp=queue.poll();
                // 题目中对单个元素特定操作
                if(temp.left!=null)
                    queue.offer(temp.left);
                if(temp.right!=null)
                    queue.offer(temp.right);
            }
            // 每层结束后的操作
        }
```

#### leetcode 102 二叉树的层次遍历

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/binary-tree-level-order-traversal/)

给你一个二叉树，请你返回其按 层序遍历 得到的节点值。 （即逐层地，从左到右访问所有节点）。

![102.二叉树的层序遍历](https://code-thinking-1253855093.file.myqcloud.com/pics/20210203144842988.png)

**参考代码**

```java
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>>res=new ArrayList<>();
        if(root==null)return res;
        // 引入辅助队列
        Queue<TreeNode>que=new LinkedList<>();
        // 添加根节点
        que.offer(root);
        while(!que.isEmpty())
        {
            // 为每一层建立一个list存储每一层的结果
            List<Integer>ans=new ArrayList<>();
            // 每一层的操作，其中size是每一层的元素个数
            int size=que.size();
            for(int i=0;i<size;i++)
            {
                TreeNode temp=que.poll();
                // 对单个元素的操作
                ans.add(temp.val);
                if(temp.left!=null)que.offer(temp.left);
                if(temp.right!=null)que.offer(temp.right);
            }
            // 每一层遍历完之后的操作
            res.add(ans);
        }
        return res;
    }

}
```

#### leetcode 637 二叉树的层平均值

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/average-of-levels-in-binary-tree/)

给定一个非空二叉树, 返回一个由每层节点平均值组成的数组。

![637.二叉树的层平均值](20210203151350500.png)

**参考代码**

```java
class Solution {
    public List<Double> averageOfLevels(TreeNode root) {
        ArrayList<Double>res=new ArrayList<>();
        if(root==null)return res;
        // 建立辅助队列
        Queue<TreeNode>que=new LinkedList<>();
        // 根节点入队
        que.offer(root);
        while(!que.isEmpty())
        {
            // 定义每层的变量
            int size=que.size();
            double count=0;
            // 层内遍历
            for(int i=0;i<size;i++)
            {
                TreeNode temp=que.poll();
                // 对层内元素求和
                count+=temp.val;
                if(temp.left!=null)
                    que.offer(temp.left);
                if(temp.right!=null)
                    que.offer(temp.right);
            }
            // 每一层遍历结束后加入结果集
            res.add(count/size);
        }
        return res;
    }
}
```

#### leetcode 515 在每个树行中找最大值

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/find-largest-value-in-each-tree-row/)

您需要在二叉树的每一行中找到最大的值。

![515.在每个树行中找最大值](20210203151532153.png)

**参考代码**

```java
class Solution {
    public List<Integer> largestValues(TreeNode root) {
        List<Integer>res=new ArrayList<>();
        if(root==null)return res;
        // 设置辅助队列
        Queue<TreeNode>que=new LinkedList<>();
        // 根节点入队
        que.offer(root);
        while(!que.isEmpty())
        {
            // 设置每一层的最大值
            int max=Integer.MIN_VALUE;
            int size=que.size();
            for(int i=0;i<size;i++)
            {
                TreeNode temp=que.poll();
                if(temp.val>max)
                    max=temp.val;
                if(temp.left!=null)
                    que.offer(temp.left);
                if(temp.right!=null)
                    que.offer(temp.right);
            }
            // 遍历完一层后将最大值放入队列中
            res.add(max);
        }
        return res;
    }
}
```

## 二叉树的深度问题

二叉树的最大深度是根节点到最远叶子节点的最长路径上的节点数。只有一个节点的二叉树深度为1

### 最大深度问题

#### leetcode 104 二叉树的最大深度

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/maximum-depth-of-binary-tree/)

给定一个二叉树，找出其最大深度。

二叉树的深度为根节点到最远叶子节点的最长路径上的节点数。

说明: 叶子节点是指没有子节点的节点。

示例：

给定二叉树 [3,9,20,null,null,15,7]，

![104. 二叉树的最大深度](https://code-thinking-1253855093.file.myqcloud.com/pics/20210203153031914-20230310134849764.png)

返回它的最大深度 3 。

**思路解析**

本题可以从迭代和递归两个角度思考

**迭代法**

因为最大的深度就是二叉树的层数，和层序遍历的方式相似。在二叉树中，一层一层的来遍历二叉树，记录一下遍历的层数就是二叉树的深度

**迭代法参考代码**

```java
class Solution {
    public int maxDepth(TreeNode root) {
        int depth=0;
        if(root==null)return 0;
        Queue<TreeNode>que=new LinkedList<>();
        que.offer(root);
        while(!que.isEmpty())
        {
            // 进行每一层遍历前的操作
            int size=que.size();
            depth++;
            for(int i=0;i<size;i++)
            {
                TreeNode temp=que.poll();
                if(temp.left!=null)que.offer(temp.left);
                if(temp.right!=null)que.offer(temp.right);
            }
        }
        return depth;
    }

}
```

**递归法**

根据递归的模板逐步确定思路

- **确定递归函数的参数和返回值：** 由题可知递归函数的参数为树的根节点，返回值为根的深度
- **确定终止条件：** 如果为空节点的话，就返回0，表示高度为0。
- **确定单层递归的逻辑：** 
  - 求最大深度可以转换为求根高度，求高度通常采用后序遍历
    - 左节点的处理：先计算左子树的高度
    - 右节点的处理：再计算右子树的高度
    - 中节点的处理：选取左右子树高度的最大值加1（中间节点）
  - 本质上求深度应当使用前序遍历
    - 中节点的处理：让当前层级递增，处理当前层级和最大深度的关系
    - 左节点的处理：计算左子树的层数
    - 右节点的处理：计算右子树的层数
    - 最后回溯层数

**参考代码**

```java
// 后序遍历法
class Solution {
    public int maxDepth(TreeNode root) {
        int depth=0;
        // 设置终止条件
        if(root==null)
            return 0;
        // 单次遍历逻辑：后序遍历
        int leftDepth=maxDepth(root.left); // 处理左子树
        int rightDepth=maxDepth(root.right); // 处理右子树
        return Math.max(leftDepth,rightDepth)+1; // 处理中间节点
    }

}

// 前序遍历法
class Solution {
    int maxDepth=0;
    public int maxDepth(TreeNode root) {
        dfs(root,0);
        return maxDepth;
    }
    // depth为当前节点的层级
    public void dfs(TreeNode root,int depth)
    {
        // 终止条件
        if(root==null)
            return;
        // 中间节点处理
        depth++; //层级递增
        maxDepth=maxDepth>depth?maxDepth:depth; // 计算最大深度
        // 处理左节点
        dfs(root.left,depth);
        // 处理右节点
        dfs(root.right,depth);
        // 回溯
        depth--;
    }

}
```

### 最小深度问题

二叉树的最小深度是从根节点到最近叶子节点的最短路径上的节点数量。。只有一个节点的二叉树深度为1。

#### leetcode 111 二叉树的最小深度

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/minimum-depth-of-binary-tree/)

给定一个二叉树，找出其最小深度。

最小深度是从根节点到最近叶子节点的最短路径上的节点数量。

说明: 叶子节点是指没有子节点的节点。

示例:

给定二叉树 [3,9,20,null,null,15,7],

![111.二叉树的最小深度1](2021020315582586.png)

返回它的最小深度 2.

**思路解析**

本题可以从迭代和递归两个角度思考

**迭代法**

因为深度可以用二叉树的层数，和层序遍历的方式相似。在二叉树中，一层一层的来遍历二叉树，遍历到没有左右子节点的节点就停止记录

**参考代码**

```java
class Solution {
    public int minDepth(TreeNode root) {
        int depth=0;
        if(root==null)return depth;
        Queue<TreeNode>que=new LinkedList<>();
        que.offer(root);
        while(!que.isEmpty())
        {
            int size=que.size();
            depth++;
            for(int i=0;i<size;i++)
            {
                TreeNode temp=que.poll();
                if(temp.left==null&&temp.right==null)
                    return depth;
                if(temp.left!=null)que.offer(temp.left);
                if(temp.right!=null)que.offer(temp.right);
            }
        }
        return depth;
    }
}
```

**递归法**

- **确定递归函数的参数和返回值：** 由题可知递归函数的参数为树的根节点，返回值为根的深度
- **确定终止条件：** 如果为空节点的话，就返回0，表示高度为0。
- **确定单层递归的逻辑：** 
  - 求最大深度可以转换为求根高度，求高度通常采用后序遍历
    - 左节点的处理：先计算左子树的高度
    - 右节点的处理：再计算右子树的高度
    - 中节点的处理：
      - 当左节点为空选取右子树的高度
      - 当右节点为空选取左子树的高度
      - 选取左右子树高度的较小值+1
  - 本质上求深度应当使用前序遍历
    - 中节点的处理：让当前层级递增，判断是否为叶子节点，若为叶子节点处理当前层级和最大深度的关系
    - 左节点的处理：计算左子树的层数
    - 右节点的处理：计算右子树的层数
    - 最后回溯层数

**参考代码**

```java
// 前序遍历
class Solution {
    int minDepth=Integer.MAX_VALUE;
    public int minDepth(TreeNode root) {
        if(root==null)
            return 0;
        dfs(root,0);
        return minDepth;
    }

    public void dfs(TreeNode root,int depth)
    {
        // 设置终止条件
        if(root==null)
            return;
        // 中节点处理
        depth++;
        if(root.left==null&&root.right==null) // 判断是否为叶子节点
            minDepth=Math.min(minDepth,depth);
        // 左节点处理
        dfs(root.left,depth);
        // 右节点处理
        dfs(root.right,depth);
        depth--;
    }

}

// 后序遍历
class Solution {
    public int minDepth(TreeNode root) {
        if(root==null)
            return 0;
        // 处理左节点
        int leftLength=minDepth(root.left);
        // 处理右节点
        int rightLength=minDepth(root.right);
        // 处理中节点
        if(root.left==null)
            return rightLength+1;
        if(root.right==null)
            return leftLength+1;
        return Math.min(leftLength,rightLength)+1;
    }

}
```

