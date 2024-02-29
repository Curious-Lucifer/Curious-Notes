# Coppersmith Short-Pad Attack

## Resultant

if $a$, $b$ is $f$, $g$’s leading coefficient, then

$$
\operatorname{res}(f,g) = a^{\operatorname{deg}(f)} \cdot b^{\operatorname{deg}(g)} \cdot \prod_{\forall (x,y) , f(x) = g(y) = 0} (x - y)
$$


---
## Coppersmith Short-Pad Attack

if $m_1 = 2^kM + r_1$ and $m_2 = 2^kM + r_2$ ($r_1$ and $r_2$ is padding, $M$ is plaintext), and we know $c_1, c_2$ is $m_1, m_2$’s cipher encrypted by $(n,c)$, consider

$$
\begin{aligned}
f_1(x,y) & \equiv x^e - c_1 \pmod n \\
f_2(x,y) & \equiv (x + y)^e - c_2 \pmod n
\end{aligned}
$$

if $\bar y = r_2 - r_1$, then $f_1(x,\bar y)$ and $f_2(x,\bar y)$ has common factor $x - m_1$, so $\operatorname{res}(f_1(x,\bar y),\space f_2(x,\bar y)) \equiv 0 \pmod n$. let $h(y) = \operatorname{res}_x(f_1,f_2)$, $\bar y$ will be a small root of $h(y)$

then bring $\bar y$ back to $f_1$ and $f_2$ , this well simplify problem to Franklin-Reiter related message attack


---
## Code

```python
def coppersmith_short_pad_attack(n: int, e: int, c1: int, c2: int, epsilon=None):
    """
    - input : `n (int)`, `e (int)`, `c1 (int)`, `c2 (int)`, `epsilon (default=None)` , `0 < epsilon <= 1/7`
    - output : `m1 (int)` , `c1`'s plain
    """

    P2 = PolynomialRing(IntegerRing(), names=('x', 'y'))
    (x, y) = P2._first_ngens(2)

    f1 = x ** e - c1
    f2 = (x + y) ** e - c2
    h = f1.resultant(f2, x).univariate_polynomial().change_ring(Zmod(n))
    small_roots = h.small_roots(epsilon=epsilon)
    if len(small_roots) > 0:
        diff = small_roots[0]
    else:
        return -1

    P = PolynomialRing(Zmod(n), implementation='NTL', names=('x',))
    x = P._first_ngens(1)[0]

    f = x + diff
    return franklin_reiter(e, c1, c2, f, x)
```