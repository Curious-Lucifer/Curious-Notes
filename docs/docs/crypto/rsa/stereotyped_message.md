# Stereotyped Message

if we know $m = \bar{m} + x_0$ and $x_0 \le N^{\frac{1}{e}}$, the cipher $c \equiv m^e \equiv (\bar{m} + x_0)^e \pmod N$, then $x_0$ is the small root of $f(x) \equiv (\bar{m} + x)^e - c \pmod N$


---
## Code

```python
def stereotyped_message(n: int, e: int, c: int, m0: int, epsilon=None):
    """
    - input : `n (int)`, `e (int)`, `c (int)`, `m0 (int)`, `epsilon (default=None)` , `0 < epsilon <= 1/7`
    - output : `m (int)` , `c`'s plain. if there's no solve, return `-1`
    """
    P = PolynomialRing(Zmod(n), implementation='NTL', names=('x',))
    x = P._first_ngens(1)[0]

    f = (m0 + x) ** e - c
    small_roots = f.small_roots(epsilon=epsilon)
    if len(small_roots) > 0:
        return int(small_roots[0]) + m0
    else:
        return -1
```

