# Euler’s Theorem

if $a \gt 1$, $n \gt 1$, $a,n \in \mathbb N$, and $\operatorname{gcd}(a,n) = 1$, then $a^{\varphi(n)} \equiv 1 \pmod n$, where $\varphi(n)$ is the number of integer that less than $n$ and coprime with $n$


---
## Proof

> the operation in this proof will be performed with modulo $n$

let $\lbrace\alpha_1,\alpha_2,...,\alpha_{\varphi(n)}\rbrace$ be a set of $\varphi(n)$ different digits that are coprime with $n$, we know $\operatorname{gcd}(a,n) = 1$, so for $i,j \in \lbrace1,2,...,\varphi(n)\rbrace$ and $i \neq j$, $\operatorname{gcd}(a\alpha_i,n) = 1$, and $a\alpha_i \not\equiv a\alpha_j$

$\Rightarrow \lbrace a\alpha_1,a\alpha_2,...,a\alpha_{\varphi(n)}\rbrace$ is another set of of $\varphi(n)$ different digits that are coprime with $n$

$$
\alpha_1 \cdot \alpha_2 \cdot ...  \cdot \alpha_{\varphi(n)} \equiv a\alpha_1 \cdot a\alpha_2 \cdot ... \cdot a\alpha_{\varphi(n)} \pmod n
$$

it's easy to see $a^{\varphi(n)} \equiv 1 \pmod n$


---
## Primitive Root

if $\operatorname{gcd}(a, n) = 1$, for the smallest $\delta$ satisfy $a ^ {\delta} \equiv 1 \pmod n$ that $\delta = \varphi(n)$, then we call $a$ is a primitive root modulo $n$
