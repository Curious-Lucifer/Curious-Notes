# Python Random Module

## seed

```c
static PyObject *_random_Random_seed_impl(RandomObject *self, PyObject *n) {
    if (random_seed(self, n) < 0) {
        return NULL;
    }
    // #define Py_RETURN_NONE return Py_None
    Py_RETURN_NONE;
}
```

```c
static int random_seed(RandomObject *self, PyObject *arg) {
    int result = -1;
    PyObject *n = NULL;
    uint32_t *key = NULL;
    size_t bits, keyused;
    int res;

    if (arg == NULL || arg == Py_None) {
        // ...
    }

    if (PyLong_CheckExact(arg)) {
        n = PyNumber_Absolute(arg);
    } else if (PyLong_Check(arg)) {
        // ...
    } else {
        // ...
    }
    if (n == NULL)
        goto Done;

    bits = _PyLong_NumBits(n);
    if (bits == (size_t)-1 && PyErr_Occurred())
        goto Done;

    // 找出 `n` 總共需要多少 32 bits 的 chunk
    keyused = bits == 0 ? 1 : (bits - 1) / 32 + 1;

    /* Convert seed to byte sequence. */
    key = (uint32_t *)PyMem_Malloc((size_t)4 * keyused);
    if (key == NULL) {
        PyErr_NoMemory();
        goto Done
    }
    // 把 `n` 的值按照 little endian 排進 `key`，倒數第二個 0 代表 unsigned，倒數第一個 1 代表有錯誤會有 exeption
    res = _PyLong_AsByteArray((PyLongObject *)n, (unsigned char *)key, keyused * 4, PY_LITTLE_ENDIAN, 0, 1);
    if (res == -1) {
        goto Done;
    }

#if PY_BIG_ENDIAN
    // 把 `key` 反過來
    {
        size_t i, j;
        for (i = 0, j = keyused - 1; i < j; i++, j--) {
            uint32_t tmp = key[i];
            key[i] = key[j];
            key[j] = tmp;
        }
    }
#endif
    init_by_array(self, key, keyused);

    result = 0;

Done:
    Py_XDECREF(n);
    PyMem_Free(key);
    return result;
}
```

```c
static void init_by_array(RandomObject *self, uint32_t init_key[], size_t key_length) {
    size_t i, j, k;
    uint32_t *mt;

    mt = self->state;
    init_genrand(self, 19650218U);
    i=1; j=0;
    k = (N > key_length ? N : key_length);
    for (; k; k--) {
        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1664525U))
                 + init_key[j] + (uint32_t)j;
        i++; j++;
        if (i >= N) { mt[0] = mt[N-1]; i=1; }
        if (j >= key_length) j=0;
    }
    for (k = N - 1; k; k--) {
        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1566083941U))
                 - (uint32_t)i;
        i++;
        if (i >= N) { mt[0] = mt[N-1]; i=1; }
    }

    mt[0] = 0x80000000U;
}
```

```c
static void init_genrand(RandomObject *self, uint32_t s) {
    int mti;
    uint32_t *mt;

    mt = self->state;
    mt[0] = s;
    // #define N 624
    for (mti = 1; mti < N; mti++) {
        mt[mti] = (1812433253U * (mt[mti - 1] ^ (mt[mti - 1] >> 30)) + mti);
    }
    self->index = mti;
    return;
}
```


---
## getrandbits

```c
static PyObject *_random_Random_getrandbits_impl(RandomObject *self, int k) {
    int i, words;
    uint32_t r;
    uint32_t *wordarray;
    PyObject *result;

    if (k < 0) {
        PyErr_SetString(PyExc_ValueError, "number of bits must be non-negative");
        return NULL;
    }

    if (k == 0)
        return PyLong_FromLong(0);

    if (k <= 32)
        return PyLong_FromUnsignedLong(genrand_uint32(self) >> (32 - k));

    words = (k - 1) / 32 + 1;
    wordarray = (uint32_t *)PyMem_Malloc(words * 4);
    if (wordarray == NULL) {
        PyErr_NoMemory();
        return NULL;
    }

#if PY_LITTLE_ENDIAN
    for (i = 0; i < words; i++, k -= 32)
#else
    for (i = words - 1; i >= 0; i--, k -= 32)
#endif
    {
        r = genrand_uint32(self);
        if (k < 32)
            r >>= (32 - k);  /* Drop least significant bits */
        wordarray[i] = r;
    }

    result = _PyLong_FromByteArray((unsigned char *)wordarray, words * 4, PY_LITTLE_ENDIAN, 0);
    PyMem_Free(wordarray);
    return result;
}
```

```c
static uint32_t
genrand_uint32(RandomObject *self)
{
    uint32_t y;
    // #define MATRIX_A 0x9908b0dfU 
    static const uint32_t mag01[2] = {0x0U, MATRIX_A};
    uint32_t *mt;

    mt = self->state;
    if (self->index >= N) {
        int kk;

        // #define M 397
        // #define UPPER_MASK 0x80000000U
        // #define LOWER_MASK 0x7fffffffU
        for (kk = 0; kk < N-M; kk++) {
            y = (mt[kk] & UPPER_MASK) | (mt[kk+1] & LOWER_MASK);
            mt[kk] = mt[kk+M] ^ (y >> 1) ^ mag01[y & 0x1U];
        }
        for (; kk < N-1; kk++) {
            y = (mt[kk] & UPPER_MASK) | (mt[kk+1] & LOWER_MASK);
            mt[kk] = mt[kk+(M-N)] ^ (y >> 1) ^ mag01[y & 0x1U];
        }
        y = (mt[N-1] & UPPER_MASK) | (mt[0] & LOWER_MASK);
        mt[N-1] = mt[M-1] ^ (y >> 1) ^ mag01[y & 0x1U];

        self->index = 0;
    }

    y = mt[self->index++];
    y ^= (y >> 11);
    y ^= (y << 7) & 0x9d2c5680U;
    y ^= (y << 15) & 0xefc60000U;
    y ^= (y >> 18);
    return y;
}
```


