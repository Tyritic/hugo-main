---
date : '2025-02-12T09:41:35+08:00'
draft : false
title : '字符串操作'
image : ""
categories : ["leetcode算法题解"]
tags : ["基础算法"]
description : "字符串的基本操作和相关算法"
math : true
---

## 字符串反转操作

在算法题中，反转字符串通常作为题目的子操作进行。

反转操作通常使用左右指针进行处理，因为字符串和数组类似都是基于连续分布内存而设计。故可以设计两个指针，一个从字符串前面，一个从字符串后面，两个指针同时向中间移动，并交换元素。

### 代码模板

```java
void reverseString(vector<char>& s) {
    int l = 0;
    int r = s.length - 1;
    while(l < r){
     	char temp = s[l];
        s[l] = s[r];
        s[r] = temp;
        l++;
        r--;
    }
}

// 字符串长度为奇数时，left将会等于right，并位于数组下标为n/2的位置上
// 字符串长度为偶数时，left将会大于right，其中left位于数组下标为n/2，right位于数组下标为n/2-1
```



### 经典例题

#### leetcode 304 反转字符串

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/reverse-string/)

编写一个函数，其作用是将输入的字符串反转过来。输入字符串以字符数组 char[] 的形式给出。

不要给另外的数组分配额外的空间，你必须原地修改输入数组、使用 O(1) 的额外空间解决这一问题。

你可以假设数组中的所有字符都是 ASCII 码表中的可打印字符。

示例 1：
输入：["h","e","l","l","o"]
输出：["o","l","l","e","h"]

示例 2：
输入：["H","a","n","n","a","h"]
输出：["h","a","n","n","a","H"]

**思路解析**

代码模板题，直接套用模板即可

**参考代码**

```java
class Solution {
    public void reverseString(char[] s) {
        int left=0;
        int right=s.length-1;
        while(left<right)
        {
            char temp=s[right];
            s[right]=s[left];
            s[left]=temp;
            left++;
            right--;
        }
    }
}
```

#### leetcode 541 反转字符串II

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/reverse-string-ii/)

给定一个字符串 s 和一个整数 k，从字符串开头算起, 每计数至 2k 个字符，就反转这 2k 个字符中的前 k 个字符。

如果剩余字符少于 k 个，则将剩余字符全部反转。

如果剩余字符小于 2k 但大于或等于 k 个，则反转前 k 个字符，其余字符保持原样。

示例:

输入: s = "abcdefg", k = 2
输出: "bacdfeg"

**思路解析**

可以在for循环中将 **`2k`** 作为步长，判断是否需要有反转的区间。

**参考代码**

```java
class Solution {
    public String reverseStr(String s, int k) {
        char[]str=s.toCharArray();
        for(int i=0;i<s.length();i+=2*k)
        {
            // 定位起始位置和终止位置
            int start=i;
            int end=Math.min(start+k-1,str.length-1);
            // 反转操作
            while(start<end)
            {
                char temp=str[start];
                str[start]=str[end];
                str[end]=temp;
                start++;
                end--;
            }
        }
        return new String(str);
    }
}
```

#### leetcode 151 反转字符串中的单词

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/reverse-words-in-a-string/)

给定一个字符串，逐个翻转字符串中的每个单词。

示例 1：
输入: "the sky is blue"
输出: "blue is sky the"

示例 2：
输入: "  hello world!  "
输出: "world! hello"
解释: 输入字符串可以在前面或者后面包含多余的空格，但是反转后的字符不能包括。

示例 3：
输入: "a good  example"
输出: "example good a"
解释: 如果两个单词间有多余的空格，将反转后单词间的空格减少到只含一个。

**思路解析**

从示例的单词位置可以看出字符串应当进行了一次整体反转。于是考虑先对字符串做一次整体反转

源字符串为："the sky is blue "

整体反转后为：" eulb si yks eht"

对比示例可知，再将每个单词进行反转即可

反转每个单词后为：" blue is sky the"

发现有多余空格则还要考虑去除多余空格

故总体思路总结如下

- 源字符串："the sky is blue "
- 先去除多余的空格："the sky is blue"
- 字符串反转："eulb si yks eht"
- 单词反转："blue is sky the"

