---
date : '2025-01-17T09:15:30+08:00'
draft : false
title : 'Java的反射机制'
image : ""
categories : ["Java基础"]
tags : ["JavaSE"]
description : "手写笔记转换"
math : true
---

## 反射机制的定义

**Java的反射机制**是一种强大的特性，它允许在运行时动态地查询和操作类、方法、构造器、字段等信息，甚至可以在运行时创建对象、修改字段和调用方法。反射机制使得 Java 程序具备了更高的灵活性，可以编写更加通用和扩展性强的代码。

## 反射机制的特性

- **运行时类信息访问**：反射机制允许程序在运行时获取类的完整结构信息，包括类名、包名、父类、实现的接口、构造函数、方法和字段等。
- **动态对象创建**：可以使用反射API动态地创建对象实例，即使在编译时不知道具体的类名。这是通过Class类的newInstance()方法或Constructor对象的newInstance()方法实现的。
- **动态方法调用**：可以在运行时动态地调用对象的方法，包括私有方法。这通过Method类的invoke()方法实现，允许你传入对象实例和参数值来执行方法。
- **访问和修改字段值**：反射还允许程序在运行时访问和修改对象的字段值，即使是私有的。这是通过Field类的get()和set()方法完成的。

## 反射的核心类

- **`Class`** 类：`Class` 类是反射的核心，它表示一个类或接口的元数据。通过 `Class` 类，可以获取类的构造器、方法、字段等信息。
- **`Constructor`** 类：表示类的构造器，可以通过反射动态创建对象。
- **`Method`** 类：表示类的方法，可以调用指定的实例方法。
- **`Field`** 类：表示类的字段（成员变量），可以访问和修改字段的值。
- **`Modifier`** 类：用于解析和获取类、方法、字段等的访问修饰符。

## 反射的常见操作

### 类对象（`class`）

#### 获取类的`class`的对象

- `Class.forName("全类名")`：对应于Java的源代码阶段
- `类名.class`：对应于加载阶段（将字节码文件加入到内存中）
- `对象.getClass()`：对应于运行阶段

上述三个方法获取的class的对象是同一个对象

#### 获取类的构造器（Constructor）

- **`getConstructor(Class<?>... parameterTypes)`**：获取类的公共构造器，构造器的参数类型必须与传入的类型匹配。

  如果构造器不存在，会抛出 `NoSuchMethodException`。

  ```java
  Class<?> clazz = Person.class;
  Constructor<?> constructor = clazz.getConstructor(String.class, int.class); // 传入构造器参数类型
  Person person = (Person) constructor.newInstance("John", 25);
  ```

- **`getDeclaredConstructor(Class<?>... parameterTypes)`**：获取类的所有构造器（包括私有构造器、受保护的构造器等），与 `getConstructor` 方法不同，`getDeclaredConstructor` 会返回类的所有构造器，而不仅限于公共构造器。

  ```java
  Constructor<?> constructor = clazz.getDeclaredConstructor(String.class, int.class); // 获取指定参数类型的构造器
  constructor.setAccessible(true); // 如果是私有构造器，需要解除访问权限
  Person person = (Person) constructor.newInstance("Alice", 30);
  ```

- **`getConstructors()`**：获取类的所有公共构造器，返回一个 `Constructor` 数组，包含该类及其父类的所有公共构造器。

  ```java
  Constructor<?>[] constructors = clazz.getConstructors();
  for (Constructor<?> constructor : constructors) {
      System.out.println(constructor.getName());
  }
  ```

- **getDeclaredConstructors()**：获取类的所有构造器（包括私有构造器、受保护的构造器等），返回一个 `Constructor` 数组，包含该类的所有构造器（不包括父类的构造器）。

  ```java
  Constructor<?>[] declaredConstructors = clazz.getDeclaredConstructors();
  for (Constructor<?> constructor : declaredConstructors) {
      System.out.println(constructor.getName());
  }
  ```

  

**示例代码**

