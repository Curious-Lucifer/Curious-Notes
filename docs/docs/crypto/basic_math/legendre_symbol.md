# Legendre Symbol

$$
\left ( \frac{a}{p} \right ) = 
\begin{cases}
1 \qquad &\text{if } \exists x \text{ that } x^2 \equiv a \pmod p \text{ and } a \not\equiv 0 \pmod p \\
-1\qquad &\text{if } \forall x \text{ that } x^2 \not\equiv a \pmod p \text{ and } a \not\equiv 0 \pmod p \\
0\qquad &\text{if } a \equiv 0 \pmod p
\end{cases}
$$

we can write the Legendre Symbol like (if $p$ is prime)

$$
\left ( \frac{a}{p} \right ) = a^{ \frac{p-1}{2} } \pmod p
$$

---
## Proof
we know that $a^{p-1} \equiv 1 \pmod p$,

$$
(a^{ \frac{p-1}{2}} + 1) \cdot (a^{ \frac{p-1}{2}} - 1) \equiv 0 \pmod p
$$

so $a^{\frac{p-1}{2}}$ will be $1$ or $-1$

if $a$ is $p$’s quadratic residue, then $\exists x$ that $x^2 \equiv a \pmod p$, then

$$
a^{\frac{p-1}{2}} \equiv x^{p-1} \equiv 1 \pmod p
$$

if $a^{\frac{p-1}{2}} \equiv 1 \pmod p$, because $p$ is a prime number, so $p$’s primitive root exist. assume $d$ is $p$’s primitive root, then $\exists j$ that $1 \le j \le p-1$ let $a \equiv d^j \pmod p$, so

$$
a^{\frac{p-1}{2}} \equiv d^{j \cdot \frac{p-1}{2}} \equiv 1 \pmod p
$$

because $d$ is $p$’s primitive root, so $(p - 1) | j \cdot \frac{p-1}{2}$ $\Rightarrow$ $j$ is even $\Rightarrow$ $a$ is $p$’s quadratic residue


---
## Code

```python
def legendre_symbol(a: int, p: int):
    """
    - input : `a (int)`, `p (int)`
    - output : `ls (int)` , value of (a/p) (legendre symbol)
    """

    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == (p - 1) else ls
```


---
## Jacobi Symbol
for any integer $a$ and any positive odd integer $n = {p_1}^{\alpha_1}{p_2}^{\alpha_2}...{p_k}^{\alpha_k}$

$$
\left ( \frac{a}{n} \right ) = \left ( \frac{a}{p_1} \right )^{\alpha_1} \left ( \frac{a}{p_2} \right )^{\alpha_2} ... \left ( \frac{a}{p_k} \right )^{\alpha_k}
$$

*Properties :*

- If $( \frac{a}{n} ) = -1$ then $a$ is a quadratic nonresidue modulo $n$
- If $a$ is a quadratic residue modulo $n$ and $\operatorname{gcd}(a, n) = 1$, then $( \frac{a}{n} ) = 1$
- If $( \frac{a}{n} ) = 1$ then $a$ may or may not be a quadratic residue modulo $n$