去除空格的思路可以参考 [leetcode 27 移除元素](https://leetcode.cn/problems/remove-element/)

使用快慢指针法

- 当快指针遍历到非空格时
  - 若慢指针不指向第一个位置则将慢指针位置置为空格，并右移慢指针
  - 进行单个单词的遍历

**参考代码**

```java
class Solution {
    public String reverseWords(String s) {
        char[]str= removeSpace(s);
        reverse(str,0,str.length-1);
        reverseEachWord(str);
        return new String(str);

    }
    // 去除多余空格,利用快慢指针的思路
    public static char[] removeSpace(String s)
    {
        int slow=0;
        char[]str=s.toCharArray();
        for(int fast=0;fast<str.length;fast++)
        {
            if(str[fast]!=' ')
            {
                // 去除在第一个单词前加入空格，同时在每个单词前加入空格
                if(slow>0)
                {
                    str[slow++]=' ';
                }
                // 获取每个单词，每个单词遍历结束后slow位于一个空格中
                while(fast<str.length&&str[fast]!=' ')
                {
                    str[slow++]=str[fast++];
                }
            }
        }
        return Arrays.copyOf(str,slow);
    }
    public static void reverse(char[] chars, int left, int right) {
        while(left<right)
        {
            char temp=chars[left];
            chars[left]=chars[right];
            chars[right]=temp;
            left++;
            right--;
        }
    }

    public void reverseEachWord(char[] chars) {
        int start=0;
        for(int end=0;end<=chars.length;end++)
        {
            if(end==chars.length||chars[end]==' ')
            {
                reverse(chars,start,end-1);
                start=end+1;
            }
        }
    }

}
```



#### 右旋字符串

[卡码网题目链接(opens new window)](https://kamacoder.com/problempage.php?pid=1065)

字符串的右旋转操作是把字符串尾部的若干个字符转移到字符串的前面。给定一个字符串 s 和一个正整数 k，请编写一个函数，将字符串中的后面 k 个字符移到字符串的前面，实现字符串的右旋转操作。

例如，对于输入字符串 "abcdefg" 和整数 2，函数应该将其转换为 "fgabcde"。

输入：输入共包含两行，第一行为一个正整数 k，代表右旋转的位数。第二行为字符串 s，代表需要旋转的字符串。

输出：输出共一行，为进行了右旋转操作后的字符串。

样例输入：

```text
2
abcdefg 
```

1
2

样例输出：

```text
fgabcde
```

1

数据范围：1 <= k < 10000, 1 <= s.length < 10000;

**思路解析**

根据样例输出，可以发现整个字符串进行一次反转，然后将前k个字符反转，剩下的字符反转

**参考代码**

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int k = Integer.parseInt(scanner.nextLine());
        String s=scanner.nextLine();
        int start=0;
        char[]str=s.toCharArray();
        int end=s.length()-1;
        // 将整个字符串反转
        reverse(str,start,end);
        // 将前k个字符反转，下标范围为[start,start+k-1]
        reverse(str,start,start+k-1);
        // 将剩下的部分反转，下标范围为[start+k,end]
        reverse(str,start+k,end);
        System.out.println(str);
        
        
    }
    
    public static void reverse(char[] chars,int left,int right)
    {
        while (left < right) {
            char temp = chars[left];
            chars[left] = chars[right];
            chars[right] = temp;
            left++;
            right--;
        }
    }
}
```



## 字符串替换操作

### 思路解析

字符串可以被视为字符数组。**做法都是先预先给数组扩容带填充后的大小，然后在从后向前进行操作**

### 经典例题

#### 替换数字

[卡码网题目链接(opens new window)](https://kamacoder.com/problempage.php?pid=1064)

给定一个字符串 s，它包含小写字母和数字字符，请编写一个函数，将字符串中的字母字符保持不变，而将每个数字字符替换为number。

例如，对于输入字符串 "a1b2c3"，函数应该将其转换为 "anumberbnumbercnumber"。

对于输入字符串 "a5b"，函数应该将其转换为 "anumberb"

输入：一个字符串 s,s 仅包含小写字母和数字字符。

输出：打印一个新的字符串，其中每个数字字符都被替换为了number

样例输入：a1b2c3

样例输出：anumberbnumbercnumber

数据范围：1 <= s.length < 10000。

#### 参考代码

```java
public class Main {
    
