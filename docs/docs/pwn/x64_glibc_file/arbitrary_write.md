# Arbitrary Write

## 設置

`size` 要大於 `read_size`，`target_addr` 到 `target_addr + size - 1` 要可寫，`lock_addr` 到 `lock_addr + 15` 要可讀可寫並且沒有被使用

- _flags = _IO_MAGIC & ~(_IO_NO_READS | _IO_EOF_SEEN)
- _fileno = 0
- _IO_read_ptr = 0
- _IO_read_end = 0
- _IO_buf_base = target_addr
- _IO_buf_end = target_addr + size
- _lock = lock_addr


---
## 整理

呼叫 `fwrite(buf, read_size, 1, fp)` 候

- 執行 `read(0, target_addr, size)`（這邊真正讀入的長度要大於 `read_size）`
- 把 `_IO_buf_base` 到 `_IO_buf_base + read_size - 1` copy 到 `buf`
- 把 `_IO_read_base`、`_IO_write_*` 都設成 `target_addr`
- 把 `_IO_read_ptr` 設成 `target_addr + read_size`
- 把 `_IO_read_end` 設成 `target_addr + 讀入長度`


---
## Trace

當呼叫 `fread(buf, read_size, 1, fp)` 的時候

```c
size_t _IO_fread(void *buf, size_t size, size_t count, FILE *fp) {
    size_t bytes_requested = size * count;
    size_t bytes_read;

    // 沒做任何事
    CHECK_FILE(fp, 0);

    if (bytes_requested == 0)
        return 0;

    _IO_acquire_lock(fp);

    bytes_read = _IO_sgetn(fp, (char *)buf, bytes_requested);

    _IO_release_lock(fp);

    return bytes_requested == bytes_read ? count : bytes_read / size;
}
```

```c
size_t _IO_file_xsgetn(FILE *fp, void *data, size_t n) {
    size_t want, have;
    ssize_t count;
    char *s = data;

    want = n;

    // fp->_IO_buf_base != NULL
    if (fp->_IO_buf_base == NULL) {
        // ...
    }

    while (want > 0) {
        have = fp->_IO_read_end - fp->_IO_read_ptr;
        // 1 : have = 0
        // 2 : 剛剛從 stdin 讀進來了多少 bytes，盡量大於 read_size

        if (want <= have) {
            memcpy(s, fp->_IO_read_ptr, want);
            fp->_IO_read_ptr += want;
            want = 0;
        } else {
            if (have > 0) {
                s = __mempcpy(s, fp->_IO_read_ptr, have);
                want -= have;
                fp->_IO_read_ptr += have;
            }

            if (_IO_in_backup(fp)) {
                // ...
            }

            // 1 : fp->_IO_buf_end - fp->_IO_buf_base = size > read_size
            if (fp->_IO_buf_base && want < (size_t)(fp->_IO_buf_end - fp->_IO_buf_base)) {
                if (__underflow(fp) == EOF)
                    break;
                continue;
            }

            // #define _IO_setg(fp, eb, g, eg)  ((fp)->_IO_read_base = (eb), (fp)->_IO_read_ptr = (g), (fp)->_IO_read_end = (eg))
            _IO_setg(fp, fp->_IO_buf_base, fp->_IO_buf_base, fp->_IO_buf_base);
            // #define _IO_setp(__fp, __p, __ep) ((__fp)->_IO_write_base = (__fp)->_IO_write_ptr = __p, (__fp)->_IO_write_end = (__ep))
            _IO_setp(fp, fp->_IO_buf_base, fp->_IO_buf_base);

            count = want;
            if (fp->_IO_buf_base) {
                size_t block_size = fp->_IO_buf_end - fp->_IO_buf_base;
                if (block_size >= 128)
                    count -= want % block_size;
            }

            count = _IO_SYSREAD(fp, s, count);
            if (count <= 0) {
                if (count == 0)
                    fp->_flags |= _IO_EOF_SEEN;
                else
                    fp->_flags |= _IO_ERR_SEEN;
                break;
            }

            s += count;
            want -= count;
            if (fp->_offset != _IO_pos_BAD)
                _IO_pos_adjust(fp->_offset, count);
	    }
    }

    return n - want;
}
```

```c
int __underflow(FILE *fp) {
    if (_IO_vtable_offset(fp) == 0 && _IO_fwide(fp, -1) != -1)
        return EOF;
    if (fp->_mode == 0)
        _IO_fwide(fp, -1);

    // #define _IO_in_put_mode(_fp) ((_fp)->_flags & _IO_CURRENTLY_PUTTING)
    // fp->_flags & _IO_CURRENTLY_PUTTING = 0
    if (_IO_in_put_mode(fp))
        if (_IO_switch_to_get_mode(fp) == EOF)
            return EOF;

    // fp->_IO_read_ptr == fp->_IO_read_end
    if (fp->_IO_read_ptr < fp->_IO_read_end)
        return *(unsigned char *) fp->_IO_read_ptr;

    if (_IO_in_backup(fp)) {
        // ...
    }
    if (_IO_have_markers(fp)) {
        // ...
    }
    else if (_IO_have_backup(fp))
        // ...

    return _IO_UNDERFLOW(fp);
}
```

```c
int _IO_new_file_underflow(FILE *fp) {
    ssize_t count;

    // fp->_flags & _IO_EOF_SEEN = 0
    if (fp->_flags & _IO_EOF_SEEN)
        return EOF;

    // fp->_flags & _IO_NO_READS = 0
    if (fp->_flags & _IO_NO_READS) {
        fp->_flags |= _IO_ERR_SEEN;
        __set_errno(EBADF);
        return EOF;
    }

    // fp->_IO_read_ptr == fp->_IO_read_end
    if (fp->_IO_read_ptr < fp->_IO_read_end)
        return *(unsigned char *)fp->_IO_read_ptr;

    // fp->_IO_buf_base != NULL
    if (fp->_IO_buf_base == NULL) {
        // ...
    }

    // fp->_flags & (_IO_LINE_BUF | _IO_UNBUFFERED = 0
    if (fp->_flags & (_IO_LINE_BUF | _IO_UNBUFFERED)) {
        // ...
    }

    // fp->_IO_read_base = fp->_IO_buf_base
    // fp->_IO_read_ptr, fp->_IO_write_* 都設成 0
    _IO_switch_to_get_mode(fp);

    fp->_IO_read_base = fp->_IO_read_ptr = fp->_IO_buf_base;
    fp->_IO_read_end = fp->_IO_buf_base;
    fp->_IO_write_base = fp->_IO_write_ptr = fp->_IO_write_end = fp->_IO_buf_base;

    // _IO_SYSREAD(fp, target_addr, size) : 從 stdin 讀 size 的 bytes 到 target_addr
    count = _IO_SYSREAD(fp, fp->_IO_buf_base, fp->_IO_buf_end - fp->_IO_buf_base);

    if (count <= 0) {
        if (count == 0)
            fp->_flags |= _IO_EOF_SEEN;
        else
            fp->_flags |= _IO_ERR_SEEN, count = 0;
    }

    fp->_IO_read_end += count;

    if (count == 0) {
        fp->_offset = _IO_pos_BAD;
        return EOF;
    }

    if (fp->_offset != _IO_pos_BAD)
        // #define _IO_pos_adjust(pos, delta) ((pos) += (delta))
        _IO_pos_adjust(fp->_offset, count);

    return *(unsigned char *)fp->_IO_read_ptr;
}
```
