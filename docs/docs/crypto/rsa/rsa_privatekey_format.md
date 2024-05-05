# RSA Private Key Format

## Length Encoding
- 0 ~ 0x7f : 00 ~ 7f
- 0x80 ~ 0xff : 81 80 ~ 81 ff
- 0x0100 ~ 0xffff : 82 01 00 ~ 82 ff ff
- 0x010000 ~ 0xffffff : 83 01 00 00 ~ 83 ff ff ff
- \.\.\.


---
## Traslation
```
-----BEGIN RSA PRIVATE KEY-----
MIIBOQIBAAJBAIOLepgdqXrM07O4dV/nJ5gSA12jcjBeBXK5mZO7Gc778HuvhJi+
RvqhSi82EuN9sHPx1iQqaCuXuS1vpuqvYiUCAwEAAQJATRDbCuFd2EbFxGXNxhjL
loj/Fc3a6UE8GeFoeydDUIJjWifbCAQsptSPIT5vhcudZgWEMDSXrIn79nXvyPy5
BQIhAPU+XwrLGy0Hd4Roug+9IRMrlu0gtSvTJRWQ/b7m0fbfAiEAiVB7bUMynZf4
SwVJ8NAF4AikBmYxOJPUxnPjEp8D23sCIA3ZcNqWL7myQ0CZ/W/oGVcQzhwkDbck
3GJEZuAB/vd3AiASmnvOZs9BuKgkCdhlrtlM6/7E+y1p++VU6bh2+mI8ZwIgf4Qh
u+zYCJfIjtJJpH1lHZW+A60iThKtezaCk7FiAC4= 
-----END RSA PRIVATE KEY-----
```

Base64 decode : (display in hex format)
```
30820139020100024100838b7a981da97accd3b3b8755fe7279812035da37230
5e0572b99993bb19cefbf07baf8498be46faa14a2f3612e37db073f1d6242a68
2b97b92d6fa6eaaf6225020301000102404d10db0ae15dd846c5c465cdc618cb
9688ff15cddae9413c19e1687b27435082635a27db08042ca6d48f213e6f85cb
9d660584303497ac89fbf675efc8fcb905022100f53e5f0acb1b2d07778468ba
0fbd21132b96ed20b52bd3251590fdbee6d1f6df02210089507b6d43329d97f8
4b0549f0d005e008a40666313893d4c673e3129f03db7b02200dd970da962fb9
b2434099fd6fe8195710ce1c240db724dc624466e001fef7770220129a7bce66
cf41b8a82409d865aed94cebfec4fb2d69fbe554e9b876fa623c6702207f8421
bbecd80897c88ed249a47d651d95be03ad224e12ad7b368293b162002e
```

- `30` : ASN.1 tag for sequence
  - `82 01 39` : length of following sequence (in byte), `82 01 39` represent 0x139
  - `02` : ASN.1 tag for int
    - `01` : length of this int (in byte)
    - `00` : Version
  - `02` : ANS.1 tag for int
    - `41` : length of this int (in byte)
    - `...` : $n$
  - `02` : ANS.1 tag for int
    - `03` : length of this int (in byte)
    - `...` : $e$
  - `02` : ANS.1 tag for int
    - `40` : length of this int (in byte)
    - `...` : $d$
  - `02` : ANS.1 tag for int
    - `21` : length of this int (in byte)
    - `...` : $p$
  - `02` : ANS.1 tag for int
    - `21` : length of this int (in byte)
    - `...` : $q$
  - `02` : ANS.1 tag for int
    - `20` : length of this int (in byte)
    - `...` : $d \pmod {p - 1}$
  - `02` : ANS.1 tag for int
    - `20` : length of this int (in byte)
    - `...` : $d \pmod {q - 1}$
  - `02` : ANS.1 tag for int
    - `20` : length of this int (in byte)
    - `...` : $q ^ {-1} \pmod {p - 1}$

