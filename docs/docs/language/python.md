# Python

## Scope & Namespace
### Namespace
namespace is a space that stores how name map to the object, most namespaces are now implemented as `dict`

**Common Namespace :**

- set of built-in names
- global names in a module
- local names in a function invocation
- set of attributes of an object

### Scope
scope is a textual region of python program where a namespace is directly accessible. At any time during execution, there are nested scopes whose namespaces are directly accessible

**Scope Search Order :**

1. innermost scope, contains the local names
2. any enclosing functions’ scope, searched starting with the nearest enclosing scope
3. next-to-last scope, contains the current module’s global names
4. outermost scope, contains the built-in names

> For name is declared by `global`, then all references and assignments go directly to the next-to-last scope containing the module’s global names
> 
> For name is declared by `nonlocal`, then this name will bind with the nearest variable outside of the innermost scope
> 
> For those names that do not belong to the innermost scope, they are read-only

---
## Class
### Class Object
**Class Definition :** when a class definition is entered, a new namespace is created, and used as the local scope. when a class definition is left, a class object is created

```python
class MyClass:
    "Here's your class' docstring"
    i = 10
    
    def f(self):
        return 'Hello World!'

# we can use MyClass.<name> to access the namespace in MyClass definition
# ex. MyClass.i, MyClass.f, MyClass.__doc__
```

### Instance Object
**Class Instantiation :**

```python
class Complex:
    def __init__(self, real, imag):
        self.r = real
        self.i = imag

# class instantiation automatically invokes __init__() for the newly created class instance
x = Complex(3, 4)

# now x.r == 3 and x.i == 4
# the namespace of x (Instance Object) will be nested in the namespace of Complex (Class Object)
# we can use x.__class__ to access Complex
```

### Method Object
When a non-data attribute of an instance is referenced, and the name is a valid class attribute that is a function object, then a method object is created by packing the instance object and the function object just found together in an abstract object

```python
class MyClass:
    def f(self):
        # the local namespace here well be nested in the module global namespace
        return 'Hello World!'

x = MyClass()
# x : <__main__.MyClass object at 0x100826b10>
# MyClass.f : <function MyClass.f at 0x10081cb80>
# x.f : <bound method MyClass.f of <__main__.MyClass object at 0x100826b10>>

# call x.f() is same as MyClass.f(x)
print(x.f())

# x.f.__self__ : the object that bound with MyClass.f (in this case is x)
# x.f.__func__ : the function object corresponde to the method (in this case is MyClass.f)
```

---
## Class Inheritance
### Inheritance
**Attribute Reference :** if a requested attribute or method is not found in the class, the search proceeds to look in the MRO of the class

```python
class DerivedClass(BaseClass1, BaseClass2):
    <statement1>
    <statement2>
    ...

# use `isinstance(object, class_name)` to see if object.__class__ is class_name or it's subclass
# use `issubclass(class_name1, class_name2)` to see if class_name1 is class_name2's subclass

# `class ClassName:` is same as `class ClassName(object):`
```

### Method Resolution Order
C3 Algorithm

> Shortcut Notation :
> 
> - $C_1C_2…C_N$ = [$C_1$, $C_2$, ..., $C_N$]
> - head of $C_1C_2…C_N$ = $C_1$
> - tail of $C_1C_2…C_N$ = $C_2C_3…C_N$
> - $C$ + $C_1C_2…C_N$ = $CC_1C_2…C_N$

Consider a class $C$ inheriting from the base classes $B_1$, $B_2$, ..., $B_N$, calculate the linearization $L[C]$ of the class $C$

1. calc $L[B_1]$, $L[B_2]$, ..., $L[B_N]$
2. calc $\operatorname{merge}(L[B_1], L[B_2], …, L[B_N], B_1B_2…B_N)$
3. $L[C]$ = $C$ + $\operatorname{merge}(L[B_1], L[B_2], …, L[B_N], B_1B_2…B_N)$

calc $\operatorname{merge}(L[B_1], L[B_2], …, L[B_N], B_1B_2…B_N)$ : 

1. take the head of the first arg
2. if this head is not in the tail of other args, then add this head to the answer list and remove it from every args
3. else take the head of the second, third, ... arg and go to 2, if there’s no any valid head then raise an exception
4. repeat 1 ~ 3 until all the class are remove from args

Ex.

```python
O = object
class F(O): pass
class E(O): pass
class D(O): pass
class C(D,F): pass
class B(D,E): pass
class A(B,C): pass
```

```
L[O] = O
L[D] = D O
L[E] = E O
L[F] = F O
```

```
L[B] = B + merge(DO, EO, DE)
     = B + D + merge(O, EO, E)
     = B + D + E + merge(O, O)
     = B + D + E + O
     = B D E O
L[C] = C D F O
```

```
L[A] = A + merge(BDEO, CDFO, BC)
     = A + B + merge(DEO, CDFO, C)
     = A + B + C + merge(DEO, DFO)
     = A + B + C + D + merge(EO, FO)
     = A + B + C + D + E + merge(O, FO)
     = A + B + C + D + E + F + merge(O, O)
     = A + B + C + D + E + F + O
     = A B C D E F O
```

```python
# Use this to see the mro of A
A.mro()
# (<class '__main__.A'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.D'>, <class '__main__.E'>, <class '__main__.F'>, <type 'object'>)
```

---
## Class Property
### Name Mangling
Change any identifier of the form `__<name>` to `_<class_name>__<name>` in class

```python
class MyClass:
    __name = "Curious"

print(MyClass._MyClass__name)
```


---
## Reference
- [Python Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python Method Resolution Order](https://www.python.org/download/releases/2.3/mro/)

