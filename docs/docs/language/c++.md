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