    public static String replaceNumber(String s) {
        // 提取计算出数字的个数
        int count=0;
        int oldLength=s.length();
        for (int i = 0; i < s.length(); i++) {
            if(Character.isDigit(s.charAt(i))){
                count++;
            }
        }
        // 预先设置扩容后的大小
        char[]newS=new char[s.length()+5*count];
        int newLength=s.length()+5*count;
        System.arraycopy(s.toCharArray(), 0, newS, 0, oldLength);
        // 从后向前操作
        for(int i=newLength-1,j=oldLength-1;j<i;i--,j--)
        {
            // 判断是否为数字，不是数字则不做操作
            if(!Character.isDigit(newS[j])){
                newS[i]=newS[j];
            }
            // 填充操作
            else{
                newS[i] = 'r';
                newS[i - 1] = 'e';
                newS[i - 2] = 'b';
                newS[i - 3] = 'm';
                newS[i - 4] = 'u';
                newS[i - 5] = 'n';
                i -= 5;
            }
        }
        return new String(newS);
    }
    
    public static void main(String[]args){
        Scanner scanner = new Scanner(System.in);
        String s = scanner.next();
        System.out.println(replaceNumber(s));
        scanner.close();
    }
}
```



## 字符串匹配（KMP算法）

KMP的主要思想是 **当出现字符串不匹配时，可以知道一部分之前已经匹配的文本内容，可以利用这些信息避免从头再去做匹配了。**

### 前缀表的作用

**前缀表是用来回退的，它记录了模式串与主串(文本串)不匹配的时候，模式串应该从哪里开始重新匹配。** 找到了最长相等的前后缀，匹配失败的位置是后缀子串的后面，那么找到与其相同的前缀的后面重新匹配就可以。**记录下标i之前（包括i）的字符串中，有多大长度的相同前缀后缀。**

### 最长公共前后缀

- **前缀是指不包含最后一个字符的所有以第一个字符开头的连续子串**。
- **后缀是指不包含第一个字符的所有以最后一个字符结尾的连续子串**。

计算方法

例如：模式串为”aabaaf"

- 字符串：a，最长公共前后缀长度为0
- 字符串：aa，最长公共前后缀长度为1
  - 前缀：a
  - 后缀：a
- 字符串：aab，最长公共前后缀长度为0
  - 前缀：a，aa
  - 后缀：b，ab
- 字符串：aaba，最长公共前后缀长度为1
  - 前缀：a，aa，aab
  - 后缀：a，ab，aba
- 字符串：aabaa，最长公共前后缀长度为2
  - 前缀：a，aa，aab，aaba
  - 后缀：a，aa，baa，abaa
- 字符串：aabaaf，最长公共前后缀长度为0
  - 前缀：a，aa，aab，aabaa
  - 后缀：f，af，aaf，baaf，abaaf

### 匹配过程

- 计算出模式串的前缀表
- 设置两个指针
  - 一个指针 **`i`** 指向文本串的起始位置，且永不回退
  - 一个指针 **`j`** 指向模式串的起始位置
- 文本串和模式串逐一匹配，遍历文本串
  - 对于匹配的字符，模式串指针 **`j`** 向右移动
  - 对于不匹配的字符，模式串指针回退前缀表的前一个位置 **`（next[j-1]）`**



### next数组的构造方法

prefix数组通常指代前缀表本身

next数组通常将前缀表prefix数组统一减一后使用，next[i] 表示 i（包括i）之前最长相等的前后缀长度（其实就是j）

构造方法

- 初始化
  - 定义两个指针i和j，j指向前缀末尾位置，i指向后缀末尾位置。
  - 对next数组进行初始化赋值
    - **`j=0`**
    - **`next[0]=0`**
- 遍历模式串
  - 处理前后缀不相同的情况
    - **`j`** 不断回退到next数组的前一个位置
  - 处理前后缀相同的情况
    - **`j`** 不断向右移动
  - 更新next数组

### 代码模板

```java
class Solution {
    public int strStr(String haystack, String needle) {
        if (needle.length() == 0) return 0;
        int[]next=new int[needle.length()];
        getNext(next,needle);

        //kmp匹配过程
        int j=0;//模式串的指针
        for(int i=0;i<haystack.length();i++)//文本串的指针
        {
            //遇到不匹配的
            while(j>0&&haystack.charAt(i)!=needle.charAt(j))
            {
                j=next[j-1];//j回退
            }
            if(needle.charAt(j)==haystack.charAt(i))
            {
                j++;
            }
            if(j==needle.length())//找到匹配子串
            {
                return i-needle.length()+1;
            }
        }
        return -1;
    }

