---
date : '2024-11-15T15:55:52+08:00'
draft : false
title : 'SpringBoot中的三大组件'
image : ""
categories : ["SpringBoot"]
tags : ["后端组件"]
description : "SpringBoot框架中对JavaWeb三大组件的集成"
---

## JavaWeb的三大组件

### Servlet

Servlet是Java Servlet的简称，称为小服务程序或服务连接器，用Java编写的服务器端程序，主要功能在于交互式地浏览和修改数据，生成动态Web内容。

狭义的Servlet是指Java语言实现的一个接口，广义的Servlet是指任何实现了这个Servlet接口的类，一般情况下，人们将Servlet理解为后者。Servlet运行于支持Java的应用服务器中。从原理上讲，Servlet可以响应任何类型的请求，但绝大多数情况下Servlet只用来扩展基于HTTP协议的Web服务器。

#### 作用：

- 接收请求数据
- 处理请求
- 完成响应

#### 使用方法

- 实现javax.servlet.Servlet接口；
- 继承javax.servlet.GenericServlet类；
- 继承javax.servlet.http.HttpServlet类；

#### 工作原理

​		Servlet接口定义了Servlet与servlet容器之间的契约。这个契约是：Servlet容器将Servlet类载入内存，并产生Servlet实例和调用它具体的方法。但是要注意的是，在一个应用程序中，每种Servlet类型只能有一个实例。

​		用户请求致使Servlet容器调用Servlet的Service（）方法，并传入一个ServletRequest对象和一个ServletResponse对象。ServletRequest对象和ServletResponse对象都是由Servlet容器（例如TomCat）封装好的，并不需要程序员去实现，程序员可以直接使用这两个对象。

 		ServletRequest中封装了当前的Http请求，因此，开发人员不必解析和操作原始的Http数据。ServletResponse表示当前用户的Http响应，程序员只需直接操作ServletResponse对象就能把响应轻松的发回给用户。
 	
 		对于每一个应用程序，Servlet容器还会创建一个ServletContext对象。这个对象中封装了上下文（应用程序）的环境详情。每个应用程序只有一个ServletContext。每个Servlet对象也都有一个封装Servlet配置的ServletConfig对象。

#### 生命周期

- init( ),当Servlet第一次被请求时，Servlet容器就会开始调用这个方法来初始化一个Servlet对象出来，但是这个方法在后续请求中不会在被Servlet容器调用，就像人只能“出生”一次一样。我们可以利用init（ ）方法来执行相应的初始化工作。调用这个方法时，Servlet容器会传入一个ServletConfig对象进来从而对Servlet对象进行初始化。
- service( )方法，每当请求Servlet时，Servlet容器就会调用这个方法。就像人一样，需要不停的接受老板的指令并且“工作”。第一次请求时，Servlet容器会先调用init( )方法初始化一个Servlet对象出来，然后会调用它的service( )方法进行工作，但在后续的请求中，Servlet容器只会调用service方法了。
- destory,当要销毁Servlet时，Servlet容器就会调用这个方法，就如人一样，到时期了就得死亡。在卸载应用程序或者关闭Servlet容器时，就会发生这种情况，一般在这个方法中会写一些清除代码。

```java
public class MyFirstServlrt implements Servlet {
 
    @Override
    public void init(ServletConfig servletConfig) throws ServletException {
        System.out.println("Servlet正在初始化");
    }
 
    @Override
    public ServletConfig getServletConfig() {
        return null;
    }
 
    @Override
    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
        //专门向客服端提供响应的方法
        System.out.println("Servlet正在提供服务");
 
    }
 
    @Override
    public String getServletInfo() {
        return null;
    }
 
    @Override
    public void destroy() {
        System.out.println("Servlet正在销毁");
    }
}      
```

#### ServletRequest接口

Servlet容器对于接受到的每一个Http请求，都会创建一个ServletRequest对象，并把这个对象传递给Servlet的Sevice( )方法。其中，ServletRequest对象内封装了关于这个请求的许多详细信息。

```java
public interface ServletRequest {
  
    int getContentLength();//返回请求主体的字节数
 
    String getContentType();//返回主体的MIME类型
 
    String getParameter(String var1);//返回请求参数的值
 
}
```



#### ServletResponse接口

