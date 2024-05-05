# C

## Variable Scope

- nested block
    ```c
    {
        // OUTER BLOCK
        {
            // INNER BLOCK
            // contents of OUTER BLOCK can be access here
        }
        // contents of INNER BLOCK are not accessible here
    }
    ```
- different block
    ```c
    {
        // BLOCK 1
        // contents of BLOCK 2 cannot be access here
    }

    {
        // BLOCK 2
        // contents of BLOCK 1 cannot be access here
    }
    ```
- global scope
    ```c
    // all global variables are declared here

    type function1() {
        // all global variables can be access inside function1
    }

    type function2() {
        // all global variables can be access inside function2
    }
    ```


---
## Structure & Union
### Structure

```c
#include <stdio.h>
#include <string.h>

// Memory Size : 0x34 bytes
struct Book {
    // 0x00 - 0x04
    int id;

    // 0x04 - 0x34
    char book_name[0x30];
} book2;

/*
struct {
    ...
} struct_var1, struct_var2, ...;
*/

int main() {
    struct Book book1 = {0, "Harry Potter"};

    printf("Book Info : %d %s\n", book1.id, (&book1)->book_name);
    // output : Book Info : 0 Harry Potter

    book2 = book1;

    book2.id = 1;
    strcpy(book2.book_name, "The Lord of the Rings");

    printf("Book Info : %d %s\n", book1.id, book1.book_name);
    // output : Book Info : 0 Harry Potter
    printf("Book Info : %d %s\n", book2.id, book2.book_name);
    // output : Book Info : 1 The Lord of the Rings

    return 0;
}
```

### Union
```c
#include <stdio.h>

// Memoery Size : 4 bytes (determined by the largest member)
union Var {
    char chr;
    int num;
} var2; 

int main(void) {
    // We can only initialize the first member
    // `union Var var1 = {1234};` is wrong
    union Var var1 = {'x'};
    
    printf("Var1 Data : %c %d\n", var1.chr, var1.num); 
    
    var2 = var1;
    var2.num = 0x12345678;

    printf("Var1 Data : %c %d\n", var1.chr, var1.num);
    printf("Var2 Data : %c %d\n", var2.chr, var2.num);
    
    return 0;
    
}
```


---
## Stream Buffering
### Buffering Strategies

- *fully buffered* : Characters written to or read from a fully buffered stream are transmitted to or from the file in blocks of arbitrary size (most newly opened streams)
- *line buffered* : Characters written to a line buffered stream are transmitted to the file in blocks when a newline character is encountered (`stdin`, `stdout`)
- *unbuffered* : Characters written to or read from an unbuffered stream are transmitted individually to or from the file (`stderr`)

### Specify Buffering Strategies
```c
#include <stdio.h>

// int setvbuf(FILE *stream, char *buf, int mode, size_t size);
//   stream : stream that we are going to set
//   buf : if it's null pointer, setvbuf will malloc for it, and close when stream closed
//   mode : _IOFBF for fully buffered, _IOLBF for line buffered, _IONBF for unbuffered
//   size : size of buffer
setvbuf(stdout, 0, _IONBF, 0);
```

### Flushing Buffers
some circumstances when buffered output on a stream is flushed automatically :

- When you try to do output and the output buffer is full
- When the stream is closed
- When the program terminates by calling `exit`

```c
#include <stdio.h>

// int fflush(FILE *stream)
//   stream : output stream that we want to flush, if stream is null pointer, than flush all open output streams
```


---
## Preprocessor
### Comments & continued lines
- Merge continued lines (line that end with backslash) to a long line (this will remove the backslash and new line symbol)
- Replace all comments to single space

### Header Files
- remove the include directive and insert the preprocess result of `file_name`
    ```c
    // Use for include system header files
    // It will search for the file named `file_name` in the standard list of system directories
    #include <file_name>

    // Use for include header files
    // It will search for the file named `file_name` first in the current directory, then the standard list of system directories
    #include "file_name"
    ```

### Macros
- Object-like macros : replace the macros follow by the definition to the defined code fragment (the body after `<macro_name>` to the end of the `#define` line, and remove leading and trailing whitespace, replace multiple space to a single space)
    ```c
    #define <macro_name> <code_fragment>

    /* let the closest `#define <macro_name> ...` (before this directive) lose effectiveness */
    /* well just for scope after this directive */
    #undef <macro_name>
    ```
- Function-like macros
    ```c
    #define lang_init() c_init()
    // lang_init() -> c_init()

    #define min(X, Y) ((X) < (Y) ? (X) : (Y))
    // x = min(a, b); -> x = (((a) < (b) ? (a) : (b)));

    #define str(s) #s
    // str(p = "bla\n") -> "p = \"bla\\n\""

    #define FUNC(NAME) { #NAME, NAME ## _func }
    // FUNC(quit) -> {"quit", quit_func}
    ```

### Conditionals
- `ifdef` / `ifndef`
    ```c
    #ifdef <MACRO>

    #endif /* MACRO */

    /* --- OR --- */

    #ifndef <MACRO>

    #endif /* NO MACRO */
    ```
- `if` / `defined` / `elif` / `else`
    ```c
    #if <C Expression Of Integer Type>

    #endif /* Expression */

    /* --- OR --- */

    #if defined <MACRO> && <C Expression Of Integer Type>

    #endif /* MACRO && Expression */

    /* --- OR --- */

    #if <Expression1>

    #elif <Expression2>

    #else /* !(Expression1) && !(Expression2) */

    #endif /* !(Expression1) && !(Expression2) */
    ```


---
## GCC
- `gcc -E <source code> -o <output file>` : preprocess source code to output file
- `gcc -S <source code> -o <output file>` : preprocess & compile source code to output file
- `gcc -c <source code> -o <output file>` : preprocess & compile & assemble source code to output file
- `gcc -shared <source code> -o <share object>` : compile source code to share object, if any standard lib’s function has used, add `-fno-builtin-<func_name>`



---
## Reference
- [Stream Buffering](https://www.gnu.org/software/libc/manual/html_node/Stream-Buffering.html)
- [C Preprocessor](https://gcc.gnu.org/onlinedocs/cpp/index.html)
- [C++ Template](https://www.rocksaying.tw/archives/3641717.html)
- [C #pragma Usage](https://blog.csdn.net/liuchunjie11/article/details/80502529)