```java
import java.lang.reflect.*;

class Person {
    private String name;
    private int age;

    // 公共构造器
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // 默认构造器
    public Person() {}

    // 私有构造器
    private Person(String name) {
        this.name = name;
    }

    public void display() {
        System.out.println("Name: " + name + ", Age: " + age);
    }
}

public class ConstructorDemo {
    public static void main(String[] args) throws Exception {
        Class<?> clazz = Person.class;

        // 1. 获取公共构造器 (带有参数)
        Constructor<?> constructor1 = clazz.getConstructor(String.class, int.class);
        Person person1 = (Person) constructor1.newInstance("John", 25);
        person1.display();

        // 2. 获取默认构造器
        Constructor<?> constructor2 = clazz.getConstructor();
        Person person2 = (Person) constructor2.newInstance();
        person2.display();

        // 3. 获取私有构造器
        Constructor<?> constructor3 = clazz.getDeclaredConstructor(String.class);
        constructor3.setAccessible(true); // 解除访问限制
        Person person3 = (Person) constructor3.newInstance("Alice");
        person3.display();

        // 4. 获取所有公共构造器
        Constructor<?>[] constructors = clazz.getConstructors();
        System.out.println("Public constructors:");
        for (Constructor<?> constructor : constructors) {
            System.out.println(constructor.getName());
        }

        // 5. 获取所有构造器（包括私有的）
        Constructor<?>[] declaredConstructors = clazz.getDeclaredConstructors();
        System.out.println("Declared constructors:");
        for (Constructor<?> constructor : declaredConstructors) {
            System.out.println(constructor.getName());
        }
    }
}

// 输出
// Name: John, Age: 25
// Name: null, Age: 0
// Name: Alice, Age: 0
// Public constructors:
// Person
// Person
// Declared constructors:
// Person
// Person
// Person
```



#### 获取类的方法（Method）

- **`getMethod(String name, Class<?>... parameterTypes)`**
  - 获取类的公共方法，包括继承自父类的公共方法。
  - 如果指定的方法不存在，会抛出 `NoSuchMethodException`。
  - 该方法的第一个参数是方法名，后续参数是方法的参数类型（可以是空参数）。
- **`getDeclaredMethod(String name, Class<?>... parameterTypes)`**
  - 获取类的所有方法（包括私有方法和受保护的方法）。
  - 如果指定的方法不存在，会抛出 `NoSuchMethodException`。
- **`getMethods()`**
  - 返回类的所有公共方法（包括继承自父类的公共方法）。
  - 返回的是一个 `Method` 数组，包含该类的所有公共方法。
- **`getDeclaredMethods()`**
  - 返回类的所有方法（包括私有方法、受保护的方法和公共方法），但不包括从父类继承的方法。
  - 返回的是一个 `Method` 数组，包含该类的所有方法。

**示例**

```java
import java.lang.reflect.*;

class Person {
    private String name;
    private int age;

    // 公共构造器
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // 公共方法
    public void display() {
        System.out.println("Name: " + name + ", Age: " + age);
    }

    // 私有方法
    private void privateMethod() {
        System.out.println("This is a private method.");
    }

    // 受保护的方法
    protected void protectedMethod() {
        System.out.println("This is a protected method.");
    }
}

public class MethodDemo {
    public static void main(String[] args) throws Exception {
        // 创建对象实例
        Person person = new Person("John", 25);

        // 1. 获取公共方法
        Class<?> clazz = person.getClass();
        Method method1 = clazz.getMethod("display");  // 获取公共方法
        method1.invoke(person);  // 调用方法

        // 2. 获取私有方法
        Method method2 = clazz.getDeclaredMethod("privateMethod");  // 获取私有方法
        method2.setAccessible(true);  // 解除访问限制
        method2.invoke(person);  // 调用私有方法

        // 3. 获取受保护的方法
        Method method3 = clazz.getDeclaredMethod("protectedMethod");  // 获取受保护的方法
        method3.setAccessible(true);  // 解除访问限制
        method3.invoke(person);  // 调用受保护的方法

       
        // 4. 获取所有方法（包括私有、受保护方法）
        Method[] declaredMethods = clazz.getDeclaredMethods();  // 获取所有方法
        System.out.println("Declared methods:");
        for (Method method : declaredMethods) {
            System.out.println(method.getName());
        }
    }
}

// 输出结果：
// Name: John, Age: 25
// This is a private method.
// This is a protected method.
// Declared methods:
// display
// privateMethod
// protectedMethod
```

