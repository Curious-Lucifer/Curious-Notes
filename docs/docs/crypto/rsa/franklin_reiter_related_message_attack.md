# Franklin-Reiter Related Message Attack

if we know $m_1, m_2$’s cipher $c_1, c_2$ is encrypted by public key $(n,e)$, and $m_1, m_2$ satisfy $m_2 = f(m_1)$ such $f$ is a polynomial on modulo $n$, consider

$$
\begin{aligned}
g_1(x) & \equiv x^e - c1 \pmod n \\
g_2(x) & \equiv {f(x)}^e - c2 \pmod n
\end{aligned}
$$

then $m_1$ is both $g_1(x)$ and $g_2(x)$’s root, so $\operatorname{gcd}(g_1,g_2) = x - m_1$


---
## Code

```python
def polynomialgcd(f1, f2):
    if f2 == 0:
        return f1.monic()

    if f2.degree() > f1.degree():
        f1, f2 = f2, f1

    while f2 != 0:
        f1, f2 = f2, f1 % f2
    
    return f1.monic()


def franklin_reiter(e: int, c1: int, c2: int, f, x):
    """
    - input : `e (int)`, `c1 (int)`, `c2 (int)`, `f (polynomial of x mod n)`, `x (symbol of polynomial mod n)`
    - output : `m1 (int)` , `f(m1) = m2`
    """

    f1 = x ** e - c1
    f2 = f ** e - c2
    return int(-polynomialgcd(f1, f2)[0])
```
