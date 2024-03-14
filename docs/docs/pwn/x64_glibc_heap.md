# x64 Glibc Heap

## Basic Concept
### Bin Table

| Name | Chunk Size | Usage | Priority | 
| --- | --- | --- | --- | 
| Tcache Bin | 0x20 ~ 0x410 | FILO | 1 | 
| Fast Bin | 0x20 ~ 0x80 | FILO | 2 | 
| Unsorted Bin | $\ge$ 0x80 | FIFO | 4 | 
| Small Bin | 0x20 ~ 0x3f0 | FIFO | 3 | 
| Large Bin | $\ge$ 0x400 | FIFO | 5 | 


### `tcache_perthread_struct`

chunk size 為 0x290，`TCACHE_MAX_BINS` 為 64

```c
typedef struct tcache_perthread_struct
{
    uint16_t counts[TCACHE_MAX_BINS];
    tcache_entry *entries[TCACHE_MAX_BINS];
} tcache_perthread_struct;
```


### Arena

main thread 的 `malloc_state` 叫 `main_arena`

```c
struct malloc_state
{
    ...

    /* Fast Bin, NFASTBINS 為 10 */
    mfastbinptr fastbinsY[NFASTBINS];
    /* Top Chunk */
    mchunkptr top;
    /* 最近被切的 chunk 所剩下的 chunk */
    mchunkptr last_remainder;
    /* Unsorted Bin, Small Bin, Large Bin  */
    mchunkptr bins[NBINS * 2 - 2];

    ...
};
```

