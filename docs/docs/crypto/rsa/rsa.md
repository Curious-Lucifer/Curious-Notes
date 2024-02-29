# RSA

generate two prime $p, q$ and an integer $e$ that $\operatorname{gcd}(e, \varphi(n)) = 1$, then calculate $n = pq$ and $\varphi(n) = (p - 1)(q - 1)$, $d \equiv e^{-1} \pmod {\varphi(n)}$

$$
\text{public key : } (e,n) \qquad \text{private key : } d
$$

Encryption : $c \equiv m^e \pmod n$

Decryption : $m \equiv c^d \pmod n$


---
## Proof

$d \equiv e^{-1} \pmod {\varphi(n)}$, so $ed = 1 + k\varphi(n)$

if $\operatorname{gcd}(m, p) = 1$

$$
m^{ed} \equiv m^{1 + k(p-1)(q-1)} \equiv m \cdot (m^{p-1})^{k(q-1)} \equiv m \pmod p
$$

if $\operatorname{gcd}(m, p) = p$

$$
m^{ed} \equiv 0 \equiv m \pmod p
$$

same as $q$, so 

$$
\begin{cases}
m^{ed} \equiv m \pmod p \\
m^{ed} \equiv m \pmod q
\end{cases}
$$

we know exist $(x, y)$ that satisfy $px + qy = 1$, and $x \equiv p^{-1} \pmod q$ and $y \equiv q^{-1} \pmod p$

use CRT

$$
\begin{aligned}
m^{ed} & \equiv m \cdot q \cdot (q^{-1} \pmod p) + m \cdot p \cdot (p^{-1} \pmod q) &\pmod n\\
& \equiv m \cdot (q \cdot (y + kp) + p \cdot (x + lq)) & \pmod n \\
&\equiv m &\pmod n
\end{aligned}
$$

