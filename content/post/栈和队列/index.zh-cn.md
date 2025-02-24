---
date : '2025-02-13T10:41:58+08:00'
draft : false
title : '栈和队列'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "栈和队列在算法题中的常见问题"
math : true
---

## 栈和队列的相互转换

### 用栈实现队列

#### 思路解析

使用栈来模拟队列的行为，所以需要两个栈 **一个输入栈，一个输出栈** 。

**`offer`** 操作时直接将数据 **`push`** 到输入栈中

**`poll`** 操作时若输出栈不为空则先将输入栈中数据依次出栈并放入输出栈中（这会让输入栈中的数据倒序存储在输出栈中）然后直接出栈



#### leetcode 232 用栈实现队列

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/implement-queue-using-stacks/)

使用栈实现队列的下列操作：

push(x) -- 将一个元素放入队列的尾部。
pop() -- 从队列首部移除元素。
peek() -- 返回队列首部的元素。
empty() -- 返回队列是否为空。

示例:

```cpp
MyQueue queue = new MyQueue();
queue.push(1);
queue.push(2);
queue.peek();  // 返回 1
queue.pop();   // 返回 1
queue.empty(); // 返回 false
```



说明:

- 你只能使用标准的栈操作 -- 也就是只有 push to top, peek/pop from top, size, 和 is empty 操作是合法的。
- 你所使用的语言也许不支持栈。你可以使用 list 或者 deque（双端队列）来模拟一个栈，只要是标准的栈操作即可。
- 假设所有操作都是有效的 （例如，一个空的队列不会调用 pop 或者 peek 操作）。

**参考代码**

```java
class MyQueue {
    Stack<Integer>stackIn;
    Stack<Integer>stackOut;
    public MyQueue() {
        stackIn=new Stack<>();
        stackOut=new Stack<>();
    }
    
    // push 操作直接放入输入栈
    public void push(int x) {
        stackIn.push(x);
    }
    
    // pop 操作先转移元素到输出栈再弹出元素
    public int pop() {
        transfer();
        return stackOut.pop();
    }
    
    public int peek() {
        transfer();
        return stackOut.peek();
    }
    
    public boolean empty() {
        return stackIn.isEmpty()&& stackOut.empty();
    }

    // 将输入栈的元素转移到输出栈中
    public void transfer(){
        if (!stackOut.isEmpty()) return;
        while(!stackIn.isEmpty())
        {
            stackOut.push(stackIn.pop());
        }
    }
}
```

### 用队列实现栈

#### 思路解析

用队列实现栈可以使用一个队列或者两个队列实现

**两个队列的思路**

设置两个队列，一个队列为主队列，另一个队列为辅助队列。

- **`push`** 操作时先将元素添加到辅助队列中，然后将主队列的元素依次出队加入辅助队列，最后辅助队列和主队列互相交换
- **`pop`** 操作直接让主队列出队即可

**一个队列的思路**

- **`push`** 操作时保证元素每次都添加到队首
  - 先进行 **`offer`** 操作
  - 将除新元素以外的元素依次出队再入队
- **`poll`** 操作时直接出队即可

#### leetcode 225 用队列实现栈

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/implement-stack-using-queues/)

使用队列实现栈的下列操作：

- push(x) -- 元素 x 入栈
- pop() -- 移除栈顶元素
- top() -- 获取栈顶元素
- empty() -- 返回栈是否为空

注意:

- 你只能使用队列的基本操作-- 也就是 push to back, peek/pop from front, size, 和 is empty 这些操作是合法的。
- 你所使用的语言也许不支持队列。 你可以使用 list 或者 deque（双端队列）来模拟一个队列 , 只要是标准的队列操作即可。
- 你可以假设所有操作都是有效的（例如, 对一个空的栈不会调用 pop 或者 top 操作）。

**参考代码**

- 两个队列实现

  ```java
  class MyStack {
      Queue<Integer>que1;
      Queue<Integer>que2;
      public MyStack() {
          que1=new ArrayDeque<>();
          que2=new ArrayDeque<>();
      }
      
      public void push(int x) {
          que2.offer(x);
          while(!que1.isEmpty())
          {
              que2.offer(que1.poll());
          }
          Queue<Integer> queueTemp;
          queueTemp = que1;
          que1 = que2;
          que2 = queueTemp;
      }
      
      public int pop() {
          return que1.poll();
      }
      
      public int top() {
          return que1.peek();
      }
      
      public boolean empty() {
          return que1.isEmpty()&&que2.isEmpty();
      }
  }
  ```

  

