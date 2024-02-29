# Fermat Factorization

assume $p \gt q$ (well $p,q$ is changable), if $p-q$ is really small, let

$$
\begin{cases}
p = a + b\\
q = a - b
\end{cases}
\space\Rightarrow\space
n = pq = a^2 - b^2
\space\Rightarrow\space
n + b^2 = a^2
$$

because $p-q$ is really small, so $b$ is really small too $\Rightarrow$ try $a$ let $\sqrt{a^2 - n} \in \mathbb N$

---
## Code

```python
def fermat_factor(n: int):
    """
    - input : `n (int)`
    - output : `(p, q) (int, int)`
    """

    a = int(isqrt(n)) + 1
    b = iroot(a ** 2 - n, 2)
    while not b[1]:
        a += 1
        b = iroot(a ** 2 - n, 2)
        print(a)
    b = int(b[0])
    return (a - b), (a + b)
```