    // next数组的获取
    public static void getNext(int[]next,String needle){
        //初始化
        int j=0;//前缀的末尾，最长相等前后缀的长度
        next[0]=0;
        //i为后缀的末尾
        for(int i=1;i<needle.length();i++)
        {
            //前后缀不匹配
            while(j>0&&needle.charAt(i)!=needle.charAt(j))
            {
                j=next[j-1];
            }
            //前后缀匹配
            if(needle.charAt(i)==needle.charAt(j))
            {
                j++;
            }
            next[i]=j;//更新next数组
        }
    }


}
```

### 经典例题

#### leetcode 28 找出字符串中第一个匹配项的下标

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/)

实现 strStr() 函数。

给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回 -1。

示例 1: 输入: haystack = "hello", needle = "ll" 输出: 2

示例 2: 输入: haystack = "aaaaa", needle = "bba" 输出: -1

说明: 当 needle 是空字符串时，我们应当返回什么值呢？这是一个在面试中很好的问题。 对于本题而言，当 needle 是空字符串时我们应当返回 0 。这与C语言的 strstr() 以及 Java的 indexOf() 定义相符。

**思路解析**

套用kmp算法模板即可

**参考代码**

```java
class Solution {
    public int strStr(String haystack, String needle) {
        if (needle.length() == 0) return 0;
        int[]next=new int[needle.length()];
        getNext(next,needle);

        //kmp匹配过程
        int j=0;//模式串的指针
        for(int i=0;i<haystack.length();i++)//文本串的指针
        {
            //遇到不匹配的
            while(j>0&&haystack.charAt(i)!=needle.charAt(j))
            {
                j=next[j-1];//j回退
            }
            if(needle.charAt(j)==haystack.charAt(i))
            {
                j++;
            }
            if(j==needle.length())//找到匹配子串
            {
                return i-needle.length()+1;
            }
        }
        return -1;
    }

