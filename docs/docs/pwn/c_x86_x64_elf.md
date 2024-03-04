# C x86/x64 ELF

## Assembly
### x86
```asm
; test.asm
section .data                 ; (for pwntools' asm)
    msg db "Hello World", 0xa ; .ascii "Hello World"
                              ; .byte 0xa

section .text
    global _start

_start: 
    mov eax, 4
    mov ebx, 1
    mov ecx, msg
    mov edx, 12
    int 0x80

    mov eax, 1
    int 0x80
```

組譯：
```shell
nasm -f elf32 test.asm -o test.o
ld -m elf_i386 test.o -o test
```

### x64
```asm
; test.asm
section .data                 ; (for pwntools' asm)
    msg db "Hello World", 0xa ; .ascii "Hello World"
                              ; .byte 0xa

section .text
    global _start

_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, 12
    syscall

    mov rax, 60
    mov rdi, 0
    syscall
```

組譯：
```shell
nasm -f elf64 test.asm -o test.o
ld test.o -o test
```


---
## Calling Convention
### x86 
- system call

| arg1  | arg2  | arg3  | arg4  | arg5  | arg6  | arg7  |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `eax` | `edx` | `ecx` | `edx` | `esi` | `edi` | `ebp` |

> - Calling Instruction : `int 0x80`
> - Syscall Detail : `man 2 <syscall_name>`
> - [Syscall Table](https://syscalls.w3challs.com/?arch=x86)

- function call

| arg1  |   arg2    |   arg3    |    arg4    |    arg5    | ... |
| ----- | --------- | --------- | ---------- | ---------- | --- |
| stack | stack + 4 | stack + 8 | stack + 16 | stack + 24 | ... |

### x64
- system call

| arg1  | arg2  | arg3  | arg4  | arg5  | arg6  | arg7  | arg8  |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `rax` | `rdi` | `rsi` | `rdx` | `r10` | `r8`  | `r9`  | stack |

> - Calling Instruction : `syscall`
> - Syscall Detail : `man 2 <syscall_name>`
> - [Syscall Table](https://syscalls.w3challs.com/?arch=x86_64)

- function call

| arg1  | arg2  | arg3  | arg4  | arg5  | arg6  | arg7+ |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `rdi` | `rsi` | `rdx` | `rcx` | `r8`  | `r9`  | stack |


---
## JMP Opcode
| Instruction | Opcode | Explanation | 
| --- | --- | --- |
| `jmp <相對位址>` | `EA [ ]` | `[ ]` 填入 `<相對位址>`（1 bytes） |
| `jmp <相對位址>` | `E9 [ ] [ ]` | `[ ] [ ]` 填入 `<相對位址>`（2 bytes） |
| `jmp <相對位址>` | `E9 [ ] [ ] [ ] [ ]` | `[ ] [ ] [ ] [ ]` 填入 `<相對位址>`（4 bytes） |

這邊所有的相對位址都是和 `jmp` 下一個 instruction 的相對位址，而且是有號整數

### Pwntools
我們可以在 `asm` 中使用 `jmp $+<相對位址>`/`jmp $-<相對位址>` 來指定要跳到的位址，這個相對位址也是相對 `jmp` 下一個 instruction 的 address


---
## Controlflow Enforcement Technology (CET)
用來防止 ROP/JOP/COP 這種使用者控制執行流程的手段，主要有 shadow stack 和 indirect branch tracking (IBT) 這兩種機制。目前的 Linux kernel 只支援 userspace 的 shadow stack 和 kernel 的 IBT。

### Shadow Stack
會 allocate 一塊記憶體當作 shadow stack，當 `call` 被呼叫到的時候，return address 會被 push 到普通的 stack 和 shadow stack。當 `ret` 被呼叫到的時候，程式會 pop shadow stack 然後和普通的 stack 去比較，一樣才會正常 return。

### Indirect Branch Tracking (IBT)
如果 `call` 或 `jmp` 被執行到的時候，會把 `TRACKER` 設定成 `WAIT_FOR_ENDBRANCH`。當 `TRACKER` 是 `WAIT_FOR_ENDBRANCH` 的時候，只能執行 `endbr64` 來把 `TRACKER` 設定成 `IDLE`，執行其他 instruction 會直接報錯。


---
## RELRO
- **Partail RELRO** : pointers to `link_map`'s head and `_dl_runtime_resolve()` can be found in `.got.plt + 0x8` and `.got.plt + 0x10`  
- **No RELRO/Full RELRO** : pointer to `link_map`'s head can be found in `r_debug + 0x8`, where pointer to `r_debug` can be found in `.dynamic + 0xc8`

> `link_map` : 
> ```c
> struct link_map
> {
>     ElfW(Addr) l_addr;                // Difference between the address in the ELF file and the addresses in memory.
>     char *l_name;                     // Absolute file name object was found in.
>     ElfW(Dyn) *l_ld;                  // Dynamic section of the shared object.
>     struct link_map *l_next, *l_prev; // Chain of loaded objects.
> 
>     ...
> };
> ```


---
## FMT
- `%<number>$[p/d/x]` : print `<number>` argument use format `[p/d/x]`
- `%<number>$s` : print content of address that (`<number>` argument) point to
- `%<number>$n` : write the length(4 bytes) of the characters that is already displayed on screen to the address `<number>` argument point to
- `%<number>$hn` : same with `%<number>$n` but it write 2 bytes
- `%<number>$hhn` : same with `%<number>$n` but it write 1 byte
- `%<number>c` : print `<number>` of characters to screen


---
## Reference
- [x64 Linux Assembly](https://www.youtube.com/watch?v=VQAKkuLL31g&list=PLetF-YjXm-sCH6FrTz4AQhfH6INDQvQSn&index=1)
- [Finding link_map and _dl_runtime_resolve() under Full RELRO](https://ypl.coffee/dl-resolve-full-relro/)
- [Controlflow Enforcement Technology](https://docs.kernel.org/next/x86/shstk.html)
- [x64 endbr64](https://cs.pynote.net/hd/asm/202302172/)


