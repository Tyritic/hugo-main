---
date : '2024-11-19T16:32:57+08:00'
draft : false
title : 'Java中的IO流'
image : ""
categories : ["互联网面试题","Java基础"]
tags : ["JavaSE"]
description : "Java中的IO流"
math : true
---

## IO流的定义

Java 的 I/O（输入/输出）流是用于处理输入和输出数据的类库。通过流，程序可以从各种输入源（如文件、网络）读取数据，或将数据写入目标位置（如文件、控制台）。

I/O 流分为两大类：**字节流** 和 **字符流**，分别用于处理字节级和字符级的数据：

- **字节流**：处理 8 位字节数据，适合于处理二进制文件，如图片、视频等。主要类是 `InputStream` 和 `OutputStream` 及其子类。
- **字符流**：处理 16 位字符数据，适合于处理文本文件。主要类是 `Reader` 和 `Writer` 及其子类。

## 字符流和字节流的区别

- 字节流一般用来处理图像、视频、音频、PPT、Word等类型的文件。字符流一般用于处理纯文本类型的文件，如TXT文件等，但不能处理图像视频等非文本文件。用一句话说就是：字节流可以处理一切文件，而字符流只能处理纯文本文件。
- 字节流本身没有缓冲区，缓冲字节流相对于字节流，效率提升非常高。而字符流本身就带有缓冲区，缓冲字符流相对于字符流效率提升就不是那么大了。

## 编码和解码

输出流将缓冲区存储的字符通过查ASCII表转换为对应数字再进行编码

输入流对文件进行解码转换为ASCII码对应的数字，然后通过查表转换为读取到的字符

中文编码通常使用GBK字符集

规则

- 汉字使用两个字节进行存储
- 高位字节以1开头，转换成十进制后为负数

Unicode字符集（万国码）是国家标准字符集同时兼任ASCII码

- UTF-16编码：使用2-4个字节保存
- UTF-32编码：固定4个字节保存
- UTF-8编码：使用1-4个字节保存
  - ASCII码：1个字节
  - 简体中文：3个字节

**乱码的原因**

- **字符编码与解码不一致**。乱码问题常常由字符编码（比如 UTF-8、GBK）和解码过程的不一致引起。如果在编码时使用了一种字符集，而在解码时使用了另一种，字符将无法正确显示，从而出现乱码。

## 文件流

一切文件（文本、视频、图片）的数据都是以二进制的形式存储的，传输时也是。所以，字节流可以传输任意类型的文件数据。

### 文件字节流

#### `FileOutputStream`文件输出流

**构造方法**

- `public FileOutputStream(String s)`：接收文件路径创建输出流，**如果文件不存在，则创建一个新文件；如果文件已经存在，则覆盖原有文件**。
- `public FileOutputStream(File file)`：使用文件对象创建 `FileOutputStream` 对象

**写入数据**

- `public void write(int b)`：写入一个ASCII码为b的字符
- `public void write(char b)`：写入一个字符
- `public void write(byte[] b)`：写入一个字节数组
-  `public void write(byte[] b,int off,int len)`：从指定的字节数组写入 len 字节到此输出流，从偏移量 off开始。 **也就是说从off个字节数开始一直到len个字节结束**

**追加数据**

在构造方法中加入第二个`Boolean`类型参数指示是否继续读写

#### `FileInputStream`文件输入流

**构造方法**

- `FileInputStream(String name)`：创建一个 FileInputStream 对象，并打开指定名称的文件进行读取。文件名由 name 参数指定。如果文件不存在，将会抛出 FileNotFoundException 异常。
- `FileInputStream(File file)`：创建一个 FileInputStream 对象，并打开指定的 File 对象表示的文件进行读取。

**读入数据**

- `public int read()`：`read()`方法会读取一个字节并返回其整数表示。如果已经到达文件的末尾，则返回 -1。如果在读取时发生错误，则会抛出 `IOException` 异常。
- `public int read(byte[] b) throws IOException`：读取数据并将其存储在字节数组 `b` 中。返回实际读取的字节数。
- `public int read(byte[] b, int off, int len) throws IOException`：从文件中读取最多 `len` 个字节的数据，存储到字节数组 `b` 中，从偏移量 `off` 开始。返回实际读取的字节数。

#### 常见操作