    // next数组的获取
    public static void getNext(int[]next,String needle){
        //初始化
        int j=0;//前缀的末尾，最长相等前后缀的长度
        next[0]=0;
        //i为后缀的末尾
        for(int i=1;i<needle.length();i++)
        {
            //前后缀不匹配
            while(j>0&&needle.charAt(i)!=needle.charAt(j))
            {
                j=next[j-1];
            }
            //前后缀匹配
            if(needle.charAt(i)==needle.charAt(j))
            {
                j++;
            }
            next[i]=j;//更新next数组
        }
    }

}
```

#### leetcode 459 重复的子字符串

**题目描述**

[力扣题目链接(opens new window)](https://leetcode.cn/problems/repeated-substring-pattern/)

给定一个非空的字符串，判断它是否可以由它的一个子串重复多次构成。给定的字符串只含有小写英文字母，并且长度不超过10000。

示例 1:

- 输入: "abab"
- 输出: True
- 解释: 可由子字符串 "ab" 重复两次构成。

示例 2:

- 输入: "aba"
- 输出: False

示例 3:

- 输入: "abcabcabcabc"
- 输出: True
- 解释: 可由子字符串 "abc" 重复四次构成。 (或者子字符串 "abcabc" 重复两次构成。)

**思路解析**

重要结论：若 **`s`** 可以被其一个子串重复多次构成则 **`s+s去掉头尾字符的字符串`** 后出现子串 **`s`** 。于是可以使用kmp算法

**参考代码**

```java
class Solution {
    public boolean repeatedSubstringPattern(String s) {
        if(s.length()==1)return false;
        String str=(s+s).substring(1,(s+s).length()-1);
        return kmp(str,s);
    }
    // 求解next数组
    public static int[] getNext(String str)
    {
       int[]next=new int[str.length()];
       int j=0; //前缀的末尾（同时是前缀的长度）
       next[0]=0;
       // 后缀末尾
       for(int i=1;i<next.length;i++)
       {
           // 前后缀不相同
           while(j>0&&str.charAt(i)!=str.charAt(j))
               j=next[j-1]; // 回退
           // 前后缀相同
           if(str.charAt(i)==str.charAt(j))
               j++;
           // 更新next数组
           next[i]=j;
       }
       return next;
    }
    public static boolean kmp(String str1,String str2)
    {
        int[]next=getNext(str2);
        int j=0; //模式串指针
        for(int i=0;i<str1.length();i++)
        {
            // 前后缀不匹配
            while(j>0&&str1.charAt(i)!=str2.charAt(j))
                j=next[j-1];
            // 前后缀匹配
            if(str1.charAt(i)==str2.charAt(j))
                j++;
            if(j==str2.length())
            {
                return true;
            }
        }
        return false;
    }
}
```

## 字符串去除多余空格

### 问题描述

当字符串中需要去掉多余空格，同时保持正常英文语法中的单词空格

### 思路解析

这里的思路是去除掉字符串头和字符串尾部以及字符串中的多余空格。可以参考 [leetcode 27 移除元素的思路](https://leetcode.cn/problems/remove-element/) 使用快慢指针，快指针用于遍历原始字符串，慢指针用于确定真正需要的字符。

### 代码模板

```java
public static char[] removeSpace(String s)
    {
        int slow=0;
        char[]str=s.toCharArray();
        for(int fast=0;fast<str.length;fast++)
        {
            if(str[fast]!=' ')
            {
                // 去除在第一个单词前加入空格，同时在每个单词前加入空格
                if(slow>0)
                {
                    str[slow++]=' ';
                }
                // 获取每个单词，每个单词遍历结束后slow位于一个空格中
                while(fast<str.length&&str[fast]!=' ')
                {
                    str[slow++]=str[fast++];
                }
            }
        }
        return Arrays.copyOf(str,slow);
    }
