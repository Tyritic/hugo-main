---
date : '2024-11-02T19:26:08+08:00'
draft : false
title : 'SpringBoot项目结构'
image : ""
categories : ["SpringBoot"]
tags : ["后端开发"]
description : "SpringBoot项目的基本结构"
---
## 如何读懂SpringBoot项目结构

SpringBoot项目本质上是一个Maven项目，大体骨架与普通的Maven项目相同

普通Maven项目结构

```
Maven-name/
|--src（源代码）
|	|--main（项目实际资源）
|		|--java（java代码）
|		|--resource（资源文件）
|	|--test（测试代码资源）
|		|--java
|		|--resource
|--pom.xml（依赖配置文件）
|--target（打包后的jar包存放地）
```

开发者的代码都存放到**src/main/java**文件夹中

## 代码层

**根目录**：**src/main/java**

**作用**：该目录下存放 **入口启动类** 及程序的开发目录。在这个目录下进行业务开发、创建实体层、控制器层、数据连接层等。

{{<notice note>}}

入口启动类：运行整个项目 **main** 方法的类

```java
@SpringBootApplication
public class UserApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserApplication.class, args);
    }
}
```

其中 **`@SpringBootApplication`** 用于标识SpringBoot项目的入口类

{{</notice>}}

### 控制器层（controller)

**根目录**：**src/main/java/controller**

**作用**：主要负责具体业务模块的流程控制，负责前后端交互，接受前端请求，调用service层，接收service层返回的数据，最后返回具体的页面和数据到客户端

**功能实现**：通过实现controller类来实现

```java
@RequestMapping("/user")
@RestController   // @RestController=@RequestMapping + @ResponseBody
public class UserController {
    @RequestMapping("/映射资源")
    public List<User> findAll(){
        return userService.findAll();
    }
```



### 业务逻辑层(service)

**根目录**：**src/main/java/service**

**作用**：主要负责业务逻辑应用设计

**功能实现**：首先设计Service接口，然后再设计其实现该接口的类(serviceImpl)

**作用目标** ：通常Service接口作用于数据库传输对象（DTO)

```java
@Service
public class UserRegisterServiceImpl implements UserRegisterService {
    @Autowired
    UserMapper userMapper;
    @Override
    public void register(UserRegisterDTO userRegisterDTO) {
        //判断用户是否已存在
        User tempUser=userMapper.getByUsername(userRegisterDTO.getUsername());
        if(tempUser!=null){
            log.error("用户{}已存在",userRegisterDTO.getUsername());
            throw new UsernameHasBeenRegisteredException("用户名已存在");
        }
        //注册
        User user=new User();
        BeanUtils.copyProperties(userRegisterDTO,user);
        userMapper.register(user);
        log.info("用户{}注册成功",userRegisterDTO.getUsername());
    }
}
```

### 常量层(common)

**根目录**：**src/main/java/common**

**作用**：主要存放工具类（**utils**)，常量类（**constant**），统一响应模板（**result**），统一异常处理（**exception**)

### 数据库实体层(pojo)

**根目录**：**src/main/java/pojo**

**作用**：存放数据库的实体类，通常一个实体类对应一张数据库表

### 数据持久层（mapper)

**根目录**：**src/main/java/mapper**

**作用**：访问数据库，向数据库发送sql语句，完成数据的增删改查任务

**功能实现**：通过 **`@Mapper`** 注解接口来建立java方法和sql语句的映射关系

**作用对象** ：

- 插入操作直接操作entity对象
- 更新操作可以直接操作entity对象
- 查询操作通常使用分页操作
- 删除操作通常接受主键作为查询条件

```java
@Mapper
public interface DistrictMapper {
    List<District>searchAll(String tname);
    boolean deleteDistrict(String dname);
    District getDistrictByName(String dname);
    void insertDistrict(DistrictDTO districtDTO);
    void updateDistrictTdid(DistrictDTO districtDTO);
    boolean deleteAll(Long tid);
    void updateDistrictDetail(DistrictDTO districtDTO);
}
```

### **数据传输对象（dto）**

**根目录**：**src/main/java/dto（或者放入pojo层中）**

**作用**：对 **entity** 进行封装，不破坏实体类结构，进行层与层之间的数据传输

{{<notice tip>}}

​	DTO通常用于

1. 控制器（Controller）与服务层（Service）之间的数据传输：控制器通过 DTO 将请求参数传递给服务层，服务层返回 DTO 对象给控制器。
2. 服务层与持久层（Mapper）之间的数据传输：服务层通过 DTO 将实体对象转换为需要的数据结构传递给持久层，持久层返回 DTO 对象给服务层。

{{</notice>}}

### 视图包装对象（vo）

**根目录**：**src/main/java/vo（或者放入pojo层中）**

**作用**：用于封装客户端请求的数据同时不破坏原有的实体类结构

{{<notice tip>}}

VO在实际开发中通常作为controller类方法的返回值从而起到封装客户端请求数据的作用

{{</notice>}}

### 配置类（config)

**根目录**：**src/main/java/config**

**作用**：**以java类代替yaml文件进行Bean对象配置**

**功能实现**：通过 **`@Configuration`** 注解一个java类

```java
@Configuration
public class WebMvcConfiguration implements WebMvcConfigurer {
    @Autowired
    JwtTokenUserInterceptor jwtTokenUserInterceptor;
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        log.info("开始注册拦截器");
        log.info("注册Jwt令牌拦截器：{}",jwtTokenUserInterceptor);
        registry.addInterceptor(jwtTokenUserInterceptor)
                .addPathPatterns("/Operator/**")
                .excludePathPatterns("/Operator/user/login")
                .excludePathPatterns("/Operator/user/register");
    }
}
```

