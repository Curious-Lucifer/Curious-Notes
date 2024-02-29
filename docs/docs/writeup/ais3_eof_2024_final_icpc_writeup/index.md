# AIS3 EOF 2024 Final - ICPC Writeup
## 題目
ICPC 總共有 4 個小題，每一個小題都會給你一個任務，然後需要你寫一段 shellcode 來解決的這小任務，而且每一隊都可以 ban 一個 byte。如果 0xc3 被第 7 隊 ban 了，那除了第 7 隊以外的隊伍下一 round 的 shellcode 就不能有 0xc3 在裡面。其他的一些限制像是 Time limit、Memory limit 或 shellcode 長度限制基本上都不會碰到，所以就不多說。

因為總共有 9 隊 + 一隊 NPC，所以每一個 round 最多會被 ban 8 個不同的 bytes。

以下是 ICPC 的 4 個小題

### A + B Problem
他會把 `A` 放到 `rdi` `B` 放到 `rsi`，然後需要把 `A + B` 的結果放到 `rax`

`grader1.c` : 
```c
/*
build in a ubuntu:22.04 docker container with:
$ apt update && apt install -y build-essential binutils
$ gcc /usr/src/grader.c -o /usr/bin/grader
$ strip /usr/bin/grader
*/

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

void *load_shellcode(const char *filename) {
    void *addr = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC,
                      MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
    assert(addr != MAP_FAILED);
    FILE *shellcode = fopen(filename, "r");
    fread(addr, 1, 0x1000, shellcode);
    assert(ferror(shellcode) == 0);
    fclose(shellcode);
    return addr;
}

int main(int argc, char **argv) {
    long long (*a_plus_b)(long long, long long) = load_shellcode(argv[1]);
    long long a, b;
    scanf("%lld%lld", &a, &b);
    long long c = a_plus_b(a, b);
    printf("%lld\n", c);
}
```


### Find Range
他會把 `n` 個 64 bits 的數字放到 `a[0]` ~ `a[n - 1]`，其中 `n` 放到 `rdi`，`a` 的位址放到 `rsi`，需要我們找到 `n` 個數字中的最大值減最小值然後結果放到 `rax`

`grader2.c` : 
```c
/*
build in a ubuntu:22.04 docker container with:
$ apt update && apt install -y build-essential binutils
$ gcc /usr/src/grader.c -o /usr/bin/grader
$ strip /usr/bin/grader
*/

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

void *load_shellcode(const char *filename) {
    void *addr = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC,
                      MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
    assert(addr != MAP_FAILED);
    FILE *shellcode = fopen(filename, "r");
    fread(addr, 1, 0x1000, shellcode);
    assert(ferror(shellcode) == 0);
    fclose(shellcode);
    return addr;
}

int main(int argc, char **argv) {
    long long (*find_range)(long long, long long *) = load_shellcode(argv[1]);
    long long n;
    scanf("%lld", &n);
    long long a[n];
    for (int i = 0; i < n; i++) {
        scanf("%lld", &a[i]);
    }
    long long ans = find_range(n, a);
    printf("%lld\n", ans);
}
```


### A + B Revenge
他會把兩個很長的數字字串放到 `rdi` 和 `rsi`，然後你要把他們加起來去掉頭部的 0 然後放到 `rax`

`grader3.c`
```c
/*
build in a ubuntu:22.04 docker container with:
$ apt update && apt install -y build-essential binutils
$ gcc /usr/src/grader.c -o /usr/bin/grader
$ strip /usr/bin/grader
*/

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

void *load_shellcode(const char *filename) {
    void *addr = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC,
                      MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
    assert(addr != MAP_FAILED);
    FILE *shellcode = fopen(filename, "r");
    fread(addr, 1, 0x1000, shellcode);
    assert(ferror(shellcode) == 0);
    fclose(shellcode);
    return addr;
}

int main(int argc, char **argv) {
    void (*a_plus_b)(char *, char *, char *) = load_shellcode(argv[1]);
    char a[1001] = {}, b[1001] = {}, c[1002] = {};
    scanf("%1000s%1000s", a, b);
    a_plus_b(c, a, b);
    printf("%1001s\n", c);
}
```


### String Sorting
他會給 `n` 個 strings 到 `s[0]` ~ `s[n - 1]`，每一個都是由 a ~ z 組成，我們需要按照字典序把字串排序

