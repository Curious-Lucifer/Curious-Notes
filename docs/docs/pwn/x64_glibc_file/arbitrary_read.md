# Arbitrary Read

## 設置

`src_addr` 到 `src_addr + size - 1` 要可讀，`lock_addr` 到 `lock_addr + 15` 要可讀可寫並且沒有被使用

- _flags = (_IO_MAGIC | _IO_CURRENTLY_PUTTING) & ~_IO_NO_WRITES
- _fileno = 1
- _IO_write_base = src_addr
- _IO_write_ptr  = src_addr + size
- _IO_write_end  = 0
- _IO_read_end   = src_addr
- _lock = lock_addr


---
## 整理

呼叫 `fwrite(buf, write_size, 1, fp)` 後

- 印出 `src` ~ `src + size - 1` 加上 `buf` ~ `buf + write_size - 1` 到 stdout
- `_IO_read_*` 和 `_IO_write_*` 都設成 0


---
## Trace

當呼叫 `fwrite(buf, write_size, 1, fp)` 的時候

```c
size_t _IO_fwrite(const void *buf, size_t size, size_t count, FILE *fp) {
    size_t request = size * count;
    size_t written = 0;

    // 沒做任何事
    CHECK_FILE (fp, 0);

    if (request == 0)
        return 0;

    // fp->_lock 可讀可寫
    _IO_acquire_lock(fp);

    if (_IO_vtable_offset(fp) != 0 || _IO_fwide(fp, -1) == -1)
        written = _IO_sputn(fp, (const char *)buf, request);

    // fp->_lock 可讀可寫
    _IO_release_lock(fp);

    if (written == request || written == EOF)
        return count;
    else
        return written / size;
}
```

```c
size_t _IO_new_file_xsputn(FILE *f, const void *data, size_t n) {
    const char *s = (const char *)data;
    size_t to_do = n;
    int must_flush = 0;
    size_t count = 0;

    if (n <= 0)
        return 0;

    // f->_flags & _IO_LINE_BUF 為 0
    if ((f->_flags & _IO_LINE_BUF) && (f->_flags & _IO_CURRENTLY_PUTTING)) {
        // ...

    // f->_IO_write_end = 0
    } else if (f->_IO_write_end > f->_IO_write_ptr)
        // ...

    // count 到這邊還是 0
    if (count > 0) {
        // ...
    }

    if (to_do + must_flush > 0) {
        size_t block_size, do_write;
        if (_IO_OVERFLOW(f, EOF) == EOF)
	        return to_do == 0 ? EOF : n - to_do;

        block_size = f->_IO_buf_end - f->_IO_buf_base;
        // block_size = 0
        do_write = to_do - (block_size >= 128 ? to_do % block_size : 0);
        // do_write = to_do

        if (do_write) {
            // 印出 buf 到 buf + write_size 到 stdout
            count = new_do_write(f, s, do_write);
            to_do -= count;
            if (count < do_write)
                return n - to_do;
        }

        // to_do = 0
        if (to_do)
	        to_do -= _IO_default_xsputn(f, s + do_write, to_do);
    }

    return n - to_do;
}
```

```c
int _IO_new_file_overflow(FILE *f, int ch) {
    // f->_flags & _IO_NO_WRITES = 0
    if (f->_flags & _IO_NO_WRITES) {
        // ...
    }

    // (f->_flags & _IO_CURRENTLY_PUTTING) = 1
    // f->_IO_write_base != NULL
    if ((f->_flags & _IO_CURRENTLY_PUTTING) == 0 || f->_IO_write_base == NULL) {
        // ...
    }

    if (ch == EOF)
        // _IO_do_write 實際上會去呼叫 _IO_new_do_write
        // 這邊可以看成 _IO_do_write(f, src_addr, size)
        return _IO_do_write(f, f->_IO_write_base, f->_IO_write_ptr - f->_IO_write_base);

    // ...
}
```

```c
int _IO_new_do_write (FILE *fp, const char *data, size_t to_do) {
  return (to_do == 0 || (size_t)new_do_write(fp, data, to_do) == to_do) ? 0 : EOF;
}
```

```c
static size_t new_do_write(FILE *fp, const char *data, size_t to_do) {
    size_t count;

    // fp->_flags & _IO_IS_APPENDING = 0
    if (fp->_flags & _IO_IS_APPENDING)
        // ...

    // fp->_IO_read_end == fp->_IO_write_base
    else if (fp->_IO_read_end != fp->_IO_write_base) {
        // ...
    }

    // #define _IO_SYSWRITE(FP, DATA, LEN) JUMP2(__write, FP, DATA, LEN)
    // _IO_SYSWRITE(fp, src_addr, size) : 從 src_addr 讀 size 個 bytes 到 stdout
    count = _IO_SYSWRITE(fp, data, to_do);

    if (fp->_cur_column && count)
        fp->_cur_column = _IO_adjust_column(fp->_cur_column - 1, data, count) + 1;

    // #define _IO_setg(fp, eb, g, eg)  ((fp)->_IO_read_base = (eb), (fp)->_IO_read_ptr = (g), (fp)->_IO_read_end = (eg))
    // 因為 fp->_IO_buf_base 和 fp->_IO_buf_end 都是 0，所以這邊會把 _IO_read_* 和 _IO_write_* 都寫成 0
    _IO_setg(fp, fp->_IO_buf_base, fp->_IO_buf_base, fp->_IO_buf_base);
    fp->_IO_write_base = fp->_IO_write_ptr = fp->_IO_buf_base;
    fp->_IO_write_end = (fp->_mode <= 0 && (fp->_flags & (_IO_LINE_BUF | _IO_UNBUFFERED)) ? fp->_IO_buf_base : fp->_IO_buf_end);

    return count;
}
```