### 参数配置类（properties）

**根目录**：**src/main/java/properties**

**作用**：**以java实体类代替yaml文件进行参数配置**

**功能实现**：通过 **`@ConfigurationProperties`** 注解一个java类

```java
@Data
@Component
@ConfigurationProperties(prefix = "operator.aliyun.oss")
public class AliyunOSSProperties {
    String endpoint;
    String accessKeyId;
    String accessKeySecret;
    String bucketName;
    String region;
}
```

### 过滤器（filter）

**根目录：src/main/java/filter**

**作用**：**在Servlet 处理请求之前或响应之后对数据进行某些处理，实现诸如日志记录、请求数据修改、响应数据修改、权限控制等功能**

{{<notice tip>}}

过滤器工作在 Servlet 容器容中，它拦截客户端的请求和服务器的响应。过滤器链（Filter Chain）是多个过滤器按照一定的顺序执行的集合，一个请求可以依次通过多个过滤器，然后到达目标 Servlet，响应也会按相反的顺序经过这些过滤器返回给客户端。

- 生命周期管理
  - Servlet 容器负责过滤器的生命周期管理。过滤器的生命周期方法包括 **`init`**（初始化）、**`doFilter`**（执行过滤操作）和 **`destroy`**（销毁）。
- 请求处理流程
  - 当一个请求到达 Servlet 容器时，容器会根据部署描述符（web.xml）或注解配置，决定是否以及如何调用过滤器链。
  - 过滤器链是多个过滤器按照一定的顺序执行的集合。容器按照这个顺序依次调用每个过滤器的 **`doFilter`** 方法。
- doFilter 方法
  - 在 **`doFilter`** 方法中，开发者可以实现自定义的处理逻辑，比如修改请求头、记录日志等。
  - **`doFilter`** 方法中必须调用 `FilterChain` 的 **`doFilter`** 方法，这样请求才能继续传递给下一个过滤器或目标资源（如 Servlet）。如果不调用，请求处理流程将会停止。
- 工作机制
  - 过滤器可以修改请求和响应，但它们通常不会生成响应或结束请求，因为这通常是 Servlet 或其他资源的职责
  
  参考文章：
  
  1. [Filter（过滤器）和 Interceptor（拦截器）详解_过滤器和拦截器-CSDN博客](https://blog.csdn.net/weixin_52438357/article/details/135955373)

{{</notice>}}

**功能实现**

1. 创建过滤器类

   - 实现 **javax.servlet.Filter** 接口。
   - 重写 **`init()`**、**`doFilter()`** 和 **`destroy()`** 方法。
2. 配置过滤器

   - 使用注解 **`@WebFilter`** 进行声明和配置。
   - 或者在 web.xml 文件中配置。
3. 编写过滤逻辑：

   - 在 **`doFilter()`**方法中实现具体的过滤逻辑。

   **示例代码**
   
   ```java
   import javax.servlet.*;
   import javax.servlet.annotation.WebFilter;
   import java.io.IOException;
   
   @WebFilter("/example/*") // 过滤器应用于 URL 模式 "/example/*"
   public class ExampleFilter implements Filter {
       
       @Override
       public void init(FilterConfig filterConfig) throws ServletException {
           // 初始化代码，例如资源加载
       }
   
       @Override
       public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
               throws IOException, ServletException {
           // 在请求处理之前执行的代码
           System.out.println("Before Servlet processing");
   
           chain.doFilter(request, response); // 将请求传递给下一个过滤器或目标资源
   
           // 在请求处理之后执行的代码
           System.out.println("After Servlet processing");
       }
   
       @Override
       public void destroy() {
           // 清理代码，例如释放资源
       }
   }
   
   ```
   
   

### 拦截器（interceptor）

   **根目录**：**src/main/java/interceptor**

   **作用**：是 Spring MVC 框架中的一个核心组件，用于在处理 HTTP 请求的过程中进行拦截和处理。拦截器主要用于实现跨切面（cross-cutting）的逻辑，如日志记录、性能统计、安全控制、事务处理等。

   **功能实现**

1. **创建拦截器类**：

   - 实现 **`HandlerInterceptor`**接口或继承 **`HandlerInterceptorAdapter`**类。
   - 重写 **`preHandle()`**、**`postHandle()`**  和 **`afterCompletion()`** 方法。

2. **注册拦截器**：

   - 创建一个配置类，实现 **WebMvcConfigurer**接口。
   - 重写 **addInterceptors** 方法来添加拦截器。

3. **编写拦截逻辑**：

   - 在 **`preHandle()`**、**`postHandle()`** 和 **`afterCompletion()`**方法中实现具体的拦截逻辑。

   **示例代码**

```java
import org.springframework.web.servlet.HandlerInterceptor;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class MyInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        // 请求处理前的逻辑
        return true; // 返回 true 继续流程，返回 false 中断流程
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) {
        // 请求处理后的逻辑，但在视图渲染前
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        // 请求处理完毕后的逻辑
    }
}

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new MyInterceptor()).addPathPatterns("/**"); // 应用于所有路径
    }
}

```

## 项目配置层

**根目录**：**src/main/resource**

**application.yml** ：项目的整体配置文件

**mapper** ：数据库映射文件