- 单个队列实现

  ```java
  class MyStack {
      Queue<Integer>que;
      public MyStack() {
          que=new ArrayDeque<>();
      }
      
      public void push(int x) {
          que.offer(x);
          int size=que.size();
          while(size>1)
          {
              que.offer(que.poll());
              size--;
          }
      }
      
      public int pop() {
          return que.poll();
      }
      
      public int top() {
          return que.peek();
      }
      
      public boolean empty() {
          return que.isEmpty();
      }
  }
  ```

  

## 括号匹配问题

### 思路解析

在编译原理中的括号匹配就是使用栈来解决的，因此可以在读取左括号时将对应的右括号入栈

分析不匹配的情况

- 左括号多余
- 左右括号不匹配
- 右括号多余

在栈中的情况如下

- 已经遍历完了字符串，但是栈不为空，说明有相应的左括号没有右括号来匹配
- 遍历字符串匹配的过程中，发现栈里没有可以匹配的字符
- 遍历字符串匹配的过程中，栈已经为空了，没有匹配的字符

### leetcode 20 有效的括号

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/valid-parentheses/)

给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。

有效字符串需满足：

- 左括号必须用相同类型的右括号闭合。
- 左括号必须以正确的顺序闭合。
- 注意空字符串可被认为是有效字符串。

示例 1:

- 输入: "()"
- 输出: true

示例 2:

- 输入: "()[]{}"
- 输出: true

示例 3:

- 输入: "(]"
- 输出: false

示例 4:

- 输入: "([)]"
- 输出: false

示例 5:

- 输入: "{[]}"
- 输出: true

#### 参考代码

```java
class Solution {
    public boolean isValid(String s) {
        Stack<Character>stack=new Stack<>();
        for(char ch:s.toCharArray())
        {
            // 检索到左括号将对应的右括号入栈
            if(ch=='(') {
                stack.push(')');
            }
            else if(ch=='{'){
                stack.push('}');
            }
            else if(ch=='['){
                stack.push(']');
            }
            // 1.栈在遍历过程中为空说明右括号多余
            // 2.栈在遍历过程中不对应说明左右括号不匹配
            else if(stack.isEmpty()||ch!=stack.peek())
                return false;
            else
                stack.pop();
        }
        // 3.栈在遍历后不为空说明左括号多余
        return stack.isEmpty();
    }
}
```

### leetcode 1021 删除最外层的括号

#### 题目描述

