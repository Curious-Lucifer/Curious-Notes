# Wiener Attack

## Continued Fraction
for example, $\frac{13}{17}$’s continued fraction is $[c_0,c_1,c_2,c_3]$, and  

$c_0 = \lfloor \frac{13}{17} \rfloor = 0$  
$c_1 = 0 + \frac{1}{\lfloor \frac{17}{13} \rfloor} = 0 + \frac{1}{1} = 1$  
$c_2 = 0 + \frac{1}{1 + \frac{1}{\lfloor \frac{13}{4} \rfloor}} = 0 + \frac{1}{1 + \frac{1}{3}} = \frac{3}{4}$  
$c_3 = 0 + \frac{1}{1 + \frac{1}{3 + \frac{1}{\lfloor 4 \rfloor}}} = 0 + \frac{1}{1 + \frac{1}{3 + \frac{1}{4}}} = \frac{13}{17}$  


---
## Legendre’s Theorem in Diophantine Approximations

for $\alpha \in \mathbb R$, $\frac{a}{b} \in \mathbb Q$, and satisfy $| \alpha - \frac{a}{b}| \lt \frac{1}{2b^2}$, then $\frac{a}{b}$ will be in $\alpha$’s continued fraction


---
## Wiener Attack

if $d \lt \frac{1}{3}n^{\frac{1}{4}}$, $|p - q| \lt \operatorname{min}(p,q)$, and $ed = k\varphi(n) + 1$, we can proof that $\frac{k}{d}$ will be in $\frac{e}{n}$’s continued fraction. because $\operatorname{gcd}(k,d) = 1$, so we can try all $\frac{e}{n}$’s continued fraction and because

$$
\frac{ed - 1}{k} = \varphi(n) = (p-1)(q-1) = n - p - \frac{n}{p} + 1
$$

so

$$
p^2 + p(\frac{ed-1}{k} -  n - 1) + n = 0
$$

we can test if $p \in \mathbb N$ and if $p$ is $n$’s factor to check if $k$ and $d$ is correct


---
## Proof

we know that $|p-q| \lt \operatorname{min}(p,q)$, we can set $p \gt q$, then $2q \gt p \gt q$, set $p = q + a$ and $a \lt q$, so

$$
n - \varphi(n) = n - (p-1)(q-1) = p + q - 1 = 2q + a - 1 < 3q
$$

and

$$
3\sqrt{n} = 3\sqrt{q^2 + qa} \gt 3\sqrt{q^2} = 3q
$$

so $3\sqrt{n} \gt (n - \varphi(n))$

$$
\left | \frac{e}{n} - \frac{k}{d} \right | = \left | \frac{ed - nk}{nd} \right | = \left | \frac{1 + k\varphi(n) - kn}{nd}\right | = \frac{k(n - \varphi(n)) - 1}{nd}
$$

then

$$
\left | \frac{e}{n} - \frac{k}{d} \right | = \frac{k(n - \varphi(n)) - 1}{nd} \lt \frac{3k\sqrt{n} - 1}{nd} \lt \frac{3k\sqrt{n}}{nd}
$$

we also know $d \lt \frac{1}{3}n^{\frac{1}{4}}$ 

$$
k \varphi(n) = ed - 1 \lt ed \lt \varphi(n) d
$$

$$
k \lt d \lt \frac{1}{3}n^{\frac{1}{4}}
$$

so

$$
\left | \frac{e}{n} - \frac{k}{d} \right | \lt \frac{3k\sqrt{n}}{nd} \lt \frac{1}{n^{\frac{1}{4}}d}
$$

and $d \lt \frac{1}{3}n^{\frac{1}{4}} \quad\Rightarrow\quad 2d \lt 3d \lt n^{\frac{1}{4}} \quad\Rightarrow\quad \frac{1}{2d} \gt \frac{1}{n^{\frac{1}{4}}}$, so

$$
\left |\frac{e}{n} - \frac{k}{d} \right | \lt \frac{1}{n^{\frac{1}{4}}d} \lt \frac{1}{2d^2}
$$

because $ed - k\varphi(n) = 1$, so $\operatorname{gcd}(k,d) = 1$, and because Legendre’s Theorem in Diophantine Approximations

$$
\left |\frac{e}{n} - \frac{k}{d} \right | \lt \frac{1}{2d^2}
$$

so $\frac{k}{d}$ will be in $\frac{e}{n}$’s continued fraction


---
## Code

```python
def wiener_attack(n: int, e: int):
    """
    - input : `n (int)`, `e (int)`
    - output : `(p, q, d) (int, int, int)`
    """

    continued_fraction_list = (Integer(e) / Integer(n)).continued_fraction()
    for i in range(2, len(continued_fraction_list)):
        cf = continued_fraction_list.convergent(i)
        k = cf.numerator()
        d = cf.denominator()
        if ((e * d - 1) % k) != 0:
            continue
        b = (e * d - 1) // k - n - 1
        if (b ** 2 - 4 * n) <= 0:
            continue
        D = iroot(int(b ** 2 - 4 * n), 2)
        if not D[1]:
            continue
        p, q = ((-int(b) + int(D[0])) // 2), ((-int(b) - int(D[0])) // 2)
        if p * q == n:
            return p, q, int(d)
```