#### 获取类的字段（Field）

- **`getField(String name)`**
  - 获取类的公共字段，包括继承自父类的公共字段。
  - 如果指定的字段不存在，会抛出 `NoSuchFieldException`。
  - 只能获取公共字段。
- **`getDeclaredField(String name)`**
  - 获取类的所有字段（包括私有字段、受保护字段和公共字段）。
  - 如果指定的字段不存在，会抛出 `NoSuchFieldException`。
- **`getFields()`**
  - 获取类的所有公共字段（包括继承自父类的公共字段）。
  - 返回一个 `Field` 数组，包含该类的所有公共字段。
- **`getDeclaredFields()`**
  - 获取类的所有字段（包括私有、受保护和公共字段），但不包括从父类继承的字段。
  - 返回一个 `Field` 数组，包含该类的所有字段。

**示例**

```java
import java.lang.reflect.*;

class Person {
    public String name;
    private int age;
    protected String gender;

    // 公共构造器
    public Person(String name, int age, String gender) {
        this.name = name;
        this.age = age;
        this.gender = gender;
    }
}

public class FieldDemo {
    public static void main(String[] args) throws Exception {
        // 创建对象实例
        Person person = new Person("John", 25, "Male");

        // 1. 获取公共字段
        Class<?> clazz = person.getClass();
        Field field1 = clazz.getField("name");  // 获取公共字段
        System.out.println("Public field 'name': " + field1.get(person));  // 获取字段值

        // 2. 获取私有字段
        Field field2 = clazz.getDeclaredField("age");  // 获取私有字段
        field2.setAccessible(true);  // 解除访问限制
        System.out.println("Private field 'age': " + field2.get(person));  // 获取字段值

        // 3. 获取受保护的字段
        Field field3 = clazz.getDeclaredField("gender");  // 获取受保护字段
        field3.setAccessible(true);  // 解除访问限制
        System.out.println("Protected field 'gender': " + field3.get(person));  // 获取字段值

        // 4. 获取所有公共字段（包括从父类继承的公共字段）
        Field[] fields = clazz.getFields();  // 获取所有公共字段
        System.out.println("Public fields:");
        for (Field field : fields) {
            System.out.println(field.getName());
        }

        // 5. 获取所有字段（包括私有、受保护和公共字段）
        Field[] declaredFields = clazz.getDeclaredFields();  // 获取所有字段
        System.out.println("Declared fields:");
        for (Field field : declaredFields) {
            System.out.println(field.getName());
        }
    }
}

// 输出：
// Public field 'name': John
// Private field 'age': 25
// Protected field 'gender': Male
// Public fields:
// name
// Declared fields:
// name
// age
// gender
```



### 字段（Field）

#### 访问对象字段属性

- 获取对象的 `Field` 对象。
- 通过 `Field` 对象访问或修改字段的值。
- 对于 `private`、`protected` 或默认访问级别的字段，使用 `setAccessible(true)` 解除访问限制。

**获取字段**：`public Object get(Object obj) throws IllegalAccessException` 获取对象中某个字段的值。

**获取字段名**：`public String getName()`

**获取字段的数据类型**：`public Class<?> getType()`

**获取访问修饰符**：`public int getModifiers()` 如果多个修饰符一起使用，它们的整数值是通过位 `OR` 运算得出的

- `public`：1
- `private`：2
- `protected`：4
- `static`：8
- `final`：16

**获取访问修饰符的字符串表示**：`Modifier.toString(int modifiers)`

