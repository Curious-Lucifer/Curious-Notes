# Coppersmith Method

if given a monic polynomial $f(x) = x^\delta + ...$, a integer of unknown factorization $N$, a upper bound $X$, a real number $\beta$, our goal is to find out all $|x_0| \le X$ that satisfy

$$
f(x_0) \equiv 0 \pmod b \quad\text{ , where }\space b \ge N^\beta \space\text{ and }\space b|N
$$

let

$$
X_0 = \lbrace x_0 \space|\space f(x_0) \equiv 0 \pmod b ,\space |x_0| \le X \rbrace
$$

if we can find a polynomial $g$ that for all $x_0 \in X_0$, $g(x_0) = 0$, then we can just solve $g(x) = 0$ to know the root of $f$

now pick two integers $m$ and $t$, let

$$
f_i(x) = \begin{cases}
x^k \cdot N^{m-j} \cdot [f(x)]^j & \text{for } 0 \le j \lt m,\space 0 \le k \lt \delta & \text{ , and } i = j\delta + k \\
x^l \cdot [f(x)]^m & \text{for } 0 \le l \lt t & \text{ , and } i = m\delta + l
\end{cases}
$$

for all $i \in [0,m\delta + t)$, $f_i(x_0) \equiv 0 \pmod {b^m}$ , let

$$
g(x) = \sum_{i=0}^{m\delta + t - 1} a_if_i(x) \space\text{ , for all }\space a_i \in \mathbb Z
$$

we know that $g(x_0) \equiv 0 \pmod {b^m}$, if $|g(x_0)| \lt b^m$, then $g(x_0) = 0$

if ($n = m\delta + t$)

$$
g(x) = \sum_{i = 0}^{n - 1}g_i \cdot x^i
$$

then let

$$
\textbf{g(x)} = (g_0,\space g_1x,\space  g_2x^2 ,\space  ... ,\space g_{n-2}x^{n-2}, \space g_{n-1}x^{n-1})
$$

if 

$$
\left | \textbf{g(X)} \right | = \sqrt {\sum_{i=0}^{n-1} (g_i \cdot X^i)^2} \lt \frac{b^m}{\sqrt n}
$$

then

$$
\begin{aligned}
\left | g(x_0) \right | & = \left | \sum_{i=0}^{n-1} g_i \cdot {x_0}^i \right | \le \sum_{i=0}^{n-1} \left | g_i \cdot {x_0}^i \right | \\
& \le \sum_{i=0}^{n-1} \left | g_i \cdot X^i \right | = \sqrt {(\sum_{i=0}^{n-1} \left | g_i \cdot X^i \right | )^2} \\
& \le \sqrt {n \cdot \sum_{i=0}^{n-1} \left | g_i \cdot X^i \right | ^2} \quad \text{ , Cauchy–Schwarz inequality} \\
& = \sqrt n \cdot | \textbf{g(X)} | \lt b^m
\end{aligned}
$$

so now, if we have a $g(x) = \sum_{i=0}^{m\delta + t - 1} a_if_i(x)$, and choose $a_i$ let $| \textbf{g(X)} | \lt \frac{b^m}{\sqrt n}$. then we can solve $g(x) = 0$ to get it's roots and some of them will be ($f(x) \equiv 0 \pmod n$)’s roots

let $(\mathbf{f_0(X)},\space\mathbf{f_1(X)},\space ..., \mathbf{f_{n-1}(X)})$ be the basis of lattice $L$, we can use LLL-algorithm to find some $\textbf{g(X)}$ that

$$
| \textbf{g(X)} | \le 2^{\frac{n-1}{4}} \cdot \operatorname{det}(L)^{\frac{1}{n}}
$$

we know that $\operatorname{det}(L) = N^{\frac{1}{2}\delta m(m+1)} \cdot X^{\frac{1}{2}n(n-1)}$, if we choose $0 \lt \epsilon \le \frac{\beta}{7}$ , and

$$
m = \lceil \frac{\beta^2}{\delta \epsilon} \rceil ,\space t = \lfloor \delta m(\frac{1}{\beta} - 1) \rfloor ,\space X = \lceil \frac{1}{2}N^{\frac{\beta^2}{\delta} - \epsilon} \rceil
$$

after some calculation, then $2^{\frac{n-1}{4}} \cdot \operatorname{det}(L)^{\frac{1}{n}} \lt \frac{N^{\beta m}}{\sqrt n}$

> Implementation : [Sage Implement](https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_modn_dense_ntl.html#sage.rings.polynomial.polynomial_modn_dense_ntl.small_roots)

