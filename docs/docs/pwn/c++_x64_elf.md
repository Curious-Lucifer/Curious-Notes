# C++ x64 ELF

## Calling Convention

所有物件的 method 都會把物件放到第一個參數，而後才是 method 本身的參數


---
## Vtable

如果一個 `struct` 有 virtual function

```c++
struct A {
    int a, b;
    void func0() {};
    virtual void func1() {};
    virtual void func2() {};
    virtual void func3() {};
}
```

那這個 struct 在記憶體的 memory 會長

```
| 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 | <- low address
|-------------------------------| 
|         vtable + 0x10         | 
|       b       |       a       | 
```

前 8 bytes 會指向 `A` 的 vtable + 0x10（`this` pointer 會指向這個 struct 也就是放 vtable + 0x10 的地方），然後接著是 struct 中的成員。而普通的 method `func0` 不會在 struct 的 memory 中

`A` 的 vtable 的 memory 會長

```
| 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 | <- low address
|-------------------------------| 
|               0               | 
|            typeinfo           | 
|            A::func1           | 
|            A::func2           | 
|            A::func3           | 
```

首先是 0，然後是一個 pointer 指到 `A` 的 typeinfo。接著（就是從 + 0x10 的位址開始）就是各個 virtual function pointer 的位址

如果有一個 struct 繼承了 `A`

```c++
struct B: A {
    virtual void func2 () override {}
}
```

那 `B` 的 vtable 就會長

```
| 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 | <- low address
|-------------------------------| 
|               0               | 
|            typeinfo           | 
|            A::func1           | 
|            B::func2           | 
|            A::func3           | 
```


---
## Reference
- [Compiler Explorer](https://godbolt.org)
- [x64 Vtable](https://cs.pynote.net/hd/asm/202302231/)
- [Pwning C++](https://www.slideshare.net/slideshow/pwning-in-c-basic/58370781)

