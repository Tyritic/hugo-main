---
date : '2025-02-08T10:24:08+08:00'
draft : false
title : 'Java中的异步调用'
image : ""
categories : ["Java并发编程","互联网面试题"]
tags : ["JavaSE"]
description : ""
math : true
---

## 为什么要异步调用？

实际项目中，一个接口可能需要同时获取多种不同的数据，然后再汇总返回

如果是串行（按顺序依次执行每个任务）执行的话，接口的响应速度会非常慢。考虑到这些任务之间有大部分都是 **无前后顺序关联** 的，可以 **并行执行** 。通过并行执行多个任务的方式，接口的响应速度会得到大幅优化。

## Future接口

**核心思想** ：当我们执行某一耗时的任务时，可以将这个耗时任务交给一个子线程去异步执行，同时我们可以干点其他事情，不用等待耗时任务执行完成。等我们的事情干完后，我们再通过 **`Future`** 类获取到耗时任务的执行结果。这样一来，程序的执行效率就明显提高了。

```java
// V 代表了Future执行的任务返回值的类型
public interface Future<V> {
    // 取消任务执行
    // 成功取消返回 true，否则返回 false
    boolean cancel(boolean mayInterruptIfRunning);
    // 判断任务是否被取消
    boolean isCancelled();
    // 判断任务是否已经执行完成
    boolean isDone();
    // 获取任务执行结果
    V get() throws InterruptedException, ExecutionException;
    // 指定时间内没有返回计算结果就抛出 TimeOutException 异常
    V get(long timeout, TimeUnit unit)

        throws InterruptedException, ExecutionException, TimeoutExceptio

}
```

**`FutureTask`** 提供了 **`Future`** 接口的基本实现，常用来封装 `Callable` 和 `Runnable`，具有取消任务、查看任务是否执行完成以及获取任务执行结果的方法。

**`FutureTask`** 有两个构造函数，可传入 **`Callable`** 或者 **`Runnable`** 对象。实际上，传入 **`Runnable`** 对象也会在方法内部转换为**`Callable`** 对象。

**`FutureTask`** 相当于对 **`Callable`** 进行了封装，管理着任务执行的情况，存储了 **`Callable`** 的 **`call`** 方法的任务执行结果。

## **`CompletableFuture`** 类

**`CompletableFuture`** 是 Java 8 引入的一个强大的异步编程工具。允许非阻塞地处理异步任务，并且可以通过**链式调用组合**多个异步操作。

**核心特性**

- **异步执行**：使用 **`runAsync()`** 或 **`supplyAsync()`** 方法，可以非阻塞地执行任务。
- **任务的组合**：可以使用 **`thenApply()`** 、**`thenAccept()`** 等方法在任务完成后进行后续操作，支持链式调用。
- **异常处理**：提供 **`exceptionally()`**、**`handle()`** 等方法来处理异步任务中的异常。
- **并行任务**：支持多个异步任务的组合，如 `thenCombine()`、`allOf()` 等方法，可以在多个任务完成后进行操作。
- **非阻塞获取结果**：相比 `Future`，`CompletableFuture` 支持通过回调函数获取结果，而不需要显式的阻塞等待。

### 创建操作

#### 使用构造方法

- **`CompletableFuture<T> future = new CompletableFuture<>();`**

#### 使用静态工厂方法

- 创建异步任务并返回结果
  - **`static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier)`** ：// 使用自定义线程池(推荐)
  - **`static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier, Executor executor)`**
- 创建异步任务，不返回结果
  - **`static CompletableFuture<Void> runAsync(Runnable runnable)`** ：// 使用自定义线程池(推荐)
  - **`static CompletableFuture<Void> runAsync(Runnable runnable, Executor executor)`**

### 获取异步调用的结果

- **`V get() throws InterruptedException, ExecutionException`** ：**阻塞** 调用，等待异步任务完成并返回结果。
  - **`get()`** 会抛出 **`InterruptedException`** 或 **`ExecutionException`**

- **`V getNow(V valueIfAbsent)`** ：**非阻塞** 调用。如果任务已完成，返回计算结果；否则，返回默认值 **`valueIfAbsent`** 。
- **`public T join()`** ：**获取 `CompletableFuture` 计算的结果**，如果任务 **尚未完成**，它会 **阻塞** 直到结果可用。
  - 如果 **`CompletableFuture`** **执行失败**，**`join()`** **不会抛出 `CheckedException`**，而是抛出 **`CompletionException`**（**运行时异常**）。


