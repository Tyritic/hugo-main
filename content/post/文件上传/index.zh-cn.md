---
date : '2024-11-07T09:52:26+08:00'
draft : false
title : '文件上传'
image : ""
categories : ["项目技术"]
tags : ["后端开发"]
description : "项目中文件上传的实现"
---

## 简介

文件上传，是指将本地图片、视频、音频等文件上传到服务器，供其他用户浏览或下载的过程。

## 实现要点

### 前端页面

- 表单项 type=“file”
- 表单提交方式 post
- 表单的enctype属性 multipart/form-data

### 后端controller类

- 使用MultipartFile接收文件

## 实现方式

### 上传到本地

常见方法

```java
- String getOriginalFilename(); //获取原始文件名
- void transferTo(File dest); //将接牧的文件转存到磁盘文件中
- long getSize(); //获取文件的大小，单位:字节
- byte[] getBytes();//获取文件内容的字节数组
- InputStream getinputStream(); //获取接收到的文件内容的输入流
```

具体实现

```java
@RestController
public class UploadController {
    @PostMapping("/upload")
    public Result upload(MultipartFile image) throws IOException
        //获取原始文件名
		String originalFilename =image.getOriginalFilename():
    	//构建新的文件名
		String newfileName = UUID.,randomUUID.toString()+originalFilename.substring(originalFilename.lastindexOf("."));
    //将文件保存在服务器端 E:/images目景下
		image.transferTo(new File("E:/images/"+newFileName)):
		return Result,success();
}
```

{{<notice tip>}}

在SpringBoot中，文件上传，默认单个文件允许最大大小为1M。如果需要上传大文件，可以进行在application.yml如下配置:

```yml
spring:
	servlet:
		multipart.max-file-size=10MB #配置单个文件最大上传大小
		max-request-size=100MB #配置单个请求最大上传大小(一次请求可以上传多个文件)
```

{{</notice>}}

### 阿里云OSS存储

基本概念

- Bucket：存储空间是用户用于存储对象(0bject，就是文件)的容器，所有的对象都必须隶属于某个存储空间。
- SDK:Software Development Kit 的缩写，软件开发工具包，包括辅助软件开发的依赖(jar包)、代码示例等，都可以叫做SDK。

具体实现

1. 创建bucket并获取AccessKey

2. 在pom.xml中引入相关依赖

3. 将aliyunOSS服务所需的相关参数写入配置文件application.yml中，并专门建立一个properties配置文件

4. 将相关方法写入工具类中

   ```java
   public String upload(MultipartFile file) throws ClientException {
           if(file==null||file.isEmpty()){
               return null;
           }
           String endpoint = aliyunOSSProperties.getEndpoint();
           String bucketName = aliyunOSSProperties.getBucketName();
           String region = aliyunOSSProperties.getRegion();
           String accessKeyId = aliyunOSSProperties.getAccessKeyId();
           String accessKeySecret = aliyunOSSProperties.getAccessKeySecret();
           // 创建OSSClient实例
           ClientBuilderConfiguration clientBuilderConfiguration = new ClientBuilderConfiguration();
           CredentialsProvider defaultCredentialProvider = new DefaultCredentialProvider(accessKeyId, accessKeySecret);
           OSS ossClient= OSSClientBuilder.create()
                   .endpoint(endpoint)
                   .credentialsProvider(defaultCredentialProvider)
                   .clientConfiguration(clientBuilderConfiguration)
                   .region(region)
                   .build();
           String originalFilename = file.getOriginalFilename();
           String fileName = UUID.randomUUID().toString() + originalFilename.substring(originalFilename.lastIndexOf("."));
           try {
               InputStream fileInputStream = file.getInputStream();
               ossClient.putObject(bucketName, fileName, fileInputStream);
               String url=endpoint.split("//")[0]+"/"+bucketName+"."+endpoint.split("//")[1]+"/"+fileName;
               return url;
           } catch (Exception e) {
               log.error("上传文件失败", e);
               throw new ClientException("上传文件失败");
           } finally {
               ossClient.shutdown();
           }
       }
   
   public void deleteExhibitImage(String d_url) {
           String endpoint = aliyunOSSProperties.getEndpoint();
           String bucketName = aliyunOSSProperties.getBucketName();
           String region = aliyunOSSProperties.getRegion();
           String accessKeyId = aliyunOSSProperties.getAccessKeyId();
           String accessKeySecret = aliyunOSSProperties.getAccessKeySecret();
           String fileName=d_url.substring(d_url.lastIndexOf("/")+1);//从url中获取bucket中的文件名
           // 创建OSSClient实例
           ClientBuilderConfiguration clientBuilderConfiguration = new ClientBuilderConfiguration();
           CredentialsProvider defaultCredentialProvider = new DefaultCredentialProvider(accessKeyId, accessKeySecret);
           OSS ossClient= OSSClientBuilder.create()
                   .endpoint(endpoint)
                   .credentialsProvider(defaultCredentialProvider)
                   .clientConfiguration(clientBuilderConfiguration)
                   .region(region)
                   .build();
           try {
               ossClient.deleteObject(bucketName, fileName);
           } catch (Exception e) {
               log.error("删除文件失败", e);
           } finally {
               ossClient.shutdown();
           }
       }
   ```

   