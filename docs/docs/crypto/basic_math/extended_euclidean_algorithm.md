# Extended Euclidean Algorithm

the algorithm that calculate a solve $(x, y)$ of $ax + by = \operatorname{gcd}(a, b)$

Ex. $a = 240, b = 46$ :

```
5 | 240 |  46 | 4         5 |        a |        b | 4
  | 230 |  40 |             |       5b | 4a - 20b |
  |-----|-----|             |----------|----------|
1 |  10 |   6 | 1         1 |   a - 5b | 21b - 4a | 1
  |   6 |   4 |             | 21b - 4a | 5a - 26b |
  |-----|-----|             |----------|----------|
2 |   4 |   2 |           2 | 5a - 26b | 47b - 9a |
  |   4 |     |             |          |          |
  |-----|     |
  |   0 |     |
```


---
## Code

```python
def egcd(a: int, b: int):
    """
    - input : a(int), b(int) , (a != 0 and b != 0)
    - output : (x, y) (int, int) that satisfy ax + by = gcd(a, b)
    """

    assert (a != 0) and (b != 0)

    a, coe_a =  (a, (1, 0)) if (a > 0) else (-a, (-1, 0))
    b, coe_b =  (b, (0, 1)) if (b > 0) else (-b, (0, -1))
    q, r = a // b, a % b
    while r:
        a, b, coe_a, coe_b = b, r, coe_b, (coe_a[0] - q * coe_b[0], coe_a[1] - q * coe_b[1])
        q, r = a // b, a % b
    
    return coe_b
```


---
## Modular Multiplicative Inverse

if $\operatorname{gcd}(a, n) = 1$, then exist unique modular multiplicative inverse $b$ let $ab \equiv 1 \pmod n$. $b$ can written as $a ^ {-1} \pmod n$

> use Extended Euclidean Algorithm calculates $ax + ny = 1$’s solve, 
($x \pmod n$) will be $a$’s modular multiplicative inverse under $n$
