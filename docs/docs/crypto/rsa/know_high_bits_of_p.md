# Know High Bits Of p

if $p = \bar{p} + x_0$ and we know $\bar{p}$, $|x_0| \lt N^{\frac{1}{4}}$, then $x_0$ is $f(x) \equiv \bar{p} + x \pmod p$’s small root (assume that $p \lt q$)


---
## Code

```python
def known_high_bits_of_p(n: int, p0: int, epsilon=None):
    """
    - input : `n (int)`, `p0 (int)`, `epsilon (default=None)` , `0 < epsilon <= 0.5/7`
    - output : `(p, q) (int, int)`
    """
    P = PolynomialRing(Zmod(n), implementation='NTL', names=('x',))
    x = P._first_ngens(1)[0]
    
    f = p0 + x
    small_roots = f.small_roots(beta=0.5, epsilon=epsilon)
    if len(small_roots) > 0:
        p = p0 + int(small_roots[0])
        q = n // p
        assert p * q == n
        return p, q
    else:
        return -1
```
