# Pollard's p-1 Algorithm
if $(p-1)$’s max prime factor $B$ is really small, $(p-1)|1 \times 2 \times ...\times B$ , so

$$
2^{1 \times 2 \times ... \times B} = 2^{k(p-1)} \equiv 1 \pmod p
$$

$\Rightarrow$ $\operatorname{gcd}(2^{1 \times 2 \times 3 \times ... \times B} - 1,n) \gt 1$


---
## Code

```python
def pollard_algorithm(n: int):
    """
    - input : `n (int)` , n has a factor p that (p - 1)'s large prime factor is really small
    - output : `(p, q) (int, int)` , n's factors
    """

    a = 2
    b = 2
    while True:
        a = int(pow(a, b, n))
        p = int(gcd(a - 1, n))
        if 1 < p < n:
            return p, n // p
        b += 1
```
