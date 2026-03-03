---
date : '2025-06-25T22:05:05+08:00'
draft : false
title : 'Go中的string'
image : ""
categories : ["Golang"]
tags : ["后端开发"]
description : "Go中string的底层原理"
math : true
---

## 📝 string的特点

- **string是不可变的**，是一个只读的字符数组，类似于 Java
- 每个字符串的长度虽然也是固定的，但是字符串的长度并不是字符串类型的一部分
- 字符串的编码为 **UTF-8**，源代码中的文本字符串通常被解释为采用 UTF-8 编码的 Unicode 码点（rune）序列，因此字符串可以包含任意的数据

---

## 🔧 底层原理

string 在 Go 中的源码如下，本质上是一个结构体：

```go
type StringHeader struct {
    Data uintptr
    Len  int
}
```

- **Data**：指向底层字符数组的指针
- **Len**：字符串的长度

<div align="center">
  <img src="image-20250625221850926.png" alt="StringHeader结构示意图" width="60%">
</div>

---

## 🛠️ 常见操作

### 📏 获取字符串长度

- **`len(str)`**：输出字符串的长度（字节数）

### 📦 strings 包常用操作

| 方法 | 功能说明 |
|------|----------|
| **`strings.Contains(s, substr)`** | 判断字符串 s 是否包含子串 substr |
| **`strings.Count(s, substr)`** | 统计子串 substr 在 s 中出现的次数 |
| **`strings.Split(s, sep)`** | 使用分隔符 sep 分割字符串 s |
| **`strings.HasPrefix(s, prefix)`** | 判断 s 是否以 prefix 开头 |
| **`strings.HasSuffix(s, suffix)`** | 判断 s 是否以 suffix 结尾 |
| **`strings.Index(s, substr)`** | 查找子串 substr 在 s 中首次出现的位置 |
| **`strings.Repeat(s, count)`** | 将字符串 s 重复 count 次 |
| **`strings.Replace(s, old, new, n)`** | 将 s 中的 old 替换为 new，最多替换 n 次 |

### 🔤 大小写转换

- **`strings.ToLower("GO")`** → `go`
- **`strings.ToUpper("java")`** → `JAVA`

### ✂️ 去除字符

- **`strings.Trim("#hello #go#", "#")`**：去除字符串两端的指定字符

### 🔄 字符数组转换

string 可以被转换为 **`[]byte`** 和 **`[]rune`**：

- **`[]byte`**：适合处理 ASCII 字符
- **`[]rune`**：适合处理包含中文、emoji 等多字节字符

### 🔍 访问字符

- **`s[i]`**：直接访问底层字符数组的第 i 个 **byte**

---

## 🔗 字符串拼接

在 Go 语言中，字符串拼接有多种方式，不同方式的性能差异很大。

### 📊 五种拼接方式对比

#### 1️⃣ 使用 `+` 运算符

```go
s1 := "Hello"
s2 := "World"
result := s1 + " " + s2
```

**特点**：
- 使用简单，直观易懂
- **性能最差**：每次拼接都会创建新的字符串，涉及内存分配和拷贝
- 不适合大量字符串拼接场景

---

#### 2️⃣ 使用 `fmt.Sprintf`

```go
name := "Go"
version := 1.18
result := fmt.Sprintf("Language: %s, Version: %.2f", name, version)
```

**特点**：
- 支持格式化输出，灵活性高
- **性能一般**：需要解析格式字符串，有额外开销
- 适合需要格式化输出的场景

---

#### 3️⃣ 使用 `strings.Builder`（推荐）

```go
var builder strings.Builder
builder.WriteString("Hello")
builder.WriteString(" ")
builder.WriteString("World")
result := builder.String()
```

**核心方法**：
- **`WriteString(str string)`**：添加字符串
- **`WriteRune(r rune)`**：添加单个 Unicode 字符
- **`WriteByte(b byte)`**：添加单个字节
- **`Grow(n int)`**：预分配 n 字节的内存空间

**特点**：
- **性能最好**：预分配内存，避免重复分配和拷贝
- 专门用于字符串拼接场景
- **推荐使用**在性能敏感的场景

**性能优化技巧**：
```go
var builder strings.Builder
// 预分配内存，避免动态扩容
builder.Grow(100)  
builder.WriteString("预先知道大概长度时，使用Grow预分配内存")
result := builder.String()
```

---

#### 4️⃣ 使用 `bytes.Buffer`

```go
var buffer bytes.Buffer
buffer.WriteString("Hello")
buffer.WriteString(" ")
buffer.WriteString("World")
result := buffer.String()
```

**特点**：
- 功能与 `strings.Builder` 类似
- **性能稍差**：有额外的接口开销
- 如果需要同时处理字节和字符串，可以使用

---

#### 5️⃣ 使用 `[]byte` 切片

```go
var buf []byte
buf = append(buf, "Hello"...)
buf = append(buf, ' ')
buf = append(buf, "World"...)
result := string(buf)
```

**特点**：
- **性能较好**：直接操作字节切片
- 需要手动管理内存
- 适合对性能有极高要求的场景

---

### ⚡ 性能对比总结

| 拼接方式 | 性能 | 适用场景 |
|----------|------|----------|
| `+` 运算符 | ⭐ | 少量字符串拼接，简单场景 |
| `fmt.Sprintf` | ⭐⭐ | 需要格式化输出的场景 |
| `strings.Builder` | ⭐⭐⭐⭐⭐ | **大量字符串拼接，性能敏感场景** |
| `bytes.Buffer` | ⭐⭐⭐⭐ | 需要同时处理字节和字符串 |
| `[]byte` | ⭐⭐⭐⭐ | 对性能有极高要求，手动管理内存 |

### 💡 最佳实践建议

1. **简单拼接**：少量字符串（2-3个）直接使用 `+` 即可
2. **循环拼接**：在循环中拼接字符串时，**必须使用** `strings.Builder`
3. **预分配内存**：如果知道最终字符串的大致长度，使用 `Grow()` 预分配内存
4. **格式化输出**：需要格式化时使用 `fmt.Sprintf`，否则优先使用 `strings.Builder`

---

## 📚 总结

- string 是**不可变**的只读字符数组，采用 **UTF-8** 编码
- 底层通过 `StringHeader` 结构体实现，包含数据指针和长度
- 字符串操作主要使用 **`strings`** 包提供的丰富 API
- 字符串拼接优先使用 **`strings.Builder`**，在性能敏感场景下预分配内存