`grader4.c`
```c
/*
build in a ubuntu:22.04 docker container with:
$ apt update && apt install -y build-essential binutils
$ gcc /usr/src/grader.c -o /usr/bin/grader
$ strip /usr/bin/grader
*/

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

void *load_shellcode(const char *filename) {
    void *addr = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC,
                      MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
    assert(addr != MAP_FAILED);
    FILE *shellcode = fopen(filename, "r");
    fread(addr, 1, 0x1000, shellcode);
    assert(ferror(shellcode) == 0);
    fclose(shellcode);
    return addr;
}

char strs[128 * 100];
int main(int argc, char **argv) {
    void (*sort_str)(long long, char *) = load_shellcode(argv[1]);
    long long n;
    scanf("%lld", &n);
    for (int i = 0; i < n; i++) {
        scanf("%s", &strs[128 * i]);
    }
    sort_str(n, strs);
    for (int i = 0; i < n; i++) {
        printf("%s\n", &strs[128 * i]);
    }
}
```


---
## 解法 & 小記
比賽開啟這題的時候我剛好在修分析封包的工具，所以就沒有第一時間去摸這題，那時候想說一開始應該大家都會解不出來，晚幾個 round 應該還好。雖然其他隊友有稍微摸一下這題，也拿到了首殺，但之後所有隊伍都開始懂這題要幹嘛，然後各種正常 shellcode 會出現的 bytes 也都被 ban 掉，我們這隊就沒有在這題繼續拿分了。等到我來看這題的時候已經幾乎沒有人解出來了。

之後就跟 Caleb 開始翻 [x86 & x64 Instruction Reference](https://www.felixcloutier.com/x86/) 和瘋狂用 [Online Assembler](https://defuse.ca/online-x86-assembler.htm)，找到一些酷酷的指令，也有成功繞過別隊的 ban bytes，但這就僅限於第一題 A + B，後面的題目都沒有寫出來。

第一天結束後回房間跟 Aukro 開始研究前三題（第四題是第二天下午才開），因為我有成功繞過 ban bytes，所以我就想說先把前三題都寫完，然後繞一繞 ban bytes，而且我還真的寫出來了。後來 Aukro 有想到可以用 AVX-512 和用 libc 的東西，但因為怕不知道會不會被 sandbox ban 或是一些奇怪的偵測擋所以就沒有用。

第二天開賽後我們大概拿了 7 輪的第三題（整場好像第三題只有我們解出來過，而且原本好像測資錯了，後來跟主辦方確認才重新測一遍），之後就是 Aukro 在盯著第一題看看哪些 bytes 被 ban 然後趕快改 shellcode。然後因為第二題 `ret` 的 `0xc3` `0xc2`、`call`、`jmp` 都被 ban 掉，沒有辦法正常控 `rip`，所以我開始想辦法把 shellcode 混淆，一開始是先用 `lea` 拿到 `rip` 然後去 `xor` 把 shellcode 的最後面改成 `ret`，後來因為 shellcode 中很多其他 bytes 都被 ban 掉，所以我就想說應該要寫一個自動（或是半自動）的混淆器。

寫一寫寫一寫第四題就開放了，但我還在寫混淆器，所有我們又双叒叕錯過了一開始沒什麼人 ban 的 round。

在比賽剩兩到三個小時我把混淆器寫好了，在第三題拿到了幾 round 的分，之後 `lea` 就被 ban 掉，我就想不到要怎麼拿到 shellcode 的 address，所以我就轉戰第四題。最後在 160 round 的時候（剛好在這個時候公布只打到 163 round）把第四題寫完 + 調整完混淆器，然後我們也手動測試了大致上沒什麼問題。但但但但但但上傳之後第一個測資就是 Segment Fault，所以我們又手動生了幾筆很大的測資，想說應該是比較大的測資造成 Segment Fault，但測出來都很正常，就這樣最後 3 個 round 就過了。

賽後我跑去問出題者為啥會錯，結果發現原來是因為沒有考慮到 n = 1 的情況，我只能說 %#$!^@#%

大概再過了一個禮拜之後，我重新看了一下發現，其實並不一定要 `lea` 才可以拿到 shellcode 的 address，因為 call shellcode 的時候會用到 `call rdx` 之類的 instruction，所以 `rdx` 本來就有 shellcode 的 address，這樣就可以從 `rdx` 下手。因此我就整理了一下賽中寫的混淆器，把他寫的更完整然後更自動化一點。目前混淆器還有幾個比較明顯的問題，就是如果 ban 到 `0x4d` 或是 `0x80` 這個混淆器就會爛掉，`0x4d` 是在 `lea r8, [r8 + 0x7f]` 之類的會用到，`0x80` 是在 `xor byte ptr [r8 + 0x12], 1` 會被用到，這兩個其實都沒有很難繞，主要是我想要偷懶，所以就懶得動了。


---
## Solve Repo
[Link](https://github.com/Curious-Lucifer/AIS3_EOF_2024_Final_ICPC)