[题目链接](https://leetcode.cn/problems/remove-outermost-parentheses/description/)

有效括号字符串为空 `""`、`"(" + A + ")"` 或 `A + B` ，其中 `A` 和 `B` 都是有效的括号字符串，`+` 代表字符串的连接。

- 例如，`""`，`"()"`，`"(())()"` 和 `"(()(()))"` 都是有效的括号字符串。

如果有效字符串 `s` 非空，且不存在将其拆分为 `s = A + B` 的方法，我们称其为**原语（primitive）**，其中 `A` 和 `B` 都是非空有效括号字符串。

给出一个非空有效字符串 `s`，考虑将其进行原语化分解，使得：`s = P_1 + P_2 + ... + P_k`，其中 `P_i` 是有效括号字符串原语。

对 `s` 进行原语化分解，删除分解中每个原语字符串的最外层括号，返回 `s` 。

 

**示例 1：**

```
输入：s = "(()())(())"
输出："()()()"
解释：
输入字符串为 "(()())(())"，原语化分解得到 "(()())" + "(())"，
删除每个部分中的最外层括号后得到 "()()" + "()" = "()()()"。
```

**示例 2：**

```
输入：s = "(()())(())(()(()))"
输出："()()()()(())"
解释：
输入字符串为 "(()())(())(()(()))"，原语化分解得到 "(()())" + "(())" + "(()(()))"，
删除每个部分中的最外层括号后得到 "()()" + "()" + "()(())" = "()()()()(())"。
```

**示例 3：**

```
输入：s = "()()"
输出：""
解释：
输入字符串为 "()()"，原语化分解得到 "()" + "()"，
删除每个部分中的最外层括号后得到 "" + "" = ""。
```

#### 思路解析

用一个栈来表示括号的深度。遇到 ‘(’ 则将字符入栈，遇到 ‘)’ 则将栈顶字符出栈。栈从空到下一次空的过程，则是扫描了一个原语的过程。

#### 参考代码

```java
class Solution {
    public String removeOuterParentheses(String s) {
        Deque<Character>stack=new LinkedList<>();
        StringBuffer sb=new StringBuffer();
        for(int i=0;i<s.length();i++)
        {
            char ch=s.charAt(i);
            if(ch==')')
                stack.pop();
            if(!stack.isEmpty())
            {
                sb.append(ch);
            }
            if(ch=='(')
            {
                stack.push(ch);
            }
            System.out.println(sb);
            System.out.println("stack:"+stack.toString());
        }
        return sb.toString();
    }
}
```



## 字符串相邻重复项问题

### 思路解析

在删除相邻重复项的时候，其实就是要知道当前遍历的这个元素，我们在前一位是不是遍历过一样数值的元素。因为栈具有先进先出的特性可以快速得到前一位的元素，因此可以用栈来存放元素。当遍历当前的这个元素的时候，去栈里看一下我们是不是遍历过相同数值的相邻元素。然后再去做对应的消除操作

### leetcode 1047 删除字符串中所有相邻重复项

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string/)

给出由小写字母组成的字符串 S，重复项删除操作会选择两个相邻且相同的字母，并删除它们。

在 S 上反复执行重复项删除操作，直到无法继续删除。

在完成所有重复项删除操作后返回最终的字符串。答案保证唯一。

示例：

- 输入："abbaca"
- 输出："ca"
- 解释：例如，在 "abbaca" 中，我们可以删除 "bb" 由于两字母相邻且相同，这是此时唯一可以执行删除操作的重复项。之后我们得到字符串 "aaca"，其中又只有 "aa" 可以执行重复项删除操作，所以最后的字符串为 "ca"。

提示：

- 1 <= S.length <= 20000
- S 仅由小写英文字母组成。

#### 参考代码

```java
class Solution {
    public String removeDuplicates(String s) {
        Stack<Character>stack=new Stack<>();
        for(Character ch:s.toCharArray())
        {
            if(!stack.isEmpty()&&ch==stack.peek())
                stack.pop();
            else
                stack.push(ch);
        }
        StringBuffer str=new StringBuffer();
        while(!stack.isEmpty())
        {
            str.append(stack.pop());
        }
        return str.reverse().toString();
    }
}
```

## 逆波兰表达式求值

### 思路解析

在离散数学中，对逆波兰表达式的求解就是使用栈进行存储。遍历字符串，将数字直接存入栈中，如果遇到运算符则连续出栈两次作为运算符的运算数。注意除法和减法是后出栈的运算先出栈的

### leetcode 150 逆波兰式求值

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/evaluate-reverse-polish-notation/)

根据 逆波兰表示法，求表达式的值。

有效的运算符包括 + , - , * , / 。每个运算对象可以是整数，也可以是另一个逆波兰表达式。

说明：

整数除法只保留整数部分。 给定逆波兰表达式总是有效的。换句话说，表达式总会得出有效数值且不存在除数为 0 的情况。

示例 1：

- 输入: ["2", "1", "+", "3", " * "]
- 输出: 9
- 解释: 该算式转化为常见的中缀算术表达式为：((2 + 1) * 3) = 9

示例 2：

- 输入: ["4", "13", "5", "/", "+"]
- 输出: 6
- 解释: 该算式转化为常见的中缀算术表达式为：(4 + (13 / 5)) = 6

示例 3：

- 输入: ["10", "6", "9", "3", "+", "-11", " * ", "/", " * ", "17", "+", "5", "+"]

- 输出: 22