```

## 回文串问题

### 思路解析

通常回文串问题可以通过两个思路解决

- 左右指针法
  - 设置一个左指针指向字符串开头，一个右指针指向字符串结尾，两个指针相向而行，直到相遇
- 反转字符串
  - 可以利用回文字符串反转后相等的属性

### 经典例题

#### leetcode 125 验证回文串

**题目描述**

如果在将所有大写字符转换为小写字符、并移除所有非字母数字字符之后，短语正着读和反着读都一样。则可以认为该短语是一个 **回文串** 。

字母和数字都属于字母数字字符。

给你一个字符串 `s`，如果它是 **回文串** ，返回 `true` ；否则，返回 `false` 。

 

**示例 1：**

```
输入: s = "A man, a plan, a canal: Panama"
输出：true
解释："amanaplanacanalpanama" 是回文串。
```

**示例 2：**

```
输入：s = "race a car"
输出：false
解释："raceacar" 不是回文串。
```

**示例 3：**

```
输入：s = " "
输出：true
解释：在移除非字母数字字符之后，s 是一个空字符串 "" 。
由于空字符串正着反着读都一样，所以是回文串。
```

**思路解析**

本题可以使用左右指针法，指针遇到非数字字母字符直接跳过。当左右指针所指的位置都是数字字母字符时进行比较，同时移动指针

**参考代码**

```java
class Solution {
    public boolean isPalindrome(String s) {
        int left=0;
        int right=s.length()-1;
        while(left<right)
        {
            while((left<right)&&!check(s.charAt(left)))
                left++;
            while((left<right)&&!check(s.charAt(right)))
                right--;
            if(check(s.charAt(left))&&check(s.charAt(right)))
            {
                if(Character.toLowerCase(s.charAt(left))!=Character.toLowerCase(s.charAt(right)))
                {
                    return false;
                }
                left++;
                right--;
            }
        }
        return true;

    }
    // 验证数字字母字符
    public boolean check(char s)
    {
        if(('a'<=s&&s<='z')||('A'<=s&&s<='Z')||('0'<=s&&s<='9'))
            return true;
        return false;
    }
}
```

## 字符串同构问题

### 问题描述

给定两个字符串 `s` 和 `t` ，判断它们是否是同构的。

如果 `s` 中的字符可以按某种映射关系替换得到 `t` ，那么这两个字符串是同构的。

每个出现的字符都应当映射到另一个字符，同时不改变字符的顺序。不同字符不能映射到同一个字符上，相同字符只能映射到同一个字符上，字符可以映射到自己本身。

### 思路解析

维护两张哈希表，一张哈希表以第一个字符串中字符为键，映射至第二个字符串的字符为值，第二张哈希表以第二个字符串中的字符为键，映射至第一个字符串的字符为值。从左至右遍历两个字符串的字符，不断更新两张哈希表，如果出现冲突时说明两个字符串无法构成同构，返回 false。

### 经典例题

#### leetcode 205 同构字符串

**题目描述**

给定两个字符串 `s` 和 `t` ，判断它们是否是同构的。

如果 `s` 中的字符可以按某种映射关系替换得到 `t` ，那么这两个字符串是同构的。

每个出现的字符都应当映射到另一个字符，同时不改变字符的顺序。不同字符不能映射到同一个字符上，相同字符只能映射到同一个字符上，字符可以映射到自己本身。

 

**示例 1:**

```
输入：s = "egg", t = "add"
输出：true
```

**示例 2：**

```
输入：s = "foo", t = "bar"
输出：false
```

**示例 3：**

```
输入：s = "paper", t = "title"
输出：true
```



**提示：**

- `1 <= s.length <= 5 * 104`
- `t.length == s.length`
- `s` 和 `t` 由任意有效的 ASCII 字符组成

**思路解析**

维护两张哈希表，第一张哈希表以 s 中字符为键，映射至 t 的字符为值，第二张哈希表以 t 中字符为键，映射至 s 的字符为值。从左至右遍历两个字符串的字符，不断更新两张哈希表，如果出现冲突时说明两个字符串无法构成同构，返回 false。

如果遍历结束没有出现冲突，则表明两个字符串是同构的，返回 true 即可。

**参考代码**

```java
class Solution {
    public boolean isIsomorphic(String s, String t) {
        HashMap<Character,Character>st=new HashMap<>();
        HashMap<Character,Character>ts=new HashMap<>();
        for(int i=0;i<s.length();i++)
        {
            char s_ch=s.charAt(i);
            char t_ch=t.charAt(i);
            if((st.containsKey(s_ch)&&st.get(s_ch)!=t_ch)||(ts.containsKey(t_ch)&&ts.get(t_ch)!=s_ch))
            {
                return false;
            }
            st.put(s_ch,t_ch);
            ts.put(t_ch,s_ch);
        }
        return true;
    }
}
```

#### leetcode 290 单词规律

**题目描述**

给定一种规律 `pattern` 和一个字符串 `s` ，判断 `s` 是否遵循相同的规律。

这里的 **遵循** 指完全匹配，例如， `pattern` 里的每个字母和字符串 `s` 中的每个非空单词之间存在着双向连接的对应规律。 

**示例1:**

```
输入: pattern = "abba", s = "dog cat cat dog"
输出: true
```

**示例 2:**

```
输入:pattern = "abba", s = "dog cat cat fish"
输出: false
```

**示例 3:**

```
输入: pattern = "aaaa", s = "dog cat cat dog"
输出: false
```

**参考代码**

```java
class Solution {
    public boolean wordPattern(String pattern, String s) {
        HashMap<Character,String>ps=new HashMap<>();
        HashMap<String,Character>sp=new HashMap<>();
        // 记录每个单词的起始位置
        int index=0;
        for(int i=0;i<pattern.length();i++)
        {
            char p_ch=pattern.charAt(i);
            // 针对单个单词
            if (index >= s.length()) {
                return false;
            }
            int j=index;
            while(j<s.length()&&s.charAt(j)!=' ')
            {
                j++;
            }
            // 截取单词
            String s_string=s.substring(index,j);
            if((ps.containsKey(p_ch)&&!ps.get(p_ch).equals(s_string))||(sp.containsKey(s_string)&&sp.get(s_string)!=p_ch))
            {
                return false;
            }
            ps.put(p_ch,s_string);
            sp.put(s_string,p_ch);
            index=j+1;
        }
        System.out.println(index);
        return index>=s.length();
    }
}
```

