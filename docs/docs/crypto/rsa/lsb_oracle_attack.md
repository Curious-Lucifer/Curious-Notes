# LSB Oracle Attack

if there's an oracle that give it $c$, it will give us the less bit of corresponding $m$. we can write the oracle like

$$
c \longrightarrow m \longrightarrow \lfloor m \rfloor_2
$$

let $m = x_0 + 2 \cdot y_1$, $x_0 \in \lbrace 0, 1\rbrace$, then we can get $x_0$ by

$$
c \longrightarrow m \longrightarrow \lfloor m \rfloor_2 = x_0
$$

let $y_1 = x_1 + 2 \cdot y_2$, $x \in \lbrace 0, 1\rbrace$, then we can get $x_1$ by

$$
(2^{-1})^e \cdot c \longrightarrow 2^{-1} \cdot m \pmod n \longrightarrow \lfloor 2^{-1} \cdot x_0 \rfloor_n + x_1 \pmod 2
$$

and then so on and so forth, we can find every bits of $m$ for ($n$’s bits length) time.


---
## Code

```python
def LSB_oracle_attack(n: int, e: int, c: int, oracle, m_bitlength: int = None):
    """
    - input : `n (int)`, `e (int)`, `c (int)`, `oracle (func)`, `m_bitlength (int, default = None)`
    - output : `m (int)`
    - oracle func : 
        - input : `c (int)`
        - output : `lbit (int)` , `{0, 1}` last bit of `m` (`c`'s plain)
    """

    m_bitlength = m_bitlength or n.bit_length()
    multiple_const = pow(2, -e, n)
    m_bitlist = []
    for i in trange(m_bitlength):
        new_c = (pow(multiple_const, i, n) * c) % n
        bit = (oracle(new_c) - (sum((pow(2, - i + j, n) * m_bitlist[j] % n) for j in range(i)) % n)) % 2
        m_bitlist.append(bit)

    return int(''.join(str(bit) for bit in reversed(m_bitlist)), base=2)
```