- 解释:该算式转化为常见的中缀算术表达式为：

  ```text
  ((10 * (6 / ((9 + 3) * -11))) + 17) + 5       
  = ((10 * (6 / (12 * -11))) + 17) + 5       
  = ((10 * (6 / -132)) + 17) + 5     
  = ((10 * 0) + 17) + 5     
  = (0 + 17) + 5    
  = 17 + 5    
  = 22    
  ```

#### 参考代码

```java
class Solution {
    public int evalRPN(String[] tokens) {
        Stack<Integer>stack=new Stack<>();
        for(String str:tokens)
        {
            if(str.equals("+"))
            {
                int x=stack.pop();
                int y=stack.pop();
                stack.push(x+y);
            }
            else if(str.equals("*"))
            {
                int x=stack.pop();
                int y=stack.pop();
                stack.push(x*y);
            }
            else if(str.equals("/"))
            {
                int x=stack.pop();
                int y=stack.pop();
                stack.push(y/x);
            }
            else if(str.equals("-"))
            {
                int x=stack.pop();
                int y=stack.pop();
                stack.push(y-x);
            }
            else {
                stack.push(Integer.valueOf(str));
            }
        }
        return stack.pop();
    }
}
```

## 单调队列问题

单调队列通常用于解决 **区间最值问题** 。

单调队列具有以下特点

- 队列中的元素 **从前到后单调** ，保证队头的元素是最值

单调队列要根据具体的场景自行设计

- pop(value)：如果窗口移除的元素value等于单调队列的出口元素，那么队列弹出元素，否则不用任何操作
- push(value)：如果push的元素value大于入口元素的数值，那么就将队列入口的元素弹出，直到push元素的数值小于等于队列入口元素的数值为止

### leetcode 239 滑动窗口最大值

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/sliding-window-maximum/)

给定一个数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。

返回滑动窗口中的最大值。

进阶：

你能在线性时间复杂度内解决此题吗？