**修改访问性**：`setAccessible(Boolean T)`

**示例**

```java
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;

class Person {
    public String name;        // 公共字段
    private int age;           // 私有字段
    protected String gender;   // 受保护字段
    static String country;     // 静态字段

    // 公共构造器
    public Person(String name, int age, String gender) {
        this.name = name;
        this.age = age;
        this.gender = gender;
    }
}

public class FieldInfoDemo {
    public static void main(String[] args) throws Exception {
        // 创建一个 Person 对象
        Person person = new Person("John Doe", 30, "Male");

        // 获取 Person 类的 Class 对象
        Class<?> clazz = person.getClass();

        // 获取所有字段，包括私有、受保护和公共字段
        Field[] fields = clazz.getDeclaredFields();

        // 遍历所有字段
        for (Field field : fields) {
            // 获取字段名
            String fieldName = field.getName();

            // 获取字段的修饰符
            int modifiers = field.getModifiers();
            
            // 获取修饰符的字符串表示
            String modifierString = Modifier.toString(modifiers);
            
            // 获取字段的值
            // 使用 setAccessible(true) 来允许访问私有字段
            field.setAccessible(true);
            Object fieldValue = field.get(person);

            // 输出字段信息
            System.out.println("Field: " + fieldName + 
                               ", Modifier: " + modifierString + 
                               ", Value: " + fieldValue);
        }
    }
}


// 输出：
// Field: name, Modifier: public, Value: John Doe
// Field: age, Modifier: private, Value: 30
// Field: gender, Modifier: protected, Value: Male
// Field: country, Modifier: static, Value: null
```

#### 修改对象字段

**修改字段**：`public void set(Object obj, Object value) throws IllegalAccessException, IllegalArgumentException` 修改对象中某个字段的值。

```java
import java.lang.reflect.Field;

class Person {
    public String name;       // 公共字段
    private int age;          // 私有字段
    protected String gender;  // 受保护字段
    static String country;    // 静态字段

    // 公共构造器
    public Person(String name, int age, String gender) {
        this.name = name;
        this.age = age;
        this.gender = gender;
    }
}

public class ModifyFieldDemo {
    public static void main(String[] args) throws Exception {
        // 创建一个 Person 对象
        Person person = new Person("John Doe", 30, "Male");

        // 获取 Person 类的 Class 对象
        Class<?> clazz = person.getClass();

        // 获取所有字段，包括私有、受保护和公共字段
        Field[] fields = clazz.getDeclaredFields();

        // 遍历所有字段
        for (Field field : fields) {
            // 获取字段名
            String fieldName = field.getName();

            // 获取字段的修饰符
            int modifiers = field.getModifiers();
            String modifierString = java.lang.reflect.Modifier.toString(modifiers);
            
            // 输出字段信息
            System.out.println("Field: " + fieldName + ", Modifier: " + modifierString + ", Original Value: " + field.get(person));

            // 修改字段的值
            field.setAccessible(true); // 设置字段为可访问
            if (field.getType() == String.class) {
                // 如果是 String 类型，修改字段值
                field.set(person, "Jane Doe");
            } else if (field.getType() == int.class) {
                // 如果是 int 类型，修改字段值
                field.set(person, 35);
            }
            
            // 输出修改后的字段值
            System.out.println("Modified Field: " + fieldName + ", New Value: " + field.get(person));
        }
    }
}
```

### 方法（Method）

#### 访问对象方法属性

**获取方法名**：`public String getName()`

**获取方法的返回值类型**：`public Class<?> getReturnType()`

**获取访问修饰符**：`public int getModifiers()` 如果多个修饰符一起使用，它们的整数值是通过位 `OR` 运算得出的

- `public`：1
- `private`：2
- `protected`：4
- `static`：8
- `final`：16

**获取访问修饰符的字符串表示**：`Modifier.toString(int modifiers)`

**获取方法的形参类型**： `Class<?>[] getParameterTypes()`

