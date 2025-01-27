---
date : '2024-11-03T00:27:14+08:00'
draft : false
title : 'Java数组'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记的转换"
math : true
---

## 一维数组的声明与创建

### 声明数组

```java
ElementType[] array_name; // 一维数组
ElementType[][] array_name; // 二维数组
```

### 创建数组

 除非数组被创建否则不能分配任何元素

```java
array_name=new ElementType[size];
```

### 初始化数组

#### 静态初始化

指定数组内的元素而不指定数组的长度

```java
ElementType array_name={x1,x2,..xn};
```

#### 动态初始化

指定数组的长度而不指定数组的元素，系统自动赋默认值

```java
ElementType[]array_name=new ElementType[size];
```



## 获取一维数组长度

```java
int length=array_name.length;
```

## 访问一维数组元素

通过数组下标访问，数组下标从0开始

## 数组元素的默认值

- 整型：0
- 浮点型：0.0
- 布尔：false
- 字符：’\u000'
- 字符串：null
- 引用数据类型：null

## 一维数组的处理

### 遍历数组

不通过数组下标可以完成数组的遍历

```java
for(数据类型 引用名:数组名)
{
	// 循环体
}
```

### 复制数组

- 使用`for`循环/`for-each`循环逐一复制元素

- 使用`system`类中的静态方法`arraycopy`复制数组

  ```java
  System.arraycopy(sourceArray,srcPos,targetArray,tarPos,length);
  // srcPos：源数组中的起始位置
  // tarPos：目标数组的起始位置
  // length：决定复制数组的元素个数
  ```

  

  {{<notice tip>}}

  数组的复制不能简单使用赋值号，赋值号只是将引用的地址值赋值，此时两个变量指向同一个数组

  {{</notice>}}

## 可变长参数列表

可以将类型相同但是数目可变的参数作为方法的形参

### 语法形式

```java
TypeName... parameterName
```



### 示例代码

```java
// 定义一个带有可变参数的方法
    public static void printAll(String... strings) {
        for (String s : strings) {
            System.out.println(s);
        }
    }

```



### 注意事项

- 可变参数必须是方法参数列表中的最后一个参数。
- 一个方法只能有一个可变参数。
- 当你调用一个带有可变参数的方法时，你可以直接传入逗号分隔的参数列表，也可以传入一个数组（数组会自动被拆分成单独的参数）。
- 在调用方法时同时传入了一个数组和一个或多个单独的参数，那么数组必须被明确地作为最后一个参数传入（即它不能被单独的可变参数分隔开）

## 二维数组的声明和创建

### 初始化二维数组

#### 静态初始化

```java
ElementType[][]array_name=new ElementType[][]{{var1,var2,..varN},{var1,var2,..varN}};
```

#### 动态初始化

```java
ElementType[][]array_name=new ElementType[m][n];
```

- `m`表示这个二维数组存放了多少个一维数组
- `n`表示这个一维数组存放多少个元素

## 二维数组的存储方式

二维数组本质上是一个一维数组，这个一维数组的存储元素是其他一维数组的地址值

例如

```java
int[][]arr={{11,22},{33,44}};
```

其中`arr`的地址为`0x0011`

`arr`的元素为

`arr[0]`为`0x0022`（对应`arr[0][]`)

`arr[1]`为`0x0033`(对应`arr[1][]`)

## 访问二维数组元素

```java
array_name[m][n];
```

- m索引指定访问哪个一维数组
- n索引指定访问这个一维数组的哪个元素

## 获取二维数组的长度

对应二维数组`array_name[m][n]`

- 通过`array_name.length`获取二维数组中包含多少个一维数组
- 通过`array_name[0].length`获取一维数组的长度