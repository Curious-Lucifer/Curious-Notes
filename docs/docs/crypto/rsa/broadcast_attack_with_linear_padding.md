# Broadcast Attack With Linear Padding

if we know $n_1$, $n_2$, $n_3$, $c_1$, $c_2$, $c_3$ and linear function $f_1$, $f_2$, $f_3$ that

$$
\begin{cases}
c_1 \equiv f_1(m) ^ e \pmod {n_1}  \\
c_2 \equiv f_2(m) ^ e \pmod {n_2}  \\ 
... \\
c_e \equiv f_3(m) ^ e \pmod {n_e}  \\
\end{cases}
$$

then we can find a set of $t_i$ that $t_i \equiv 1 \pmod {n_i}$ and $t_i \equiv 0 \pmod {n_j}$ for $i \neq j$ 

let 

$$
g(x) = \sum_{i=1}^e (t_i \cdot (f_i(x) ^ e - c_i))
$$

then $m$ will probably be the small root of $g(x) \pmod {\prod n_i}$


---
## Code

```python
def broadcast_with_linear(a_list: list[int], b_list: list[int], c_list: list[int], n_list: list[int], e: int, epsilon=None):
    """
    - input : `a_list (list[int])`, `b_list (list[int])`, `c_list (list[int])`, `n_list (list[int])`, `e (int)`, `epsilon (default=None)` , `0 < epsilon <= 1/7`
        - `(a1 * m + b1) ^ e ≡ c1 (mod n1)
        - `(a2 * m + b2) ^ e ≡ c2 (mod n2)
        - ...
    - output : `m % N (int)` , `N = n1 * n2 * ...`
    """

    N = reduce(lambda x, y: x * y, n_list)
    t_list = [(N // n) * pow(N // n, -1, n) for n in n_list]

    P = PolynomialRing(Zmod(N), implementation='NTL', names=('x',))
    x = P._first_ngens(1)[0]

    g = 0
    for i in range(e):
        f = a_list[i] * x + b_list[i]
        g += t_list[i] * (f ** e - c_list[i])

    g *= pow(int(g.leading_coefficient()), -1, N)
    small_roots = g.small_roots(epsilon=epsilon)
    if len(small_roots) > 0:
        return int(small_roots[0])
    else:
        return -1
```