**获取方法的形参数组**：`public Parameter[] getParameters()`

- `getName()`：获取参数名称。
- `getType()`：获取参数的类型。

**修改访问性**：`setAccessible(Boolean T)`

**示例**

```java
import java.lang.reflect.Method;
import java.lang.reflect.Parameter;

class Person {
    public String greet(String name, int age) {
        return "Hello, " + name + ". You are " + age + " years old.";
    }

    public void display() {
        System.out.println("This is a display method.");
    }
}

public class ReflectDemo {
    public static void main(String[] args) throws Exception {
        // 获取 Person 类的 Class 对象
        Class<?> clazz = Person.class;

        // 获取 greet 方法
        Method greetMethod = clazz.getMethod("greet", String.class, int.class);

        // 获取方法的参数信息
        Parameter[] parameters = greetMethod.getParameters();

        // 输出参数的详细信息
        System.out.println("Method: " + greetMethod.getName());
        for (Parameter param : parameters) {
            System.out.println("Parameter name: " + param.getName());
            System.out.println("Parameter type: " + param.getType().getName());
        }
    }
}

// 输出：
// Method: greet
// Parameter name: name
// Parameter type: java.lang.String
// Parameter name: age
// Parameter type: int
```



#### 调用对象方法

`public Object invoke(Object obj, Object... args) throws IllegalAccessException, IllegalArgumentException, InvocationTargetException`

**`obj`**:

- 类型：`Object`
- 说明：调用方法的目标对象。对于实例方法，它是目标对象实例；对于静态方法，这个参数可以是 `null`（尽管最好传递 `null`）。

**`args`**:

- 类型：`Object...`
- 说明：方法的实际参数（如果有）。这个参数是一个可变参数，表示调用方法时传入的参数值。如果方法没有参数，`args` 可以是空数组或者不传递任何值。

**`Object`**: 返回调用方法的结果。如果方法是 `void`，则返回 `null`。

**示例**

```java
public class Person {
    private String name;

    public Person(String name) {
        this.name = name;
    }

    // 有返回值的方法
    public String greet(String greeting) {
        return greeting + ", " + name;
    }

    // 无返回值的方法
    public void display() {
        System.out.println("Hello, " + name);
    }
}

import java.lang.reflect.Method;

public class ReflectDemo {
    public static void main(String[] args) throws Exception {
        // 创建 Person 对象
        Person person = new Person("Alice");

        // 获取 Person 类的 Class 对象
        Class<?> clazz = person.getClass();

        // 获取 greet 方法（具有一个 String 参数）
        Method greetMethod = clazz.getMethod("greet", String.class);

        // 调用 greet 方法，传递参数 "Hello"
        String result = (String) greetMethod.invoke(person, "Hello");
        System.out.println("Result from greet method: " + result);

        // 获取 display 方法（没有参数）
        Method displayMethod = clazz.getMethod("display");

        // 调用 display 方法
        displayMethod.invoke(person);
    }
}

// 输出：
// Result from greet method: Hello, Alice
// Hello, Alice

```

### 对象

#### 创建对象

- 通过反射得到的构造器创建对象（ Constructor）

  ```java
  Constructor<MyClass> constructor = MyClass.class.getConstructor();
  MyClass obj = constructor.newInstance();
  ```

  

- 通过类的字节码（Class）来创建对象

  ```java
  MyClass obj = (MyClass) Class.forName("com.example.MyClass").newInstance();
  ```

## 反射的使用场景

Spring 框架的 IOC（动态加载管理 Bean），Spring通过配置文件配置各种各样的bean，你需要用到哪些bean就配哪些，spring容器就会根据你的需求去动态加载，你的程序就能健壮地运行。

Spring通过XML配置模式装载Bean的过程：

- 将程序中所有XML或properties配置文件加载入内存
- Java类里面解析xml或者properties里面的内容，得到对应实体类的字节码字符串以及相关的属性信息
- 使用反射机制，根据这个字符串获得某个类的Class实例
- 动态配置实例的属性

