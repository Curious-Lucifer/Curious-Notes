# C++

## Namespace
- Define Namespace
    ```cpp
    namespace <namespace_name> {
        // variables, fuctions, classes ...
    }
    ```
- Using variables / functions / classes in Namespace
    ```cpp
    <namespace_name>::<identifier>
    ```
- `using` directive
    ```cpp
    using namespace std;
    // any instruction (same scope) in std after this can be done without `std::`

    /* --- OR --- */

    using std::cout;
    // we can use `cout` instead `std::cout`, but for others still need `std::`
    ```


---
## Object Oriented Programming
### Class Definition
```cpp
class MyClass {
    // members with no specifier will be private members
    private:
        // members cannot be accessed from outside the class
    protected:
        // members cannot be accessed from outside the class
    public: 
        // members are accessible from outside the class
};
```

### Class Method
```cpp
class MyClass {
    public:
        void myMethod() {
            cout << "Hello MyClass" << endl;
        }
}

/* --- OR --- */

class MyClass {
    public:
        void myMethod();
}

void MyClass::myMethod() {
    cout << "Hello MyClass" << endl;
}
```

### Object
```cpp
#include <iostream>
#include <string>

using namespace std;

class MyClass {
    int num;
    public:
        int myNum;
        string myString;
        void myMethod() {
            cout << "Hello MyClass" << endl;
        }
        void setNum(int n) {
            num = n;
        }
        int getNum() {
            return num;
        }
};

int main() {
    MyClass myobj;

    myobj.myNum = 123;
    myobj.myString = "WoW";
    cout << myobj.myNum << " " << myobj.myString << endl;
    myobj.myMethod();

    myobj.setNum(456);
    cout << myobj.getNum() << endl;

    return 0;
}
```

### Constructor & Destructor
```cpp
#include <iostream>

using namespace std;

class Car {
    public:
        string brand;
        string model;
        int year;
        Car(string x, string y, int z) {
            brand = x;
            model = y;
            year = z;
        }

        ~Car() {
            cout << "Destroy Car Object !" << endl;
        }
};

int main() {
    Car carObj1("BMW", "X5", 1999);
    Car carObj2("Ford", "Mustang", 1969);

    cout << carObj1.brand << " " << carObj1.model << " " << carObj1.year << endl;
    cout << carObj2.brand << " " << carObj2.model << " " << carObj2.year << endl;
    return 0;
}
```

### Inheritance
```cpp
class Base {
    public:
        int x;
    protected:
        int y;
    private:
        int z;
};

class PublicDerived: public Base {
    // x is public
    // y is protected
    // z is not accessible
};

class ProtectedDerived: protected Base {
    // x is protected
    // y is protected
    // z is not accessible
};

class PrivateDerived: private Base {
    // x is private
    // y is private
    // z is not accessible
};
```

> Multiple Inheritance :  
> `class MyChildClass: public MyClass, public MyOtherClass`


---
## Struct
可以把 struct 看成是 class（跟 C 的 struct 不一樣），比較重要和 class 不一樣的點有

- struct 的成員預設是 public，class 預設是 private
    ```c++
    struct A {
        // 預設是 public，在 sturct 外可以訪問
        char str[0x20];
    }
    ```

    ```c++
    class A {
        // 預設是 private，在 class 外不能訪問
        char str[0x20];
    }
    ```
- struct 繼承的時候預設是 public 繼承，class 預設是 private 繼承
    ```c++
    struct A {

    }

    // 和 struct B: public A 相同
    struct B: A {

    }
    ```

    ```c++
    class A {

    }

    // 和 class B: private A 相同
    class B: A {

    }
    ```


---
## Virtual Function
虛擬函數和一般的 method 不一樣的地方就是如果

```c++
#include <iostream>

using namespace std;

class A {
public:
    void print() {
        cout << "print from A" << endl;
    }
};

class B: public A {
public:
    void print() {
        cout << "print from B" << endl;
    }
};

int main() {
    B b;
    A* a_ptr = &b;

    // print from A
    a_ptr->print();

    return 0;
}
```

那編譯器會用 `a_ptr` 的型別去判定 `a_ptr->print()` 是哪一個 method，因為 `a_ptr` 的型別是 `A`（注意但 `a_ptr` 指向的物件型別是 `B`），所以 `print()` 會 call 到 `A` 的。
但如果用虛擬函數的話

```c++
#include <iostream>

using namespace std;

class A {
public:
    virtual void print() {
        cout << "print from A" << endl;
    }
};

class B: public A {
public:
    virtual void print() override{
        cout << "print from B" << endl;
    }
};

int main() {
    B b;
    A* a_ptr = &b;

    // print from B
    a_ptr->print();

    return 0;
}
```

編譯器就會根據 `a_ptr` 指向的物件型別去判斷 call 哪一個 method

### Virtual Function

不強制子類要實作，如果沒有實作就用父類的，有的話就用子類的

```c++
#include <iostream>

using namespace std;

class A {
public:
    virtual void print() {
        cout << "print from A" << endl;
    }
};

class B: public A {
public:
    virtual void print() override {
        cout << "print from B" << endl;
    }
};

int main() {
    B b;
    A* a_ptr = &b;

    // print from B
    a_ptr->print();

    return 0;
}
```

### Pure Virtual Function

父類不實作，所以父類是純虛擬的不能被實例化，強制子類一定要實作

```c++
#include <iostream>

using namespace std;

class A {
public:
    virtual void print() = 0;
};

class B: public A {
public:
    virtual void print() override{
        cout << "print from B" << endl;
    }
};

int main() {
    B b;
    A* a_ptr = &b;

    // print from B
    a_ptr->print();

    return 0;
}
```


---
## Reference
- [C++ Struct 繼承](https://www.796t.com/content/1548143114.html)
- [C++ Virtual Function](https://shengyu7697.github.io/cpp-virtual/)
- [C++ Vector](https://medium.com/@leonardian14/c-vector-%E7%B0%A1%E5%96%AE%E8%AA%AA%E6%98%8E%E8%88%87%E7%94%A8%E6%B3%95-946c975bd526)
- [C++ new/operator new/placement new](https://blog.csdn.net/qq_26822029/article/details/81213537)
- [C++ new/delete & new[]/delete[]](https://www.cnblogs.com/hazir/p/new_and_delete.html)


