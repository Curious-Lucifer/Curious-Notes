# William's p+1 Algorithm

## Lucas Sequence
Given two integer parameters $P$ and $Q$, then Lucas Sequences $U_n(P, Q)$ and $V_n(P, Q)$ is defined by

$$
U_0(P, Q) = 0,\space U_1(P, Q) = 1,\space U_n(P, Q) = P \cdot U_{n-1} - Q \cdot U_{n-2}
$$

$$
V_0(P, Q) = 2,\space V_1(P, Q) = P,\space V_n(P, Q) = P \cdot V_{n-1} - Q \cdot V_{n-2}
$$

### Properties

1. $V_{i+j} = V_iV_j - Q^jV_{i-j}$
2. $V_{2i} = {V_i}^2 - 2Q^i$
3. $V_{ij}(P, Q) = V_i(V_j(P, Q), Q^j)$
4. for $P = A > 2$ and $Q = 1$, and every operations are performed modulo $n$

$$
V_0 = 2,\space V_1 = A,\space V_j = AV_{j-1} - V_{j-2}
$$

then any odd prime $p$ divides $\operatorname{gcd}(n,V_M−2)$ whenever $M$ is a multiple of $p - \left ( \frac{D}{p} \right )$, where $D = A^2 - 4$ and $\left ( \frac{D}{p} \right )$ is Legendre Symbol


---
## William's p+1 Algorithm
if $(p + 1)$’s max prime factor $B$ is really small, then we can randomly choose $A$. if $(\frac{A^2 - 4}{p}) = -1$, let $M = 1 \times 2 \times … \times B$, then $\operatorname{gcd}(n, V_M-2) > 1$


---
## Code

```python
def william_algorithm(n: int, B: int=None):
    """
    - input : `n (int)`, `B (int, default None)` , B is the upper bound of (p + 1)'s max prime factor
    - output : `(p, q) (int, int)` , `p * q = n`
    """

    def calc_lucas(a: int, k: int):
        """
        - input : `a (int)`, `k (int)`
        - output : `v1 (int)` , return V_k(a, 1)
        """

        # Init : v1, v2 = V[1], V[2]
        # General : v1, v2 = V[i], V[i + 1]
        v1, v2 = a % n, (a ** 2 - 2) % n
        for bit in bin(k)[3:]:
            if bit == '1':
                # v1, v2 = V[2i + 1], V[2i + 2]
                v1, v2 = (v1 * v2 - a) % n, (v2 ** 2 - 2) % n
            else:
                # v1, v2 = V[2i], V[2i + 1]
                v1, v2 = (v1 ** 2 - 2) % n, (v1 * v2 - a) % n
        return v1

    prime_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    
    B = B or int(isqrt(n))
    for A in prime_list:
        v = A
        for i in trange(1, B + 1, desc=f'A = {A}'):
            v = calc_lucas(v, i)
            p = gcd(v - 2, n)
            if n > p > 1:
                return p, n // p
```