![img](https://code-thinking.cdn.bcebos.com/pics/239.%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%E6%9C%80%E5%A4%A7%E5%80%BC.png)

提示：

- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- 1 <= k <= nums.length

#### 思路解析

本题是区间最值问题，可以维护一个单调队列，队列内单调递减，队头为队列的最大值。窗口移动时队头的最大值出队，队尾入队，入队前先将队列中所有比入队元素小的元素出队。

#### 参考代码

```java
class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        if (nums.length == 1) {
            return nums;
        }
        int num=0;
        int len = nums.length - k + 1;
        //存放结果元素的数组
        int[] res = new int[len];
        MyQueue que=new MyQueue();
        for(int i=0;i<k;i++)
        {
            que.push(nums[i]);
        }
        res[num++] = que.peek();
        for(int i=k;i<nums.length;i++)
        {
            que.poll(nums[i-k]);
            que.push(nums[i]);
            res[num++]= que.peek();
        }
        return res;
    }
}

class MyQueue{
    Deque<Integer>deq=new LinkedList<>();
    void poll(int val){
        if(!deq.isEmpty()&&val==deq.peek())
            deq.poll();
    }
    void push(int val)
    {
        while (!deq.isEmpty() && val > deq.getLast()) {
            deq.removeLast();
        }
        deq.add(val);
    }
    int peek()
    {
        return deq.peek();
    }
}
```

## 前K个的最值问题

### 题目描述

通常在数据结构中堆（优先队列）适合处理前k个的最值问题。维护一个优先队列，将元素依次入队，元素在队列中进行堆排序，再依次出队

### leetcode 347 前k个高频元素

#### 题目描述

[力扣题目链接(opens new window)](https://leetcode.cn/problems/top-k-frequent-elements/)

给定一个非空的整数数组，返回其中出现频率前 k 高的元素。

示例 1:

- 输入: nums = [1,1,1,2,2,3], k = 2
- 输出: [1,2]

示例 2:

- 输入: nums = [1], k = 1
- 输出: [1]

提示：

- 你可以假设给定的 k 总是合理的，且 1 ≤ k ≤ 数组中不相同的元素的个数。
- 你的算法的时间复杂度必须优于 $O(n \log n)$ , n 是数组的大小。
- 题目数据保证答案唯一，换句话说，数组中前 k 个高频元素的集合是唯一的。
- 你可以按任意顺序返回答案。

#### 思路解析

本题是经典的前k个最值问题，故想到使用优先队列实现。题目要求统计元素的出现频率，故需要使用map建立元素和出现次数之间的映射关系

为了在队列中体现键值对可以将队列中的元素设置为长度为2的数字，第一个元素代表键，第二个元素代表值

#### 参考代码

```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        // 统计元素出现次数
        HashMap<Integer,Integer>map=new HashMap<>();
        for(Integer i:nums)
        {
            map.put(i,map.getOrDefault(i,0)+1);
        }
        int[]res=new int[k];
        // 优先队列中按照出现频率降序排列
        PriorityQueue<int[]>que=new PriorityQueue<>((int[] o1, int[] o2)-> {
                return o2[1]-o1[1];
            }
        );
        // 元素依次入队
        for(Integer i:map.keySet())
        {
            que.add(new int[]{i,map.get(i)});
        }
        for(int i=0;i<k;i++)
        {
            res[i]=que.poll()[0];
        }
        return res;
    }
}
```

### **BM48** **数据流中的中位数**

#### 题目描述

[题目链接](https://www.nowcoder.com/share/jump/1895918791740295185624)

如何得到一个数据流中的中位数？如果从数据流中读出奇数个数值，那么中位数就是所有数值排序之后位于中间的数值。如果从数据流中读出偶数个数值，那么中位数就是所有数值排序之后中间两个数的平均值。我们使用Insert()方法读取数据流，使用GetMedian()方法获取当前读取数据的中位数。

数据范围：数据流中数个数满足 1≤n≤1000 1≤*n*≤1000 ，大小满足 1≤val≤1000 1≤*v**a**l*≤1000 

进阶： 空间复杂度 O(n) *O*(*n*) ， 时间复杂度 O(nlogn) *O*(*n**l**o**g**n*) 

示例1

输入：

```
[5,2,3,4,1,6,7,0,8]
```

返回值：

```
"5.00 3.50 3.00 3.50 3.00 3.50 4.00 3.50 4.00 "
```

说明：

```
数据流里面不断吐出的是5,2,3...,则得到的平均数分别为5,(5+2)/2,3...   
```

示例2

输入：

```
[1,1,1]
```

返回值：

```
"1.00 1.00 1.00 "
```

#### 思路解析

中位数的特征，它是数组中间个数字或者两个数字的均值，它是数组较小的一半元素中最大的一个，同时也是数组较大的一半元素中最小的一个。那我们只要每次维护最小的一半元素和最大的一半元素，并能快速得到它们的最大值和最小值，那不就可以了嘛。这时候就可以想到了堆排序的优先队列。

- step 1：我们可以维护两个堆，分别是大顶堆min，用于存储较小的值，其中顶部最大；小顶堆max，用于存储较大的值，其中顶部最小，则中位数只会在两个堆的堆顶出现。
- step 2：我们可以约定奇数个元素时取大顶堆的顶部值，偶数个元素时取两堆顶的平均值，则可以发现两个堆的数据长度要么是相等的，要么奇数时大顶堆会多一个。
- step 3：每次输入的数据流先进入大顶堆排序，然后将小顶堆的最大值弹入大顶堆中，完成整个的排序。
- step 4：但是因为大顶堆的数据不可能会比小顶堆少一个，因此需要再比较二者的长度，若是小顶堆长度小于大顶堆，需要从大顶堆中弹出最小值到大顶堆中进行平衡。

#### 参考代码

```java
public class Solution {
    // 小顶堆
    PriorityQueue<Integer>max_que = new PriorityQueue<>();
    // 大顶堆
    PriorityQueue<Integer>min_que = new PriorityQueue<>(new Comparator<Integer>() {
        @Override
        public int compare(Integer o1, Integer o2) {
            return o2 - o1;
        }
    });
    public void Insert(Integer num) {
        min_que.offer(num);
        max_que.offer(min_que.poll());
        if (min_que.size() < max_que.size()) {
            min_que.offer(max_que.poll());
        }
    }

    public Double GetMedian() {
        // 奇数个
        if (min_que.size() > max_que.size())
            return (double)min_que.peek();
        else {
            return (double)(min_que.peek() + max_que.peek()) / 2;
        }
    }


}
```