### 处理异步调用的结果

- **`<U> CompletableFuture<U> thenApply(Function<? super T,? extends U> fn)`** ：接受一个 **`Function`** 实例，用它来修改任务返回值，并返回新的 **`CompletableFuture<U>`** ，支持 **链式调用**

  - 适合需要 **基于前一个任务的结果进行计算或转换** 的场景。


  ```java
  import java.util.concurrent.CompletableFuture;
  import java.util.concurrent.ExecutionException;
  import java.util.function.Function;
  
  public class ThenApplyAnonymousClassExample {
      public static void main(String[] args) throws ExecutionException, InterruptedException {
          // 创建 CompletableFuture
          CompletableFuture<String> future = CompletableFuture.supplyAsync(new java.util.concurrent.Callable<Integer>() {
              @Override
              public Integer call() {
                  return 10;
              }
          }).thenApply(new Function<Integer, String>() {
              @Override
              public String apply(Integer number) {
                  return "Result: " + (number * 2);
              }
          });
  
          // 获取结果
          System.out.println(future.get()); // 输出: Result: 20
      }
  }
  ```

  

- **`CompletableFuture<Void> thenAccept(Consumer<? super T> action)`** ：接受一个 **`Comsumer`** 实例（该任务访问之前异步任务的结果），并基于结果做无返回值的操作，返回新的 **`CompletableFuture<Void>`** ，支持 **链式调用**  ，但不返回新结果

  - 适用于 **消费** 上一个异步操作的结果，但 **不需要修改结果**，例如打印日志、存储数据等。


  ```java
  import java.util.concurrent.CompletableFuture;
  
  public class ThenAcceptExample {
      public static void main(String[] args) throws Exception {
          CompletableFuture<Void> future = CompletableFuture
                  .supplyAsync(() -> "Hello, World")
                  .thenAccept(result -> System.out.println("Received: " + result));
  
          future.get(); // 等待执行完成
      }
  }
  ```

  

- **`CompletableFuture<Void> thenRun(Runnable action)`**  ：接受一个 **不接收参数** 且 **无返回值** 的 **`Runnable`** 任务（该任务不访问之前异步任务的结果），并返回新的 **`CompletableFuture<Void>`** ，支持 **链式调用**  ，不返回新结果

  - 适用于在异步任务完成后执行 **不依赖于结果的** 动作时。

  ```java
  import java.util.concurrent.CompletableFuture;
  
  public class ThenRunExample {
      public static void main(String[] args) throws Exception {
          CompletableFuture<Void> future = CompletableFuture
                  .supplyAsync(() -> "Task Completed")
                  .thenRun(() -> System.out.println("Logging: Task finished!"));
  
          future.get(); // 等待任务完成
      }
  }
  ```



- **`CompletableFuture<T> whenComplete(BiConsumer<? super T, ? super Throwable> action)`** ：不改变异步任务的结果，但是保存下异步任务的结果


  - **`BiConsumer<? super T, ? super Throwable> action`** ：
    - `T`：前一个 `CompletableFuture` **成功** 计算的结果（可能为 `null`）。
    - **`Throwable`** ：**异常信息**（若任务成功则为 `null`）
  - 用于 **无论任务成功或失败时** 都要执行某些操作，且 **不修改原始结果** 的场景。

  ```java
  import java.util.concurrent.CompletableFuture;
  import java.util.concurrent.ExecutionException;
  
  public class WhenCompleteExample {
      public static void main(String[] args) throws ExecutionException, InterruptedException {
          CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
              if (Math.random() > 0.5) {
                  throw new RuntimeException("Computation failed!");
              }
              return "Success!";
          }).whenComplete((result, error) -> {
              if (error != null) {
                  System.out.println("Error: " + error.getMessage());
              } else {
                  System.out.println("Result: " + result);
              }
          });
  
          // 获取最终结果（可能抛出异常）
          System.out.println("Final result: " + future.get());
      }
  }
  ```

  

### 异常处理