javax.servlet.ServletResponse接口表示一个Servlet响应，在调用Servlet的Service( )方法前，Servlet容器会先创建一个ServletResponse对象，并把它作为第二个参数传给Service( )方法。ServletResponse隐藏了向浏览器发送响应的复杂过程。

```java
public interface ServletResponse {
    String getCharacterEncoding();
 
    String getContentType();
 
    ServletOutputStream getOutputStream() throws IOException;
 
    PrintWriter getWriter() throws IOException;
 
    void setCharacterEncoding(String var1);
 
    void setContentLength(int var1);
 
    void setContentType(String var1); //在发送任何HTML之前，应该先调用setContentType（）方法，设置响应的内容类型，并将“text/html”作为一个参数传入，这是在告诉浏览器响应的内容类型为HTML，需要以HTML的方法解释响应内容而不是普通的文本，或者也可以加上“charset=UTF-8”改变响应的编码方式以防止发生中文乱码现象。
 
    void setBufferSize(int var1);
 
    int getBufferSize();
 
    void flushBuffer() throws IOException;
 
    void resetBuffer();
 
    boolean isCommitted();
 
    void reset();
 
    void setLocale(Locale var1);
 
    Locale getLocale();
}
```

#### HttpServlet抽象类

HttpServlet抽象类是继承于GenericServlet抽象类而来的。使用HttpServlet抽象类时，还需要借助分别代表Servlet请求和Servlet响应的HttpServletRequest和HttpServletResponse对象。

```java
protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
    }

protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
    }

protected void doPut(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
    }

protected void doDelete(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
    }
```



#### HttpServletRequest接口

HttpServletRequest表示Http环境中的Servlet请求。它扩展于javax.servlet.ServletRequest接口，并添加了几个方法。

获取请求的相关数据

```java
String getContextPath();//返回请求上下文的请求URI部分

Cookie[] getCookies();//返回一个cookie对象数组

String getHeader(String var1);//返回指定HTTP标题的值

String getMethod();//返回生成这个请求HTTP的方法名称

String getQueryString();//返回请求URL中的查询字符串

HttpSession getSession();//返回与这个请求相关的会话对象

String getRequestURI();

StringBuffer getRequestURL();

String[] getParameterValues(String name); //获得如checkbox类（名字相同，但值有多个）的数据。 接收数组变量

String getParameter(String name)； //获得相应名的数据，如果有重复的参数名，则返回第一个的值
```



#### HttpServletResponse接口

在Service API中，定义了一个HttpServletResponse接口，它继承自ServletResponse接口，专门用来封装HTTP响应消息。  由于HTTP请求消息分为状态行，响应消息头，响应消息体三部分，因此，在HttpServletResponse接口中定义了向客户端发送响应状态码，响应消息头，响应消息体的方法。

设置响应的相关数据

```java
void addCookie(Cookie var1);//给这个响应添加一个cookie

void addHeader(String var1, String var2);//给这个请求添加一个响应头

void sendRedirect(String var1) throws IOException;//发送一条响应码，讲浏览器跳转到指定的位置

void setStatus(int var1);//设置响应行的状态码

void addHeader(String name, String value);//添加响应头

void addIntHeader(String name, int value)

void addDateHeader(String name, long date)

void setHeader(String name, String value)

void setDateHeader(String name, long date)

void setIntHeader(String name, int value)

PrintWriter getWriter();//获得字符流，通过字符流的write(String s)方法可以将字符串设置到response   缓冲区中，随后Tomcat会将response缓冲区中的内容组装成Http响应返回给浏览器端。

ServletOutputStream getOutputStream();//获得字节流，通过该字节流的write(byte[] bytes)可以向response缓冲区中写入字节，再由Tomcat服务器将字节内容组成Http响应返回给浏览器。
```



### Filter

