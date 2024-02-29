# Chinese Remainder Theorem

$$
\text{if } \space
\begin{cases}
x \equiv a_1 \pmod {m_1}\\
x \equiv a_2 \pmod {m_2}\\
x \equiv a_3 \pmod {m_3}\\
...\\
x \equiv a_n \pmod {m_n}
\end{cases}
\quad\text{ let }\quad
\begin{cases}
M = m1 \cdot m2 \cdot ... \cdot m_n\\
M_i = \frac{M}{m_i}\\
t_i \equiv M_i^{-1} \pmod {m_i}
\end{cases}
$$

$$
\Rightarrow \quad x \equiv a_1t_1M_1 + a_2t_2M_2 + ... + a_nt_nM_n \pmod M
$$


---
## Code

```python
def crt(ai_list: list[int], mi_list: list[int]):
    """
    - input : `ai_list (list[int])`, `mi_list (list[int])` , and assume `ai_list = [a1, a2, ...]`, `mi_list = [m1 ,m2, ...]`
        - `x ≡ a1 (mod m1)`
        - `x ≡ a2 (mod m2)`
        - ...
    - output : `x % M (int)` , `M = m1 * m2 * ...`
    """
    assert len(ai_list) == len(mi_list)

    M = reduce(lambda x, y: x * y, mi_list)
    Mi_list = [M // mi for mi in mi_list]
    ti_list = [pow(Mi, -1, mi) for Mi, mi in zip(Mi_list, mi_list)]
    return sum(ai * ti * Mi for ai, ti, Mi in zip(ai_list, ti_list, Mi_list)) % M
```