**文件拷贝**

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class FileCopy {
    public static void main(String[] args) {
        String sourceFile = "source.txt"; // 源文件
        String destFile = "destination.txt"; // 目标文件

        try (FileInputStream fis = new FileInputStream(sourceFile); 
             FileOutputStream fos = new FileOutputStream(destFile)) {

            byte[] buffer = new byte[1024]; // 缓冲区大小，可以根据需要调整
            int length;

            // 读取源文件并写入目标文件
            while ((length = fis.read(buffer)) > 0) {
                fos.write(buffer, 0, length);
            }

            System.out.println("文件拷贝完成！");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

**文件夹拷贝**

```java
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class DirectoryCopy {

    public static void main(String[] args) {
        String sourceDir = "sourceDirectory"; // 源文件夹
        String destDir = "destinationDirectory"; // 目标文件夹

        try {
            copyDirectory(new File(sourceDir), new File(destDir));
            System.out.println("文件夹拷贝完成！");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // 递归复制文件夹
    public static void copyDirectory(File sourceDir, File destDir) throws IOException {
        if (!sourceDir.exists()) {
            throw new IOException("源文件夹不存在！");
        }
        
        // 如果目标文件夹不存在，则创建它
        if (!destDir.exists()) {
            destDir.mkdir();
        }

        // 获取源文件夹中的所有文件和子文件夹
        File[] files = sourceDir.listFiles();
        if (files != null) {
            for (File file : files) {
                // 如果是文件，则直接拷贝
                if (file.isFile()) {
                    copyFile(file, new File(destDir, file.getName()));
                } else if (file.isDirectory()) {
                    // 如果是文件夹，则递归调用
                    copyDirectory(file, new File(destDir, file.getName()));
                }
            }
        }
    }

    // 拷贝文件
    private static void copyFile(File sourceFile, File destFile) throws IOException {
        try (InputStream in = new FileInputStream(sourceFile);
             OutputStream out = new FileOutputStream(destFile)) {

            byte[] buffer = new byte[1024]; // 缓冲区
            int length;

            // 读取文件并写入目标文件
            while ((length = in.read(buffer)) != -1) {
                out.write(buffer, 0, length);
            }
        }
    }
}
```

### 文件字符流

**字符流 = 字节流 + 编码表**

#### `FileReader`文件输入流

一次读取一个字节，遇到中文时一次读入多个字节

**构造方法**

- `FileReader(File file)`：创建一个新的 `FileReader`，参数为**File对象**。
- `FileReader(String fileName)`：创建一个新的 `FileReader`，参数为文件名。
- `FileReader(File file，Charset set)`：创建一个新的 `FileReader`，参数为**File对象和字符集**。

**读取数据**

- `public int read()`：每次可以读取一个字符，返回读取的字符（转为 int 类型），当读取到文件末尾时，返回`-1`
- `public int read(char[]buffer,int off,int len)`:读取多个字符到字符数组`buffer`，返回值为读入的字符数，读到文件末尾返回`-1`

**释放资源**

`public int close()`：释放字符流

#### `FileWriter`文件输出流

**构造方法**

- `FileWriter(File file)`： 创建一个新的 FileWriter，参数为要读取的File对象。可以后跟`Boolean`参数指定是否追加数据
- `FileWriter(String fileName)`： 创建一个新的 FileWriter，参数为要读取的文件的名称。可以后跟`Boolean`参数指定是否追加数据

**写入数据**

- `public void write(int b)`：写入一个ASCII码为b的字符
- `public void write(String b)`：写入字符串
- `public void write(String str, int off, int len)` ：将指定字符串的一部分写入输出流
- `public void write(char[] cbuf)` ：将指定字符数组写入输出流
- `public void write(char[] cbuf, int off, int len)` ：将指定字符数组的一部分写入输出流

**关闭和刷新**

- `flush()` ：刷新缓冲区，将缓冲区中的数据强制写入目标设备或流中,流对象可以继续使用。
- `close()` ：先刷新缓冲区，然后通知系统释放资源。流对象不可以再被使用了。

## **缓冲流**：

缓冲流是对基础流的包装，可以显著提高 I/O 性能。常见的缓冲流有 `BufferedInputStream`、`BufferedOutputStream`、`BufferedReader` 和 `BufferedWriter`，它们通过**内部缓冲区减少实际 I/O 操作的次数**。

在处理大文件或频繁 I/O 操作时，使用缓冲流可以有效提高性能。

### 字节缓冲流

底层自带8KB的缓冲区

#### `BufferedInputStream` 字节缓冲输入流

**构造方法**

`BufferedInputStream(InputStream in)` ：创建一个新的缓冲输入流，注意参数类型为**InputStream**。

**读入数据**

- `public int read()`：`read()`方法会读取一个字节并返回其整数表示。如果已经到达文件的末尾，则返回 -1。如果在读取时发生错误，则会抛出 `IOException` 异常。
- `public int read(byte[] b) throws IOException`：读取数据并将其存储在字节数组 `b` 中。返回实际读取的字节数。
- `public int read(byte[] b, int off, int len) throws IOException`：从文件中读取最多 `len` 个字节的数据，存储到字节数组 `b` 中，从偏移量 `off` 开始。返回实际读取的字节数。

#### `BufferedOutputStream`字节缓冲输出流

**构造方法**

`BufferedOutputStream(OutputStream in)` ：创建一个新的缓冲输入流，注意参数类型为**OutputStream**。

**写入数据**

- `public void write(int b)`：写入一个ASCII码为b的字符
- `public void write(String b)`：写入字符串
- `public void write(String str, int off, int len)` ：将指定字符串的一部分写入输出流
- `public void write(char[] cbuf)` ：将指定字符数组写入输出流
- `public void write(char[] cbuf, int off, int len)` ：将指定字符数组的一部分写入输出流

**关闭和刷新**

- `flush()` ：刷新缓冲区，将缓冲区中的数据强制写入目标设备或流中,流对象可以继续使用。
- `close()` ：先刷新缓冲区，然后通知系统释放资源。流对象不可以再被使用了。只用关闭高级流的流对象底层会自动关闭基本流

### 字符缓冲流

#### `BufferedReader`字符缓冲输入流

**构造方法**

- `BufferedReader(Reader in)` ：创建一个新的缓冲输入流，注意参数类型为**Reader**。

**读取数据**

- `public int read()`：每次可以读取一个字符，返回读取的字符（转为 int 类型），当读取到文件末尾时，返回`-1`
- `public int read(char[]buffer,int off,int len)`:读取多个字符到字符数组`buffer`，返回值为读入的字符数，读到文件末尾返回`-1`
- `String readLine()`: **读一行数据**，读取到最后返回 `null`

**释放资源**

`public int close()`：释放字符流

#### `BufferedWriter`字符缓冲输出流

**构造方法**

- `BufferedWriter(Writer out)`： 创建一个新的缓冲输出流，注意参数类型为**Writer**。

**写入数据**

- `public void write(int b)`：写入一个ASCII码为b的字符
- `public void write(String b)`：写入字符串
- `public void write(String str, int off, int len)` ：将指定字符串的一部分写入输出流
- `public void write(char[] cbuf)` ：将指定字符数组写入输出流
- `public void write(char[] cbuf, int off, int len)` ：将指定字符数组的一部分写入输出流
- `public void newLine()`：输出换行符

**关闭和刷新**

- `flush()` ：刷新缓冲区，将缓冲区中的数据强制写入目标设备或流中,流对象可以继续使用。
- `close()` ：先刷新缓冲区，然后通知系统释放资源。流对象不可以再被使用了。

## 转换流

将字符流和字节流进行连接，实现互相转换

`InputStreamReader` ：将一个字节输入流转换为一个字符输入流，

`OutputStreamWriter` ：将一个字节输出流转换为一个字符输出流。

它们使用指定的字符集将字节流和字符流之间进行转换。常用的字符集包括 UTF-8、GBK、ISO-8859-1 等。

### `InputStreamReader`

#### 作用

- 将字节流（InputStream）转换为字符流（Reader）
- 同时支持指定的字符集编码方式，从而实现字节流到字符流之间的转换。

#### 构造方法

- `InputStreamReader(InputStream in)`: 创建一个使用默认字符集的字符流。
- `InputStreamReader(InputStream in, String charsetName)`: 创建一个指定字符集的字符流。

#### 常用方法

- `read()`：从输入流中读取一个字符的数据。
- `read(char[] cbuf, int off, int len)`：从输入流中读取 len 个字符的数据到指定的字符数组 cbuf 中，从 off 位置开始存放。
- `ready()`：返回此流是否已准备好读取。
- `close()`：关闭输入流。

### `OutputStreamWriter`

#### 作用

- 将字符流（Writer）转换为字节流（OutputStream）
- 同时支持指定的字符集编码方式，从而实现字符流到字节流之间的转换。

#### 构造方法

- `OutputStreamWriter(OutputStream in)`: 创建一个使用默认字符集的字节流。
- `OutputStreamWriter(OutputStream in, String charsetName)`：创建一个指定字符集的字节流。

#### 常用方法

- `write(int c)`：向输出流中写入一个字符的数据。
- `write(char[] cbuf, int off, int len)`：向输出流中写入指定字符数组 cbuf 中的 len 个字符，从 off 位置开始。
- `flush()`：将缓冲区的数据写入输出流中。
- `close()`：关闭输出流

### 示例

```java
try {
    // 从文件读取字节流，使用UTF-8编码方式
    FileInputStream fis = new FileInputStream("test.txt");
    // 将字节流转换为字符流，使用UTF-8编码方式
    InputStreamReader isr = new InputStreamReader(fis, "UTF-8");
    // 使用缓冲流包装字符流，提高读取效率
    BufferedReader br = new BufferedReader(isr);
    // 创建输出流，使用UTF-8编码方式
    FileOutputStream fos = new FileOutputStream("output.txt");
    // 将输出流包装为转换流，使用UTF-8编码方式
    OutputStreamWriter osw = new OutputStreamWriter(fos, "UTF-8");
    // 使用缓冲流包装转换流，提高写入效率
    BufferedWriter bw = new BufferedWriter(osw);

    // 读取输入文件的每一行，写入到输出文件中
    String line;
    while ((line = br.readLine()) != null) {
        bw.write(line);
        bw.newLine(); // 每行结束后写入一个换行符
    }

    // 关闭流
    br.close();
    bw.close();
} catch (IOException e) {
    e.printStackTrace();
}
```

## 序列化流

**序列化**

是将对象转换为字节流的过程，这样对象可以通过网络传输、持久化存储或者缓存。Java 提供了 `java.io.Serializable` 接口来支持序列化，只要类实现了这个接口，就可以将该类的对象进行序列化。

**反序列化**

是将字节流重新转换为对象的过程，即从存储中读取数据并重新创建对象。

### `ObjectOutputStream`序列化流

#### 构造方法

`ObjectOutputStream(OutputStream out)`

```java
FileOutputStream fos = new FileOutputStream("file.txt");
ObjectOutputStream oos = new ObjectOutputStream(fos);
```

#### 写入方法

- `public final writeObject (Object obj)`：写入一个对象
- `public void write(int b) throws IOException`
- `public void write(byte[] b, int off, int len) throws IOException`

#### 示例

```java
public class ObjectOutputStreamDemo {
    public static void main(String[] args) {
        Person person = new Person("沉默王二", 20);
        try {
            FileOutputStream fos = new FileOutputStream("logs/person.dat");
            ObjectOutputStream oos = new ObjectOutputStream(fos);
            oos.writeObject(person);
            oos.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
class Person implements Serializable {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }
}
```

### `ObjectInputStream`反序列化流

`ObjectInputStream` 可以读取 `ObjectOutputStream` 写入的字节流，并将其反序列化为相应的对象（包含`对象的数据`、`对象的类型`和`对象中存储的属性`等信息）。

#### 构造方法

- `ObjectInputStream(InputStream in)`

#### 读入方法

- `public Object readObject()`：读入对象
- `public void read()`：读一个字节

### `Serializable`序列化接口

**定义**

```java
public interface Serializable {
}
```

**注意事项**

- `static`和 `transient`修饰的字段是不会被序列化的
  - 被反序列化后，`transient` 字段的值被设为初始值
- Java底层根据类的内容对实现了`Serializable`接口的类计算出类型为`long`的版本号`serialVersionUID`，若类的代码发生改变会使版本号改变导致无法反序列化
- Java 虚拟机会把字节流中的 `serialVersionUID` 与被序列化类中的 `serialVersionUID` 进行比较，如果相同则可以进行反序列化，否则就会抛出序列化版本不一致的异常
- 通常使用`private` ，`static` ，`final` 来修饰`serialVersionUID`

### `transient`瞬态关键字

在实际开发过程中，不需要被序列化的字段，比如说用户的一些敏感信息（如密码、银行卡号等），为了安全起见，不希望在网络操作中传输或者持久化到磁盘文件中，那这些字段就可以加上 `transient` 关键字。

被 `transient` 关键字修饰的成员变量在反序列化时会被自动初始化为默认值