参见先前博客 [Filter](https://tyritic.github.io/p/filter/)

### Listener

#### 概述

​	监听器就是监听某个对象的状态变化的组件，监听web应用中某些对象、信息的创建、销毁、增加，修改，删除等动作的发生，然后作出相应的响应处理

#### 具体实现

1. 实现ServletContextListener接口

   ```java
   public class MyListener implements ServletContextListener {
       @Override
       public void contextInitialized(ServletContextEvent sce){
           System.out.println("Servlet上下文--->当前web项目启动");
       }
       @Override
       public void contextDestroyed(ServletContextEvent sce){
           System.out.println("当前类销毁");
       }
   }
   ```

2. 注册Listenner监听器

## SpringBoot对三大组件的集成

SpringBoot中内嵌的Servlet容器是Tomcat服务器

### 嵌入式Servlet容器配置修改

- 方法一：通过全局配置文件Application.yml修改

  - 可以通过server.xxx 来进行web服务配置， 没有带服务器名称的则是通用配置,通过带了具体的服务器名称则是单独对该服务器进行设置，比如server.tomcat.xxx 就是专门针对tomcat的配置,具体配置参见[SpringBoot官方文档](https://springdoc.cn/spring-boot/application-properties.html#appendix.application-properties.server)

    ```yml
    server:
    	port: 8080
    	tomcat:
    		
    ```

- 方法二：通过注册一个实现 `WebServerFactoryCustomizer` 接口的Spring Bean

  ```java
  import org.springframework.boot.web.server.WebServerFactoryCustomizer;
  import org.springframework.boot.web.servlet.server.ConfigurableServletWebServerFactory;
  import org.springframework.stereotype.Component;
  
  @Component
  public class MyWebServerFactoryCustomizer implements WebServerFactoryCustomizer<ConfigurableServletWebServerFactory> {
  
      @Override
      public void customize(ConfigurableServletWebServerFactory server) {
          server.setPort(9000);
      }
  
  }
  ```

  - 修改server.xxx 配置的相关内容
  - 会跟配置文件形成互补

### 三大组件的注册

- 方法一：servlet3.0规范提供的注解方式注册

  - 在组件的实现类使用提供的注解注册

    ```java
    @WebServlet(name="HelloServlet",urlPatterns = "/HelloServlet")
    public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    	PrintWriter writer = resp.getWriter();
    	writer.println("hello servlet!");
     	}
    }
    ```

    - @WebServlet
    - @WebListener
    - @WebFilter

  - 在SpringBoot启动类上添加注解@ServletComponentScan

    ```java
    @SpringBootApplication
    @ServletComponentScan
    public class Application {
         public static void main(String[] args) {
         	SpringApplication.run(Application.class, args);
         }
    }	
    ```

- 方法二：SpringBoot提供的注册方法

  ```java
  package com.hzl.boot.config.filter;
  
  import org.springframework.boot.web.servlet.FilterRegistrationBean;
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;
  
  import javax.servlet.Filter;
  
  /**
   * @description
   * @create: 2024-09-23 22:25
   **/
  @Configuration
  public class FilterRegistrationDemo {
  
  	@Bean
  	public FilterRegistrationBean filterRegistrationBean(){
  		FilterRegistrationBean<Filter> registrationBean = new FilterRegistrationBean<>();
  		// 设置自己的过滤器
  		registrationBean.setFilter(new MyFilter());
  		// 设置自定义的拦截规则
  		registrationBean.addUrlPatterns("/*");
  		// 设置拦截器的顺序
  		registrationBean.setOrder(1);
  
  		return registrationBean;
  	}
  }
  ```

  - ServletRegistrationBean
  - FilterRegistrationBean
  - ServletListenerRegistrationBean

### 切换内嵌Servlet容器

SpringBoot包含了对Tomcat,Jetty（Socket)等服务器的支持

通过修改pom.xml的依赖即可排除相关依赖并添加相关依赖即可

1. 排除原有的tomcat依赖

   ```xml
   <dependency>
   	 <groupId>org.springframework.boot</groupId>
   	 <artifactId>spring‐boot‐starter‐web</artifactId>
   	 <!‐‐1.排除tomcat‐‐>
   	 <exclusions>
   		 <exclusion>
   		 <artifactId>spring‐boot‐starter‐tomcat</artifactId>
   		 <groupId>org.springframework.boot</groupId>
   	 	 </exclusion>
   	 </exclusions>
   </dependency>
   ```

2. 引入相关依赖

   ```xml
   <!‐‐2.依赖jetty -->
   <dependency>
   	<artifactId>spring‐boot‐starter‐jetty</artifactId>
   	<groupId>org.springframework.boot</groupId>
   </dependency>
   
   <!‐‐3.依赖undertow ‐‐>
   <dependency>
   	<artifactId>spring‐boot‐starter‐undertow</artifactId>
   	<groupId>org.springframework.boot</groupId>
   </dependency>
   ```

   

