---
date : '2025-07-13T22:20:26+08:00'
draft : false
title : 'Kitex的基本特性'
image : ""
categories : ["Kitex框架"]
tags : ["后端开发"]
description : "Kitex的基本特性"
math : true
---

## Go的项目结构

```
|--src（源代码）
|	|--app（项目的主要服务，通常使用Hertz框架生成暴露的HTTP服务）
|		|---api
|			|----go_api(HTTP服务)
|		|----faas(faas服务)
|		|----rpc(RPC服务)
|
|	|--biz(业务逻辑代码)
|   |--dao(数据库交互)
|	|--...(其他模块)

```

## RPC服务的项目结构

```
|--rpc（rpc服务集合）
|	|--service_name（单个RPC服务）
|		|---client(RPC客户端)
|		|---dal(数据交互层)
|		|----headlers(RPC服务的具体实现)
|		|----model(数据类型)
|		|----tool(工具层)
|		|----handler.go
|		|----kitex_gen
|	|--biz(业务逻辑代码)
|   |--dao(数据库交互)
|	|--...(其他模块)
```

其中kitex_gen的代码结构如下

```shell
|-- kitex_gen // Dir for Generated code, which should not be modified. 
|   |-- base
|   |   |-- base.go
|   |   |-- k-base.go
|   |   |-- k-consts.go
|   |-- P
|       |-- S
|           |-- M
│               ├── k-consts.go
│               ├── k-stock.go // kitex 专用的一些拓展内容,FastCodec 序列化代码
│               ├── stock.go // 根据 IDL 生成的编解码文件，由 IDL 编译器生成（结构体桩代码和普通的序列化）
│               └── stockservice // kitex 封装代码主要在这里(Kitex Client/Server的脚手架)
│                   ├── client.go
│                   ├── invoker.go
│                   ├── server.go
│                   └── stockservice.go
```

## 代码框架生成了什么

生成代码主要分为两个部分

- 结构体桩代码 + 普通的序列化代码  
- 创建 Kitex Client/Server 的脚手架

以stock.thrift为例

```thrift
namespace go example.shop.stock
include "base.thrift"
struct GetStockReq {
    1: required i64 item_id
}

struct GetStockResp {
    1: required i64 stock,
    2: base.BaseResp baseResp
}

service StockService {
    GetStockResp GetStock(1: GetStockReq req)
}
```

### 结构体桩代码

```go
type Item struct {
	Id          int64  `thrift:"id,1" frugal:"1,default,i64" json:"id"`
	Title       string `thrift:"title,2" frugal:"2,default,string" json:"title"`
	Description string `thrift:"description,3" frugal:"3,default,string" json:"description"`
	Stock       int64  `thrift:"stock,4" frugal:"4,default,i64" json:"stock"`
}

func NewItem() *Item {
	return &Item{}
}

func (p *Item) InitDefault() {
}

func (p *Item) GetId() (v int64) {
	return p.Id
}

func (p *Item) GetTitle() (v string) {
	return p.Title
}

func (p *Item) GetDescription() (v string) {
	return p.Description
}

func (p *Item) GetStock() (v int64) {
	return p.Stock
}
func (p *Item) SetId(val int64) {
	p.Id = val
}
func (p *Item) SetTitle(val string) {
	p.Title = val
}
func (p *Item) SetDescription(val string) {
	p.Description = val
}
func (p *Item) SetStock(val int64) {
	p.Stock = val
}

func (p *Item) String() string {
	if p == nil {
		return "<nil>"
	}
	return fmt.Sprintf("Item(%+v)", *p)
}

var fieldIDToName_Item = map[int16]string{
	1: "id",
	2: "title",
	3: "description",
	4: "stock",
}
```

常见方法

- **`Get/Set`** ：作为Getter和Setter，获取字段值
  - 被option修饰的字段会被转换为指针，Get方法获取的是其值
- **`String`** ：输出对象的字符串

|                            方法名                            |                  描述&用途                   | CodeGen 内容长度 |
| :----------------------------------------------------------: | :------------------------------------------: | :--------------: |
|                         InitDefault                          |               Frugal 场景需要                |        短        |
|              GetXXXField/SetXXXField/IsSetXXXX               |      GetterSetter，部分 interface 需要       |        短        |
|              Read/ReadFieldX/Write/writeFieldX               |              原生 Apache Codec               |        长        |
|                            String                            |                   Stringer                   |        短        |
|                 DeepEqual/FieldXXXDeepEqual                  |                 set 去重提速                 |        长        |
|                           DeepCopy                           |                RPAL 场景需要                 |        短        |
|                      ThriftService 模板                      |        ServiceInterface 描述接口定义         |        短        |
|             XXXClientFactory、XXXClientProtocol              |       旧的 ThriftClient 代码，不再有用       |       较长       |
|                         XXXProcessor                         |     旧的 Thrift Processor 代码，不再有用     |       较长       |
|                 XXXServiceMethodArgs/Result                  | Thrift 为Method 的入参和返回值单独生成的类型 |        短        |
|                  GetFirstArgument/GetResult                  |              args、result 专用               |        短        |
| FastRead/FastReadFieldX/FastWrite/FastWriteNocopy/BLength/fastWriteFieldX/fieldXLength |               FastCodec 编解码               |        长        |
|                GetOrSetBase/GetOrSetBaseResp                 |      特殊的 Base 相关接口，框架内部使用      |        短        |

### 脚手架

```
── stockservice // kitex 封装代码主要在这里(Kitex Client/Server的脚手架)
│              ├── client.go // 远程调用
│              ├── invoker.go
│              ├── server.go
│              └── stockservice.go
```

