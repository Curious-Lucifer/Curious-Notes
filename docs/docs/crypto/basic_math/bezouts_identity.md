# Bézout's Identity

if $a, b, m \in \mathbb Z$, and $a \neq 0 \wedge b \neq 0$, then

$$
\exists (x, y) \in \mathbb Z^2 \text{ that } ax + by = m \Leftrightarrow \operatorname{gcd}(a, b)|m
$$


---
## Proof
let 

$$
A = \lbrace(ax + by)|(x, y) \in \mathbb Z^2\rbrace
$$

because $A \cup \mathbb N \neq \emptyset$, so $\exists d_0 = ax_0 + by_0$ is $A$’s smallest positive element.

for any $p = ax_1 + by_1 \in A$, let $p$ perform integer division on $d_0$

$$
p = qd_0 + r \text{ and } 0 \le r \lt d_0
$$

$$
r = p - qd_0 = a(x_1 - qx_0) + b(y_1 - qy_0) \in A
$$

because $0 \le r \lt d_0$ and $d_0$ is the smallest positive element in $A$, so $r = 0$ $\Rightarrow$ $p = qd_0$ $\Rightarrow$ $d_0 | p$, this represent any element $p \in A$ is $d_0$’s multiple

we know that $a \in A \text{ and } b \in A$, so $d_0$ is $(a,b)$’s common factor

for any $(a,b)$’s common factor $d$, let $a = kd$ and $b = ld$

$$
d_0 = ax_0 + by_0 = d(kx_0 + ly_0)
$$

so $d|d_0$, $d_0 = \operatorname{gcd}(a,b)$

> the solve set of $ax + by = \operatorname{gcd}(a,b)$ is $\lbrace(x_0 + k \cdot \frac{b}{d_0},y_0 - k \cdot \frac{a}{d_0})|k \in \mathbb Z\rbrace$

