# Crypto CTF 2024 Writeup

## Easy

### Mashy

這題就是需要 input 7 組兩個不同的 hex string，然後這兩個 hex string 和一個不知道是啥的 `salt` md5 之後，xor 起來的 hex 要是 `a483b30944cbf762d4a3afc154aad825`。這邊直接猜測可能需要兩個 hex string 的 md5 一樣，這樣 xor 起來就會一直都是 `salt` 的 md5

Solve Script : 

```py
from pwn import *

from CTFLib.Utils import *
from CTFLib.Tools import *

payloads = []
for i in range(8):
    payloads.append(fastcoll(bytes([i])))

r = nc('nc 01.cr.yp.toc.tf 13771')

for i in trange(8):
    r.sendlineafter(b':  \n', payloads[i][0].hex().encode())
    r.sendlineafter(b': \n', payloads[i][1].hex().encode())

r.interactive()
```

Flag : `CCTF{mD5_h4Sh_cOlL!Si0N_CrYp7o_ch41lEnGe!!!}`


---
### Alibos

這題就簡單的模運算

Solve Script : 

```py
from Crypto.Util.number import *

pkey = ...
enc  = ...

d = len(str(enc))

enc = (enc - pkey) % (10 ** d)
m = (pow(d, -2, 10 ** d) * enc) % (10 ** d)

print(long_to_bytes(int(str(m).rstrip('1'))))
```

Flag : `CCTF{h0M3_m4De_cRyp70_5ySTeM_1N_CryptoCTF!!!}`


---
### Beheaded

分析一下 `behead_me.sh`

```shell
#!/bin/bash

source secrets.sh

FLAGS="all_flags.txt"
rm -f "all_flags.enc"

while read flag; do
	magick -background white -fill blue -pointsize 72 -size "$X"x"$Y" -gravity North caption:"$flag" flag.ppm
	tail -n +4 flag.ppm > tail
	openssl enc -aes-256-ecb -pbkdf2 -nosalt -pass pass:"$KEY" -in tail >> "all_flags.enc"
done < "$FLAGS"
```

基本上他就是把 `all_flags.txt` 一行一行讀到 `$flag` 這個變數中，然後用 

```shell
magick -background white -fill blue -pointsize 72 -size "$X"x"$Y" -gravity North caption:"$flag" flag.ppm
```

這個 command 生成一個白底藍字 `$X` x `$Y` 的 `flag.ppm`，其中的文字內容就是剛剛讀的 `$flag`。接著把 `flag.ppm` 的前三行去掉後用 AES ECB 加密整張圖片，然後再附加到 `all_flags.enc` 後面。

首先先確定 PPM 的檔案格式和 `magick` 會生出什麼。用以下的 command 生一張測試的 PPM

```shell
magick -background white -fill blue -pointsize 72 -size "500"x"100" -gravity North caption:"FLAG{test}" ppm-test.ppm
```