- **`CompletableFuture<U> handle(BiFunction<? super T, Throwable, ? extends U> fn)`** ：

  - 如果 **任务成功**，则 `fn` 会接收到前一个任务的结果和 `null` 作为异常，返回一个新的结果。
  - 如果 **任务失败**，则 `fn` 会接收到前一个任务的异常和 `null` 作为结果，返回一个新的结果（默认值）。

  ```java
  import java.util.concurrent.CompletableFuture;
  
  public class HandleExample {
      public static void main(String[] args) {
          CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
              // 随机决定是否抛出异常
              if (Math.random() > 0.5) {
                  throw new RuntimeException("Task failed!");
              }
              return "Task completed successfully!";
          }).handle((result, error) -> {
              if (error != null) {
                  // 任务失败时，返回一个默认值
                  return "Recovered from error: " + error.getMessage();
              } else {
                  // 任务成功时，返回结果的修改
                  return "Handled result: " + result;
              }
          });
  
          // 输出结果
          System.out.println(future.join());
      }
  }
  ```




### 组合处理

- **`public <U> CompletableFuture<U> thenCompose(Function<? super T, ? extends CompletionStage<U>> fn)`**

  - 适用场景

    - 适用于 **前后依赖的异步任务**（即一个任务的结果作为下一个任务的输入）。

  - 示例代码

    ```java
    CompletableFuture<String> future1 = CompletableFuture.supplyAsync(new Supplier<String>() {
                @Override
                public String get() {
                    return "Hello";
                }
            }).thenCompose((String s)-> {
                    return CompletableFuture.supplyAsync(new Supplier<String>() {
                        @Override
                        public String get() {
                            return s + " World";
                        }
                    });
            });
    ```

    

- **`public <U, V> CompletableFuture<V> thenCombine( CompletionStage<? extends U> other, BiFunction<? super T, ? super U, ? extends V> fn)`**

  - 适用场景

    - **`thenCombine()`** 会在 **两个任务都完成** 后，使用提供的函数 **合并它们的结果**。两个任务之间没有前后依赖

  - 示例代码

    ```java
    CompletableFuture<Integer> future2=CompletableFuture.supplyAsync(new Supplier<Integer>() {
                @Override
                public Integer get() {
                    return 100;
                }
            });
    
            CompletableFuture<Integer> future3=CompletableFuture.supplyAsync(new Supplier<Integer>() {
                @Override
                public Integer get() {
                    return 200;
                }
            });
            CompletableFuture<Integer> future4=future2.thenCombine(future3, new BiFunction<Integer, Integer, Integer>() {
                @Override
                public Integer apply(Integer integer, Integer integer2) {
                    return integer+integer2;
                }
            });
    ```



### 并行处理

- **`static CompletableFuture<Void> allOf(CompletableFuture<?>... cfs)`**

  - 适用场景

    - 适用于 **多个异步任务并行执行**，并在 **所有任务完成后继续执行**

  - 示例代码

    ```java
    import java.util.concurrent.CompletableFuture;
    import java.util.Arrays;
    import java.util.List;
    import java.util.stream.Collectors;
    
    public class AllOfExample {
        public static void main(String[] args) {
            CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Task 1");
            CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "Task 2");
            CompletableFuture<String> future3 = CompletableFuture.supplyAsync(() -> "Task 3");
    
            CompletableFuture<Void> allOf = CompletableFuture.allOf(future1, future2, future3);
    
            // 等待所有任务完成后，获取每个任务的结果
            List<String> results = Arrays.asList(future1, future2, future3)
                .stream()
                .map(CompletableFuture::join)
                .collect(Collectors.toList());
    
            System.out.println(results); // 输出: [Task 1, Task 2, Task 3]
        }
    }
    ```

    

- **`static CompletableFuture<Object> anyOf(CompletableFuture<?>... cfs)`**

  - 适用场景

    - 适用于 **多个任务竞争**，只关心 **最先完成** 的任务结果。

  - 示例代码

    ```java
    import java.util.concurrent.CompletableFuture;
    
    public class AnyOfExample {
        public static void main(String[] args) {
            CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> {
                try { Thread.sleep(1000); } catch (InterruptedException e) {}
                return "Task 1";
            });
    
            CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> {
                try { Thread.sleep(500); } catch (InterruptedException e) {}
                return "Task 2";
            });
    
            CompletableFuture<Object> anyOf = CompletableFuture.anyOf(future1, future2);
    
            System.out.println(anyOf.join()); // 输出: Task 2 （因为 Task 2 更快）
        }
    }
    ```

    