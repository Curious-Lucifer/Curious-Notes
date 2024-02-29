# Factor n with d
for

$$
\begin{cases}
x^2 \equiv 1 \pmod p\\
x^2 \equiv 1 \pmod q
\end{cases}
\space\Rightarrow\space
x^2 \equiv 1 \pmod n
$$

there will be at least 4 solves

$$
\begin{cases}
x \equiv 1 \pmod p\\
x \equiv 1 \pmod q
\end{cases}
\Rightarrow x \equiv 1 \pmod n
\quad,\quad
\begin{cases}
x \equiv -1 \pmod p\\
x \equiv -1 \pmod q
\end{cases}
\Rightarrow x \equiv -1 \pmod n
$$

$$
\begin{cases}
x \equiv 1 &\pmod p\\
x \equiv -1 &\pmod q
\end{cases}
\quad,\quad
\begin{cases}
x \equiv -1 &\pmod p\\
x \equiv 1 &\pmod q
\end{cases}
$$

if we can find a solve of $x^2 \equiv 1 \pmod n$ that $x \not\equiv \pm 1 \pmod n$, then

$$
(x + 1)(x - 1) \equiv 0 \pmod n
\space\Rightarrow\space
\begin{cases}
1 \lt \operatorname{gcd}(n, x + 1) \lt n\\
1 \lt \operatorname{gcd}(n, x - 1) \lt n
\end{cases}
$$

for any $g$, we know that $g^{ed - 1} \equiv 1 \pmod n$ and $ed - 1 = k\varphi(n) = 2^tr$, so $g^{2^{t - 1}r} \pmod n$ is a root of $x^2 \equiv 1 \pmod n$. if $g^{2^{t - 1}r} \not\equiv \pm 1 \pmod n$, then we can calculate $\operatorname{gcd}(g^{2^{t - 1}r} - 1, n)$ to factor $n$

else if $g^{2^{t - 1}r} \equiv 1 \pmod n$, then calculate if $g^{{2^{t-2}}r} \not\equiv \pm 1 \pmod n$, so on and so forth.

if none of them $\not\equiv \pm 1 \pmod n$, then choose another $g$.


---
## Code

```python
def factor_n_with_d(n: int, e: int, d: int):
    """
    - input : `n (int)`, `e (int)`, `d (int)`
    - output : `(p, q) (int, int)` , `p * q = n` and p, q is prime
    """

    for g in range(2, n):
        init_pow = e * d - 1
        while ((init_pow % 2) == 0):
            init_pow //= 2
            root = pow(g, init_pow, n)
            if 1 < gcd(root - 1, n) < n:
                p = gcd(root - 1, n)
                q = n // p
                return p, q
            if root == (n - 1):
                break
```
