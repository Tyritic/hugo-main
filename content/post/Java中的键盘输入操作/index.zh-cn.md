---
date : '2024-11-03T12:09:48+08:00'
draft : false
title : 'Java中的标准输入操作'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记的转换"
math : true
---

## Scanner类

java.utils包中用于获取输入的类，用于解析基本类型和字符串类型的输入。它可以从控制台、文件、字符串等不同的数据源读取数据，并将其解析为适当的类型。

## 基本构造函数

`Scanner`可以接收控制台的键盘输入（标准输入流），文件和字符串

- 从控制台输入读取

  ```java
  Scanner scanner = new Scanner(System.in);
  ```

- 从文件输入读取

  ```java
  File file = new File("input.txt");
  Scanner scanner = new Scanner(file);
  ```

- 从字符串中读取

  ```java
  String input = "Hello World!";
  Scanner scanner = new Scanner(input);
  ```

  

## 基本用法

### 读取基本类型

- `nextInt()`：读取int类型
- `nextShort()`：读取short类型
- `nextLong()`：读取long类型
- `nextFloat()`：读取float类型
- `nextDouble()`：读取double类型

### 读取字符串

- **`next()`** ：读取下一个字符串，遇到空白符（如空格、制表符、换行符等）停止
- **`nextLine()`**：读取下一行文本，遇到回车停止

{{<notice tip>}}

**`next()`** 和 **`nextLine()`** 的区别

**`next()`**

- 一定要读取到有效字符后才可以结束输入。
- 对输入有效字符之前遇到的空白，**`next()`** 方法会自动将其去掉。
- 只有输入有效字符后才将其后面输入的空白作为分隔符或者结束符。
- **`next()`** 不能得到带有空格的字符串。

**`nextLine()`**

1. 以Enter为结束符,也就是说 **`nextLine()`** 方法返回的是输入回车之前的所有字符。
2. 可以获得空白。

先使用 **`nextLine()`** 再使用 **`next()、nextInt()`** 等没问题，但是先使用 **`next()`** 和 **`nextInt()`** 等之后就不可以再紧跟 **`nextLine()`** 使用。

原因：因为 **`next()`** 等这些方法读取结束后会紧跟一个回车符，而 **`nextLine()`** 会直接读取到这个回车符，这就导致出现我们还没有来得及输入我们想要输入的数据，**`nextLine()`** 就以为我们已经输入完了

解决方法：我们直接在 **`next()`** 使用后加两个 **`nextLine()`** 即可了，这样第一个 **`nextLine()`** 就会当一个‘替死鬼’读取前一个 **`next()`** 遗留的空白符，第二个 **`nextLine()`** 就可以输入自己想要输入的数据啦！

{{</notice>}}

### 检验输入

- `hasNext()`方法会检查输入中是否还有下一个单词，即是否存在非空白字符。这意味着，只要输入中还有非空白字符，无论是在当前行还是在下一行，`hasNext()`都会返回true。通常配合 **`next()`** 使用
- `hasNextLine()`方法则会检查输入中是否还有下一行。如果输入中存在换行符，或者如果输入中至少还有一个字符（即使这个字符是空白字符），`hasNextLine()`都会返回true。但是如果输入已经到达结尾，或者输入中的下一个字符是输入流的结尾，`hasNextLine()`就会返回阻塞。

## 设置分隔符

`Scanner`类默认使用空白字符（空格、制表符、换行符等）作为分隔符，但可以自定义分隔符。

`delimiter()`用于查看当前分隔符

`useDelimiter()`方法用于修改分隔符

### 示例代码

```java
Scanner scanner = new Scanner(System.in);
scanner.useDelimiter(","); // 使用逗号作为分隔符
System.out.print("Enter comma-separated values: ");
while (scanner.hasNext()) {
    String value = scanner.next();
    System.out.println("Value: " + value);
}
```



## 关闭扫描器

使用完Scanner后，一定要记得将它关闭！因为使用Scanner本质上是打开了一个IO流，如果不关闭的话，它将会一直占用系统资源。

`close()`方法