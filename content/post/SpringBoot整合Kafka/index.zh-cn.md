
---
date : '2025-03-18T19:22:46+08:00'
draft : false
title : 'SpringBoot整合Kafka'
image : ""
categories : ["Kafka","Spring系列"]
tags : ["消息队列","Web开发框架"]
description : "SpringBoot中整合Kafka"
math : true
---

## 🚀 SpringBoot中整合Kafka的流程

### 📦 引入依赖

引入 **Spring for Apache Kafka** 依赖

```xml
&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
&lt;/dependency&gt;

&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.kafka&lt;/groupId&gt;
    &lt;artifactId&gt;spring-kafka&lt;/artifactId&gt;
&lt;/dependency&gt;
```

---

### ⚙️ 配置Kafka相关参数

在application.xml中配置Kafka的相关参数

---

### 📤 创建生产者

通常生产者作为Service类，使用 **`KafkaTemplate`** 的相关API来调用相关方法

```java
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class KafkaProducer {
    private final KafkaTemplate&lt;String, String&gt; kafkaTemplate;

    public KafkaProducer(KafkaTemplate&lt;String, String&gt; kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void sendMessage(String topic, String message) {
        kafkaTemplate.send(topic, message);
        System.out.println("Sent message: " + message);
    }
}
```

---

### 📥 创建消费者

对监听的方法使用 **`@KafkaListener`** 注解，指定消息主题和消费者组

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class KafkaConsumer {

    @KafkaListener(topics = "test-topic", groupId = "my-group")
    public void listen(ConsumerRecord&lt;String, String&gt; record) {
        System.out.println("Received message: " + record.value());
    }
}
```

