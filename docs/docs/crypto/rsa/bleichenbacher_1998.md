# Bleichenbacher 1998

if there's an oracle that give it $c$, it will tells you if the $m$'s highest two bytes is `0x0002` (PKCS#1). 

let $2^{8(k-1)} \le n \lt 2^{8k}$, $B = 2^{8(k-2)}$, if the oracle tells $m$ is PKCS conforming, that means 

$$
2 \cdot B \le m \lt3 \cdot B
$$


---
## Algorithm

> let $M_i$ be a set of intervals that $m_0 \in M_i$

### step 1

given an cipher $c$, randomly choose $s_0$ to let $(c{s_0}^e \pmod n)$'s plain is PKCS conforming, then set $c_0 = c(s_0)^e \pmod n$, $M_0 = [2B, 3B-1]$, $i = 1$

### step 2

if $i = 1$, because for any $s_1 \le \frac{n}{3B}$, $s_1m_0$ will not be PKCS conforming, so search for the smallest integer $s_1 \gt \frac{n}{3B}$, let $s_1m_0$ is PKCS conforming.

if $i \gt 1$ and the number of intervals in $M_{i-1}$ is at least 2, then search for the smallest integer $s_i \gt s_{i-1}$ let $s_im_0$ is PKCS conforming.

if $i \gt 1$ and $M_{i-1} = [a, b]$, then choose small integer $r_i, s_i$ such that

$$
r_i \ge 2 \frac{bs_{i-1} - 2B}{n}
$$

and 

$$
\frac{2B + r_in}{b} \le s_i \lt \frac{3B + r_in}{a}
$$

because $a \le m_0 \le b$, so

$$
\frac{2B + r_in}{b} \le \frac{2B + r_in}{m_0} \le s_i \le \frac{3B - 1 + r_in}{m_0} \le \frac{3B-1+r_in}{a}
$$

use these $s_i$ until $s_im_0$ is PKCS conforming

### step 3

after $s_i$ has been found, set

$$
M_i = \bigcup_{[a,b] \in M_{i-1},\space r_i} \{[\space\operatorname{max}(a,\space\lceil \frac{2B + r_in}{s_i} \rceil),\space\operatorname{min}(b, \space\lfloor \frac{3B - 1 + r_in}{s_i} \rfloor)\space]\}
$$

and for $[a, b] \in M_{i-1}$

$$
\frac{as_i - 3B + 1}{n} \le r_i \le \frac{bs_i - 2B}{n}
$$

because

$$
\begin{aligned}
& 2B \le s_im_0 \pmod n \le 3B - 1\\
\Rightarrow \space & 2B \le s_im_0-r_in \le 3B - 1 \\
\Rightarrow \space & 2B + r_in \le s_im_0 \le 3B - 1 + r_in \\
\Rightarrow \space & \lceil \frac{2B + r_in}{s_i} \rceil \le m_0 \le \lfloor \frac{3B - 1 + r_in}{s_i} \rfloor
\end{aligned}
$$

and for every $[a, b] \in M_{i-1}$, we know that $2B \le s_im_0 - r_in \le 3B - 1$, so 

$$
as_i - (3B - 1) \le r_in \le bs_i - 2B
$$

$$
M_i = \bigcup_{[a,b] \in M_{i-1},\space r_i} \{[\space\operatorname{max}(a,\space\lceil \frac{2B + r_in}{s_i} \rceil),\space\operatorname{min}(b, \space\lfloor \frac{3B - 1 + kn}{s_i} \rfloor)\space]\}
$$

### step 4

if $M_i$ contains only one interval and $M_i = [a,a]$, then $m_0 = a$, $m \equiv {s_0}^{-1}a \pmod n$, else go back to step 2


---
## Code

```python
def bleichenbacher_1998(n: int, e: int, c: int, oracle):
    """
    - input : `n (int)`, `e (int)`, `c (int)`, `oracle (func)` , `c` is PKCS#1 conforming
    - output : `m (int)` , `e`'s plain
    - oracle func : 
        - input : `c (int)`
        - output : `PKCS_conforming (bool)` , is `c` PKCS#1 conforming
    """

    assert oracle(c)
    B = 1 << (n.bit_length() // 8 - 1) * 8

    def bleichenbacher_orifind_s(lower_bound: int):
        si = lower_bound
        while True:
            new_c = (pow(si, e, n) * c) % n
            if oracle(new_c):
                return si
            si += 1

    def bleichenbacher_optfind_s(prev_si: int, a: int, b: int):
        ri = ceil_int(2 * (b * prev_si - 2 * B), n)
        while True:
            low_bound = ceil_int(2 * B + ri * n, b)
            high_bound = ceil_int(3 * B + ri * n, a)
            for si in range(low_bound, high_bound):
                new_c = (pow(si, e, n) * c) % n
                if oracle(new_c):
                    return si
            ri += 1

    def bleichenbacher_merge_M(si: int, M: list):
        new_M = []
        for [a, b] in M:
            r_low = ceil_int(a * si - 3 * B + 1, n)
            r_high = floor_int(b * si - 2 * B, n) + 1
            for ri in range(r_low, r_high):
                interval_low = max(a, ceil_int(2 * B + ri * n, si))
                interval_high = min(b, floor_int(3 * B + ri * n - 1, si))
                if interval_high >= interval_low:
                    new_M.append([interval_low, interval_high])
        return new_M

    s = bleichenbacher_orifind_s(ceil_int(n, 3 * B))
    M = bleichenbacher_merge_M(s, [[2 * B, 3 * B - 1]])
    print(s, M)

    while True:
        if len(M) > 1:
            s = bleichenbacher_orifind_s(s + 1)
        else:
            if M[0][0] == M[0][1]:
                return M[0][0]
            s = bleichenbacher_optfind_s(s, M[0][0], M[0][1])
        M = bleichenbacher_merge_M(s, M)
        print(s, M)
```