看一下生出來的 `ppm-test.ppm`，配合上 [這個網站](https://netpbm.sourceforge.net/doc/ppm.html)，可以知道用 `magick` 生出來的檔案前三行大約會長

```
P6
<width> <height>
65535
```

接下來的資料猜測是 6 bytes 代表一個 pixel，這一個 pixel 又分成 r, g, b 三組各佔兩個 bytes，這兩個 bytes 猜測是一個 byte 重複寫兩次。

用以下的 script 把 PPM 轉成 PNG

```py
from CTFLib.Utils import *
from CTFLib.Misc import *

with open('ppm-test.ppm', 'rb') as f:
    for _ in range(3):
        f.readline()

    buf = f.read()

pixel_list = [(buf[i], buf[i + 2], buf[i + 4]) for i in range(0, len(buf), 6)]
width, height = 500, 100

PNGConverter.list2png(pixel_list, width, height, 'ppm-test.png')
```

看一下轉換出來的 `ppm-test.png`，看起來我的猜測並沒有問題

![](Beheaded/ppm-test.png)

然後再回去看一下 `ppm-test.ppm`，可以發現因為大多數的 pixel 都是白色，所以 `ppm-test.ppm` 的資料大多數都是 `\xff`。

利用這個特點，加上因為是 AES ECB 加密，所以可以知道實際上 `db4e86ff76e9183f97a95d7720dc1d31` 這個 `all_flag.enc` 中的 block 對應的就是 `ffffffffffffffffffffffffffffffff`

至於其餘非 `db4e86ff76e9183f97a95d7720dc1d31` 的 block，可以知道對應的明文不是有混到非白色的 pixel，就是 padding。所以可以先把這些 block 轉成 `00000000000000000000000000000000`

```py
from CTFLib.Utils import *
from CTFLib.Misc import *

with open('all_flags.enc', 'rb') as f:
    cipher = f.read()

white_block_cipher = bytes.fromhex('db4e86ff76e9183f97a95d7720dc1d31')
blocks = [
    b'\xff' * 16 if cipher[i: i + 16] == white_block_cipher else b'\0' * 16
    for i in range(0, len(cipher), 16)
]
plain = b''.join(blocks)
```

接著就是要去識別到底有幾張 `flag.ppm` 被存到 `all_flag.enc` 裡面。

我這邊是假設如果每一張 `flag.ppm` 最前面和最後面都會有一串很長的白色 pixel，然後去算有多少條差不多長的白色 pixel

```py
from CTFLib.Utils import *
from CTFLib.Misc import *

with open('all_flags.enc', 'rb') as f:
    cipher = f.read()

white_block_cipher = bytes.fromhex('db4e86ff76e9183f97a95d7720dc1d31')
blocks = [
    b'\xff' * 16 if cipher[i: i + 16] == white_block_cipher else b'\0' * 16
    for i in range(0, len(cipher), 16)
]
plain = b''.join(blocks)

continuous_white_length = []
count = 0
for num in plain:
    if num != 0xff:
        if count == 0:
            continue
        else:
            continuous_white_length.append(count)
            count = 0

    else:
        count += 1

continuous_white_length.sort(reverse=True)

current = order_of_magnitude(continuous_white_length[0])
for i, length in enumerate(continuous_white_length):
    if order_of_magnitude(length) < current:
        image_num = i // 2
        break

print(len(plain) // 16, image_num)
```

這邊可以知道 `image_num` 是 110，而 `plain` 總共有 6293210 個 block。也就是說每一個 PPM 佔用了 57211 個 block，可能會有 152562、152561 或 152560 個 pixel，把他們都分解一下

```
152562 : 2 * 3 * 47 * 541
152561 : 41 * 61 ** 2
152560 : 2 ** 4 * 5 * 1907
```

如果都嘗試一下就可以發現當 `width, height = 3 * 541, 2 * 47` 的時候轉換出來的圖片是對的

可以看到有一堆 fake flag，找到沒有 `FAKE_FLAG` 的就是 flag 了

![](Beheaded/flag-40.png)

Solve Script : 

```py
from CTFLib.Utils import *
from CTFLib.Misc import *

with open('all_flags.enc', 'rb') as f:
    cipher = f.read()

# Decrypt
white_block_cipher = bytes.fromhex('db4e86ff76e9183f97a95d7720dc1d31')
blocks = [
    b'\xff' * 16 if cipher[i: i + 16] == white_block_cipher else b'\0' * 16
    for i in range(0, len(cipher), 16)
]
plain = b''.join(blocks)


# Get Pixture Number
continuous_white_length = []
count = 0
for num in plain:
    if num != 0xff:
        if count == 0:
            continue
        else:
            continuous_white_length.append(count)
            count = 0

    else:
        count += 1

continuous_white_length.sort(reverse=True)

current = order_of_magnitude(continuous_white_length[0])
for i, length in enumerate(continuous_white_length):
    if order_of_magnitude(length) < current:
        image_num = i // 2
        break


width, height = 3 * 541, 2 * 47
images = [
    plain[j: j + len(plain) // image_num]
    for j in range(0, len(plain), len(plain) // image_num)
]
for i, image in enumerate(images):
    pixel_list = [(image[i], image[i + 2], image[i + 4]) for i in range(0, width * height * 6, 6)]
    PNGConverter.list2png(pixel_list, width, height, f'flag/flag-{i}.png')
```

Flag : `CCTF{i_LOv3_7He_3C8_cRypTo__PnNgu1n!!}`


---
## Medium
### RM2

這題就是需要找兩個質數 `p` 和 `q`，然後 server 會用 `(e, (p - 1) * (q - 1))` 和 `(e, (2 * p + 1) * (2 * q + 1))` 這兩把公鑰來加密兩段 secret。其實主要這題就是找兩個 `p, q` 減一之後是平滑的且 `2 * p + 1, 2 * q + 1` 都是質數。

Solve Script - Get Primes : 

```py
from functools import reduce
from time import time

from CTFLib.Crypto import *
from CTFLib.Utils import *


count = 0
p_list = []
p_prime_list = []

attempts = 0
start = time()
while True:
    prime_list = [2] + [fastGetPrime(16) for _ in range(63)]
    pp = reduce(lambda x, y: x * y, prime_list)
    while True:
        prime = fastGetPrime(1024 - (pp + 1).bit_length())
        if (pp * prime + 1).bit_length() == 1024:
            prime_list.append(prime)
            p = pp * prime + 1
            break

    attempts += 1
    if (attempts % 10000) == 0:
        info(f'Attempts : {attempts} , Time : {int(time() - start)}s')

    if fastIsPrime(p) and fastIsPrime(2 * p + 1):
        success('Find `p` satisfy `p - 1` is smooth && `2 * p + 1` is prime')
        p_list.append(p)
        p_prime_list.append(prime_list)
        count += 1

    if count == 2:
        print(p_list)
        print(p_prime_list)
        break
```

Solve Script - Get Flag : 

```py
from functools import reduce

from pwn import *

from CTFLib.Utils import *
from CTFLib.Crypto import *


p, q = 101467603600533253533749743975646364844173598577648400138336797600783818213363258921863013380811248995724695874802825719336820459857060438619096706747567187198506819574079738237272881359908029674632388215610621308365297055329415011351828866884588427281606068043971544928833780593896455462105646419558180515303, 108168561301201300728399062968410555470575683686985403584819961865787855097422831813235839935077911239327521506183092740640673693028762694586788262735865402280069179620903251128434451951607438251720571146188670924433019947809471926130248350364116014623228188944456833831401234990556066423932597797085794109579
p_minus_1_factor, q_minus_1_factor = [2, 44683, 56591, 53891, 60913, 43987, 59419, 65437, 37571, 55733, 39791, 45979, 57283, 43319, 60679, 57601, 57149, 58363, 37511, 56783, 34213, 62347, 34667, 36299, 49411, 44741, 48679, 34429, 40879, 58147, 48079, 47843, 33083, 61141, 59219, 35753, 56963, 58057, 33071, 33349, 64217, 45389, 51437, 52837, 51439, 63397, 56209, 51913, 59627, 50077, 42023, 44959, 41263, 35543, 59243, 37361, 46153, 62701, 47111, 34253, 58403, 47417, 40543, 59399, 4145982413407], [2, 36821, 50287, 37123, 40883, 37447, 55889, 39163, 48413, 60103, 51461, 51199, 37117, 45341, 62851, 52433, 46051, 34039, 52363, 46099, 43793, 57191, 39607, 43963, 44879, 62801, 56101, 62099, 46643, 39727, 50459, 39341, 61057, 40531, 53597, 36241, 39157, 43037, 44851, 63793, 50587, 34297, 42643, 54331, 51631, 57097, 41603, 46229, 35317, 44753, 43313, 38671, 59663, 49429, 54377, 56999, 63809, 44267, 60689, 33343, 62311, 50461, 39367, 39317, 26060857320569]

factors = mullist2powlist(p_minus_1_factor + q_minus_1_factor)
phi1 = 1
for factor, nth in factors:
    phi1 *= (factor - 1) * (factor ** (nth - 1))
phi2 = 2 * p * 2 * q
d1 = pow(65537, -1, phi1)
d2 = pow(65537, -1, phi2)

r = nc('nc 00.cr.yp.toc.tf 13371')

r.sendlineafter(b':\n', (str(p) + ',' + str(q)).encode())

c1 = int(r.recvline().strip().split(b'= ')[1])
c2 = int(r.recvline().strip().split(b'= ')[1])
m1 = pow(c1, d1, (p - 1) * (q - 1))
m2 = pow(c2, d2, (2 * p + 1) * (2 * q + 1))

r.sendlineafter(b': \n', long_to_bytes(m1) + long_to_bytes(m2))

r.interactive()
```

Flag : `CCTF{i_l0v3_5UpeR_S4fE_Pr1m3s!!}`


---
### Joe-19
這題就是需要找出四個由自然底數 `e` 的小數中連續的數字組成的 512 bits 質數且是 `n` 的因數。

Solve Script : 

```py
import mpmath
from Crypto.Util.number import *

from CTFLib.Utils import *
from CTFLib.Crypto import *


n = ...
c = ...

length = 10000000
mpmath.mp.dps = length
e_value = str(mpmath.e)[2:]

factors = []
i, j = 0, 1
while True:
    if (i % 10000) == 0:
        info(f'Head : {i}')

    if int(e_value[i:j]).bit_length() < 512:
        j += 1
        continue
    if int(e_value[i:j]).bit_length() > 512:
        i += 1
        continue

    if fastIsPrime(int(e_value[i:j])):
        p = int(e_value[i:j])
        if ((n % p) == 0) and (p not in factors):
            factors.append(p)
            success(f'Find n\'s factor')
    i += 1

    if len(factors) == 4:
        break


phi = reduce(lambda x, y: x * y, [factor - 1 for factor in factors])
d = pow(0x10001, -1, phi)
m = pow(c, d, n)

print(long_to_bytes(m))
```

Flag : `CCTF{ASIS_h1r3_7aL3nT5_t0_cO1La8orAt3_!N_Crypto_CTF!}`


---
### Soufia

這題是要解一個方程式 

```
f(t * x) + t * f(x) = f(f(x + y))
```

其中 `t` 是一個常數，然後他還會給兩個初始條件，其中一個是 `f(0) = f_0`，另一個是 `f(a) = f_a` 其中 `f_0` `a` `f_a` 都不固定。

假設 `x = 0` 的話

```
f(0) + t * f(x) = f(f(x))
```

因為 `f` 的值域是整數，所以可以假設對於任何一個 `c`，一定存在 `b` 讓 `f(b) = c`，所以

```
f(0) + t * c = f(c)
```

由此可以透過一開始給的初始條件來算出 t，接著就是帶入求解了

Solve Script : 

```py
from pwn import *

from CTFLib.Utils import *

r = nc('nc 00.cr.yp.toc.tf 13377')
r.recvlines(4)

f_0 = int(r.recvline().strip().split()[4][:-1])

result = r.recvline().strip().split()
a = int(result[2][2:-1])
f_a = int(result[4])

t = (f_a - f_0) // a

for i in trange(20):
    r.recvline()
    x = int(r.recvline().strip().split()[4][2:-2])
    r.sendline(str(f_0 + t * x).encode())

r.interactive()
```

Flag : `CCTF{A_funCti0nal_3qu4tiOn_iZ_4_7yPe_oF_EquAtioN_tHaT_inv0lVe5_an_unKnOwn_funCt!on_r4tH3r_thAn_juS7_vArIabl3s!!}`


