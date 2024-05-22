# Basic Concept
> Version : 2.35

## IO_validate_vtable

```c
static inline const struct _IO_jump_t* IO_validate_vtable(const struct _IO_jump_t *vtable) {
    uintptr_t section_length = __stop___libc_IO_vtables - __start___libc_IO_vtables;
    uintptr_t ptr = (uintptr_t)vtable;
    uintptr_t offset = ptr - (uintptr_t)__start___libc_IO_vtables;
    if (__glibc_unlikely(offset >= section_length))
        // TODO : _IO_vtable_check 註解
        _IO_vtable_check();
    return vtable;
}
```


---
## _IO_link_in

```c
void _IO_link_in(struct _IO_FILE_plus *fp) {
    if ((fp->file._flags & _IO_LINKED) == 0) {
        fp->file._flags |= _IO_LINKED;

#ifdef _IO_MTSAFE_IO
        _IO_cleanup_region_start_noarg(flush_cleanup);
        _IO_lock_lock(list_all_lock);
        run_fp = (FILE *)fp;
        _IO_flockfile((FILE *)fp);
#endif

        fp->file._chain = (FILE *)_IO_list_all;
        _IO_list_all = fp;

#ifdef _IO_MTSAFE_IO
        _IO_funlockfile((FILE *)fp);
        run_fp = NULL;
        _IO_lock_unlock(list_all_lock);
        _IO_cleanup_region_end(0);
#endif
    }
}
```


---
## _IO_un_link

```c
void _IO_un_link(struct _IO_FILE_plus *fp) {
    if (fp->file._flags & _IO_LINKED) {
        FILE **f;

#ifdef _IO_MTSAFE_IO
        _IO_cleanup_region_start_noarg(flush_cleanup);
        _IO_lock_lock(list_all_lock);
        run_fp = (FILE *)fp;
        _IO_flockfile((FILE *)fp);
#endif

        if (_IO_list_all == NULL)
            ;
        else if (fp == _IO_list_all)
	        _IO_list_all = (struct _IO_FILE_plus *)_IO_list_all->file._chain;
        else
            for (f = &_IO_list_all->file._chain; *f; f = &(*f)->_chain)
                if (*f == (FILE *)fp) {
                    *f = fp->file._chain;
                    break;
                }

        fp->file._flags &= ~_IO_LINKED;

#ifdef _IO_MTSAFE_IO
        _IO_funlockfile((FILE *) fp);
        run_fp = NULL;
        _IO_lock_unlock(list_all_lock);
        _IO_cleanup_region_end(0);
#endif
    }
}
```


---
## JUMP0、JUMP1、JUMP2、JUMP3

```c
// 目前的討論範圍 THIS 的 type 都會是 (FILE *)，且 ((struct _IO_FILE_plus *)THIS)->vtable 會指向 _IO_file_jumps
#define JUMP0(FUNC, THIS) (_IO_JUMPS_FUNC(THIS)->FUNC) (THIS)
#define JUMP1(FUNC, THIS, X1) (_IO_JUMPS_FUNC(THIS)->FUNC) (THIS, X1)
#define JUMP2(FUNC, THIS, X1, X2) (_IO_JUMPS_FUNC(THIS)->FUNC) (THIS, X1, X2)
#define JUMP3(FUNC, THIS, X1,X2,X3) (_IO_JUMPS_FUNC(THIS)->FUNC) (THIS, X1,X2, X3)
```

```c
#define _IO_JUMPS_FUNC(THIS) (IO_validate_vtable(_IO_JUMPS_FILE_plus(THIS)))
```

```c
#define _IO_JUMPS_FILE_plus(THIS) _IO_CAST_FIELD_ACCESS((THIS), struct _IO_FILE_plus, vtable)
```

```c
#define _IO_CAST_FIELD_ACCESS(THIS, TYPE, MEMBER) ( \
    *(_IO_MEMBER_TYPE(TYPE, MEMBER) *)(((char *)(THIS)) + offsetof(TYPE, MEMBER)))
```

```c
#define _IO_file_jumps (__io_vtables[IO_FILE_JUMPS])
```

```c
const struct _IO_jump_t __io_vtables[] attribute_relro = {
    // ...

    [IO_FILE_JUMPS] = {
        JUMP_INIT_DUMMY,
        JUMP_INIT(finish, _IO_file_finish),
        JUMP_INIT(overflow, _IO_file_overflow),
        JUMP_INIT(underflow, _IO_file_underflow),
        JUMP_INIT(uflow, _IO_default_uflow),
        JUMP_INIT(pbackfail, _IO_default_pbackfail),
        JUMP_INIT(xsputn, _IO_file_xsputn),
        JUMP_INIT(xsgetn, _IO_file_xsgetn),
        JUMP_INIT(seekoff, _IO_new_file_seekoff),
        JUMP_INIT(seekpos, _IO_default_seekpos),
        JUMP_INIT(setbuf, _IO_new_file_setbuf),
        JUMP_INIT(sync, _IO_new_file_sync),
        JUMP_INIT(doallocate, _IO_file_doallocate),
        JUMP_INIT(read, _IO_file_read),
        JUMP_INIT(write, _IO_new_file_write),
        JUMP_INIT(seek, _IO_file_seek),
        JUMP_INIT(close, _IO_file_close),
        JUMP_INIT(stat, _IO_file_stat),
        JUMP_INIT(showmanyc, _IO_default_showmanyc),
        JUMP_INIT(imbue, _IO_default_imbue)
    },

    // ...
}
```


---
## _IO_doallocbuf

```c
void _IO_doallocbuf(FILE *fp) {
    if (fp->_IO_buf_base)
        return;

    // fp->_mode > 0  代表 fp 使用的是寬字符模式
    // fp->_mode == 0 代表 fp 還沒有指定字符模式
    // fp->_mode < 0  代表 fp 使用的是窄字符模式
    if (!(fp->_flags & _IO_UNBUFFERED) || fp->_mode > 0)
        // #define _IO_DOALLOCATE(FP) JUMP0(__doallocate, FP)
        if (_IO_DOALLOCATE(fp) != EOF)
            return;

    _IO_setb(fp, fp->_shortbuf, fp->_shortbuf + 1, 0);
}
```

```c
int _IO_file_doallocate(FILE *fp) {
    size_t size;
    char *p;
    struct __stat64_t64 st;

    // #define BUFSIZ 8192
    size = BUFSIZ;  

    // #define _IO_SYSSTAT(FP, BUF) JUMP1(__stat, FP, BUF)
    // _IO_file_stat 會把 fp->_fileno 對應的檔案狀態存到 st，成功會回傳 0，失敗回傳 -1
    if (fp->_fileno >= 0 && __builtin_expect(_IO_SYSSTAT(fp, &st), 0) >= 0) {

        // S_ISCHR(st.st_mode) 判斷文件是不是 character device file
        if (S_ISCHR(st.st_mode)) {
	        // ...
	    }

#if defined _STATBUF_ST_BLKSIZE
        // st.st_blksize 是文件系統建議的 block size
        if (st.st_blksize > 0 && st.st_blksize < BUFSIZ)
	        size = st.st_blksize;
#endif
    }

    p = malloc(size);
    if (__glibc_unlikely(p == NULL))
        return EOF;

    _IO_setb(fp, p, p + size, 1);
    return 1;
}
```

```c
void _IO_setb(FILE *f, char *b, char *eb, int a) {
    if (f->_IO_buf_base && !(f->_flags & _IO_USER_BUF))
        free(f->_IO_buf_base);

    f->_IO_buf_base = b;
    f->_IO_buf_end = eb;

    if (a)
        f->_flags &= ~_IO_USER_BUF;
    else
        f->_flags |= _IO_USER_BUF;
}
```


---
## _IO_OVERFLOW

```c
#define _IO_OVERFLOW(FP, CH) JUMP1(__overflow, FP, CH)
```

```c
// overflow 對應到的函數是 _IO_file_overflow，但呼叫 _IO_file_overflow 實際上會呼叫的是 _IO_new_file_overflow
int _IO_new_file_overflow(FILE *f, int ch) {
    if (f->_flags & _IO_NO_WRITES) {
        f->_flags |= _IO_ERR_SEEN;
        __set_errno(EBADF);
        return EOF;
    }

    if ((f->_flags & _IO_CURRENTLY_PUTTING) == 0 || f->_IO_write_base == NULL) {
        if (f->_IO_write_base == NULL) {
            _IO_doallocbuf(f);

            // #define _IO_setg(fp, eb, g, eg) ( \
            //     (fp)->_IO_read_base = (eb), (fp)->_IO_read_ptr = (g), (fp)->_IO_read_end = (eg))
            _IO_setg(f, f->_IO_buf_base, f->_IO_buf_base, f->_IO_buf_base);
	    }

        if (__glibc_unlikely(_IO_in_backup(f))) {
            // ...
        }

        if (f->_IO_read_ptr == f->_IO_buf_end)
	        f->_IO_read_end = f->_IO_read_ptr = f->_IO_buf_base;
        f->_IO_write_ptr = f->_IO_read_ptr;
        f->_IO_write_base = f->_IO_write_ptr;
        f->_IO_write_end = f->_IO_buf_end;
        f->_IO_read_base = f->_IO_read_ptr = f->_IO_read_end;

        f->_flags |= _IO_CURRENTLY_PUTTING;

        if (f->_mode <= 0 && f->_flags & (_IO_LINE_BUF | _IO_UNBUFFERED))
	        f->_IO_write_end = f->_IO_write_ptr;
    }

    if (ch == EOF)
        // _IO_do_write 實際上會去呼叫 _IO_new_do_write
        return _IO_do_write(f, f->_IO_write_base, f->_IO_write_ptr - f->_IO_write_base);

    if (f->_IO_write_ptr == f->_IO_buf_end)
        if (_IO_do_flush(f) == EOF)
            return EOF;

    *f->_IO_write_ptr++ = ch;
    if ((f->_flags & _IO_UNBUFFERED) || ((f->_flags & _IO_LINE_BUF) && ch == '\n'))
        if (_IO_do_write(f, f->_IO_write_base, f->_IO_write_ptr - f->_IO_write_base) == EOF)
            return EOF;

    return (unsigned char)ch;
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

    if (fp->_flags & _IO_IS_APPENDING)
        fp->_offset = _IO_pos_BAD;

    else if (fp->_IO_read_end != fp->_IO_write_base) {
        off64_t new_pos = _IO_SYSSEEK(fp, fp->_IO_write_base - fp->_IO_read_end, 1);
        if (new_pos == _IO_pos_BAD)
	        return 0;
        fp->_offset = new_pos;
    }

    // #define _IO_SYSWRITE(FP, DATA, LEN) JUMP2(__write, FP, DATA, LEN)
    count = _IO_SYSWRITE(fp, data, to_do);

    if (fp->_cur_column && count)
        fp->_cur_column = _IO_adjust_column(fp->_cur_column - 1, data, count) + 1;

    // #define _IO_setg(fp, eb, g, eg)  ((fp)->_IO_read_base = (eb), (fp)->_IO_read_ptr = (g), (fp)->_IO_read_end = (eg))
    _IO_setg(fp, fp->_IO_buf_base, fp->_IO_buf_base, fp->_IO_buf_base);

    fp->_IO_write_base = fp->_IO_write_ptr = fp->_IO_buf_base;

    fp->_IO_write_end = (fp->_mode <= 0 && (fp->_flags & (_IO_LINE_BUF | _IO_UNBUFFERED)) ? fp->_IO_buf_base : fp->_IO_buf_end);

    return count;
}
```

```c
ssize_t _IO_new_file_write(FILE *f, const void *data, ssize_t n) {
    ssize_t to_do = n;
    while (to_do > 0) {
        ssize_t count = (__builtin_expect(f->_flags2 & _IO_FLAGS2_NOTCANCEL, 0)
            ? __write_nocancel(f->_fileno, data, to_do)
            : __write(f->_fileno, data, to_do)
        );

        if (count < 0) {
            f->_flags |= _IO_ERR_SEEN;
            break;
        }

        to_do -= count;
        data = (void *)((char *)data + count);
    }

    n -= to_do;
    if (f->_offset >= 0)
        f->_offset += n;
    return n;
}
```

```c
unsigned _IO_adjust_column(unsigned start, const char *line, int count) {
    const char *ptr = line + count;
    while (ptr > line)
        if (*--ptr == '\n')
            return line + count - ptr - 1;
    return start + count;
}
```

```c
#define _IO_do_flush(_f) ((_f)->_mode <= 0 \
    ? _IO_do_write(_f, (_f)->_IO_write_base, (_f)->_IO_write_ptr - (_f)->_IO_write_base)		      \
    : _IO_wdo_write(_f, (_f)->_wide_data->_IO_write_base, ((_f)->_wide_data->_IO_write_ptr - (_f)->_wide_data->_IO_write_base)))
// 呼叫 _IO_do_write 實際上會去呼叫 _IO_new_do_write
```


---
## _IO_UNDERFLOW

```c
#define _IO_UNDERFLOW(FP) JUMP0(__underflow, FP)
```

```c
// underflow 對應到的函數是 _IO_file_underflow，但呼叫 _IO_file_underflow 實際上會呼叫的是 _IO_new_file_underflow
int _IO_new_file_underflow(FILE *fp) {
    ssize_t count;

    if (fp->_flags & _IO_EOF_SEEN)
        return EOF;

    if (fp->_flags & _IO_NO_READS) {
        fp->_flags |= _IO_ERR_SEEN;
        __set_errno(EBADF);
        return EOF;
    }

    if (fp->_IO_read_ptr < fp->_IO_read_end)
        return *(unsigned char *)fp->_IO_read_ptr;

    if (fp->_IO_buf_base == NULL) {
        if (fp->_IO_save_base != NULL) {
            // ...
        }
        _IO_doallocbuf(fp);
    }

    if (fp->_flags & (_IO_LINE_BUF | _IO_UNBUFFERED)) {
        _IO_acquire_lock(stdout);
        if ((stdout->_flags & (_IO_LINKED | _IO_NO_WRITES | _IO_LINE_BUF)) == (_IO_LINKED | _IO_LINE_BUF))
	        _IO_OVERFLOW(stdout, EOF);
        _IO_release_lock(stdout);
    }

    _IO_switch_to_get_mode(fp);

    fp->_IO_read_base = fp->_IO_read_ptr = fp->_IO_buf_base;
    fp->_IO_read_end = fp->_IO_buf_base;
    fp->_IO_write_base = fp->_IO_write_ptr = fp->_IO_write_end = fp->_IO_buf_base;

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

```c
int _IO_switch_to_get_mode(FILE *fp) {
    if (fp->_IO_write_ptr > fp->_IO_write_base)
        if (_IO_OVERFLOW(fp, EOF) == EOF)
            return EOF;

    if (_IO_in_backup(fp))
        fp->_IO_read_base = fp->_IO_backup_base;
    else {
        fp->_IO_read_base = fp->_IO_buf_base;
        if (fp->_IO_write_ptr > fp->_IO_read_end)
	        fp->_IO_read_end = fp->_IO_write_ptr;
    }

    fp->_IO_read_ptr = fp->_IO_write_ptr;
    fp->_IO_write_base = fp->_IO_write_ptr = fp->_IO_write_end = fp->_IO_read_ptr;
    fp->_flags &= ~_IO_CURRENTLY_PUTTING;

    return 0;
}
```

```c
#define _IO_SYSREAD(FP, DATA, LEN) JUMP2(__read, FP, DATA, LEN)
```

```c
ssize_t _IO_file_read(FILE *fp, void *buf, ssize_t size) {
    return (__builtin_expect(fp->_flags2 & _IO_FLAGS2_NOTCANCEL, 0)
        ? __read_nocancel(fp->_fileno, buf, size)
        : __read(fp->_fileno, buf, size));
}
```


---
## fopen

```c
FILE *_IO_new_fopen(const char *filename, const char *mode) {
    return __fopen_internal(filename, mode, 1);
}
```

```c
FILE *__fopen_internal(const char *filename, const char *mode, int is32) {
    struct locked_FILE {
        struct _IO_FILE_plus fp;
        _IO_lock_t lock;
        struct _IO_wide_data wd;
    } *new_f = (struct locked_FILE *)malloc(sizeof(struct locked_FILE));

    if (new_f == NULL)
        return NULL;

    new_f->fp.file._lock = &new_f->lock;

    // new_f->fp.file._flags = _IO_MAGIC
    // new_f->fp.file._wide_data = &new_f->wd
    // new_f->wd._wide_vtable = &_IO_wfile_jumps
    // 除了以上和 new_f->fp.file._lock 其它都寫 0
    _IO_no_init(&new_f->fp.file, 0, 0, &new_f->wd, &_IO_wfile_jumps);

    // new_f->fp.vtable = &_IO_file_jumps
    _IO_JUMPS(&new_f->fp) = &_IO_file_jumps;

    // new_f->fp.file._offset = _IO_pos_BAD (-1)
    // new_f->fp.file._flags |= CLOSED_FILEBUF_FLAGS
    // new_f->fp.file._fileno = -1
    // 呼叫 _IO_link_in
    _IO_new_file_init_internal(&new_f->fp);

    // _IO_file_fopen 實際上會呼叫 _IO_new_file_fopen
    if (_IO_file_fopen((FILE *)new_f, filename, mode, is32) != NULL)
        return __fopen_maybe_mmap(&new_f->fp.file);

    _IO_un_link(&new_f->fp);
    free(new_f);
    return NULL;
}
```

```c
FILE* _IO_new_file_fopen(FILE *fp, const char *filename, const char *mode, int is32not64) {
    int oflags = 0, omode;
    int read_write;
    int oprot = 0666;
    int i;
    FILE *result;
    const char *cs;
    const char *last_recognized;

    // fp->_fileno != -1
    if (_IO_file_is_open(fp))
        return 0;

    switch (*mode) {
        case 'r':
            omode = O_RDONLY;
            read_write = _IO_NO_WRITES;
            break;
        case 'w':
            omode = O_WRONLY;
            oflags = O_CREAT|O_TRUNC;
            read_write = _IO_NO_READS;
            break;
        case 'a':
            omode = O_WRONLY;
            oflags = O_CREAT|O_APPEND;
            read_write = _IO_NO_READS|_IO_IS_APPENDING;
            break;
        default:
            __set_errno(EINVAL);
            return NULL;
    }
    last_recognized = mode;
    for (i = 1; i < 7; ++i) {
        switch (*++mode) {
            case '\0':
                break;
            case '+':
                omode = O_RDWR;
                read_write &= _IO_IS_APPENDING;
                last_recognized = mode;
                continue;
            case 'x':
                oflags |= O_EXCL;
                last_recognized = mode;
                continue;
            case 'b':
                last_recognized = mode;
                continue;
            case 'm':
                fp->_flags2 |= _IO_FLAGS2_MMAP;
                continue;
            case 'c':
                fp->_flags2 |= _IO_FLAGS2_NOTCANCEL;
                continue;
            case 'e':
                oflags |= O_CLOEXEC;
                fp->_flags2 |= _IO_FLAGS2_CLOEXEC;
                continue;
            default:
                /* Ignore.  */
                continue;
	    }
        break;
    }

    result = _IO_file_open(fp, filename, omode|oflags, oprot, read_write,  is32not64);

    if (result != NULL) {
        cs = strstr (last_recognized + 1, ",ccs=");
        if (cs != NULL) {
            // ...
	    }
    }

    return result;
}
```

```c
FILE* _IO_file_open(FILE *fp, const char *filename, int posix_mode, int prot, int read_write, int is32not64) {
    int fdesc;
    if (__glibc_unlikely(fp->_flags2 & _IO_FLAGS2_NOTCANCEL))
        fdesc = __open_nocancel(filename, posix_mode | (is32not64 ? 0 : O_LARGEFILE), prot);
    else
        fdesc = __open(filename, posix_mode | (is32not64 ? 0 : O_LARGEFILE), prot);
    if (fdesc < 0)
        return NULL;
    fp->_fileno = fdesc;

    // #define _IO_mask_flags(fp, f, mask) ((fp)->_flags = ((fp)->_flags & ~(mask)) | ((f) & (mask)))
    _IO_mask_flags(fp, read_write, _IO_NO_READS+_IO_NO_WRITES+_IO_IS_APPENDING);

    if ((read_write & (_IO_IS_APPENDING | _IO_NO_READS)) == (_IO_IS_APPENDING | _IO_NO_READS)) {
        off64_t new_pos = _IO_SYSSEEK(fp, 0, _IO_seek_end);
        if (new_pos == _IO_pos_BAD && errno != ESPIPE) {
            __close_nocancel(fdesc);
            return NULL;
        }
    }

    _IO_link_in((struct _IO_FILE_plus*)fp);
    return fp;
}
```

```c
#define _IO_SYSSEEK(FP, OFFSET, MODE) JUMP2(__seek, FP, OFFSET, MODE)
```

```c
off64_t _IO_file_seek(FILE *fp, off64_t offset, int dir) {
    return __lseek64(fp->_fileno, offset, dir);
}
```

```c
off64_t __lseek64 (int fd, off64_t offset, int whence) {
#ifdef __NR_llseek
#define __NR__llseek __NR_llseek
#endif

#ifdef __NR__llseek
    loff_t res;
    int rc = INLINE_SYSCALL_CALL(_llseek, fd, (long)(((uint64_t)offset) >> 32), (long)offset, &res, whence);
    return rc ?: res;
#else
    return INLINE_SYSCALL_CALL (lseek, fd, offset, whence);
#endif
}
```

```c
FILE* __fopen_maybe_mmap(FILE *fp) {
#if _G_HAVE_MMAP
    if ((fp->_flags2 & _IO_FLAGS2_MMAP) && (fp->_flags & _IO_NO_WRITES)) {
        // 重設 ((struct _IO_FILE_plus *)fp)->vtable
        if (fp->_mode <= 0)
            _IO_JUMPS_FILE_plus(fp) = &_IO_file_jumps_maybe_mmap;
        else
            _IO_JUMPS_FILE_plus(fp) = &_IO_wfile_jumps_maybe_mmap;

        fp->_wide_data->_wide_vtable = &_IO_wfile_jumps_maybe_mmap;
    }
#endif
    return fp;
}
```


---
## fread

```c
size_t _IO_fread(void *buf, size_t size, size_t count, FILE *fp) {
    size_t bytes_requested = size * count;
    size_t bytes_read;

    // 沒做任何事
    CHECK_FILE(fp, 0);

    if (bytes_requested == 0)
        return 0;

    // _IO_flockfile(fp)
    _IO_acquire_lock(fp);

    bytes_read = _IO_sgetn(fp, (char *)buf, bytes_requested);

    // _IO_funlockfile(fp)
    _IO_release_lock(fp);

    return bytes_requested == bytes_read ? count : bytes_read / size;
}
```

```c
size_t _IO_sgetn(FILE *fp, void *data, size_t n) {
  return _IO_XSGETN(fp, data, n);
}
```

```c
#define _IO_XSGETN(FP, DATA, N) JUMP2(__xsgetn, FP, DATA, N)
```

```c
size_t _IO_file_xsgetn(FILE *fp, void *data, size_t n) {
    size_t want, have;
    ssize_t count;
    char *s = data;

    want = n;

    if (fp->_IO_buf_base == NULL) {
        if (fp->_IO_save_base != NULL) {
            // ...
        }
        _IO_doallocbuf(fp);
    }

    while (want > 0) {
        have = fp->_IO_read_end - fp->_IO_read_ptr;
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
    // _IO_fwide(fp, 1) 代表嘗試把 fp->_mode 設定成 1（寬字符模式）並回傳 1
    // _IO_fwide(fp, 0) 代表直接回傳 fp->_mode
    // _IO_fwide(fp, -1) 代表嘗試把 fp->_mode 設定成 -1（窄字符模式）並回傳 -1
    if (_IO_vtable_offset(fp) == 0 && _IO_fwide(fp, -1) != -1)
        return EOF;
    if (fp->_mode == 0)
        _IO_fwide(fp, -1);

    // #define _IO_in_put_mode(_fp) ((_fp)->_flags & _IO_CURRENTLY_PUTTING)
    if (_IO_in_put_mode(fp))
        if (_IO_switch_to_get_mode(fp) == EOF)
            return EOF;

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


---
## fwrite

```c
size_t _IO_fwrite(const void *buf, size_t size, size_t count, FILE *fp) {
    size_t request = size * count;
    size_t written = 0;

    // 沒做任何事
    CHECK_FILE(fp, 0);

    if (request == 0)
        return 0;

    _IO_acquire_lock(fp);
    if (_IO_vtable_offset(fp) != 0 || _IO_fwide(fp, -1) == -1)
        written = _IO_sputn(fp, (const char *)buf, request);
    _IO_release_lock(fp);

    if (written == request || written == EOF)
        return count;
    else
        return written / size;
}
```

```c
#define _IO_sputn(__fp, __s, __n) _IO_XSPUTN(__fp, __s, __n)
```

```c
#define _IO_XSPUTN(FP, DATA, N) JUMP2(__xsputn, FP, DATA, N)
```

```c
// 呼叫 _IO_file_xsputn 實際上是呼叫 _IO_new_file_xsputn
size_t _IO_new_file_xsputn(FILE *f, const void *data, size_t n) {
    const char *s = (const char *)data;
    size_t to_do = n;
    int must_flush = 0;
    size_t count = 0;

    if (n <= 0)
        return 0;

    if ((f->_flags & _IO_LINE_BUF) && (f->_flags & _IO_CURRENTLY_PUTTING)) {
        count = f->_IO_buf_end - f->_IO_write_ptr;
        if (count >= n) {
            const char *p;
            for (p = s + n; p > s; ) {
                if (*--p == '\n') {
                    count = p - s + 1;
                    must_flush = 1;
                    break;
                }
            }
        }
    } else if (f->_IO_write_end > f->_IO_write_ptr)
        count = f->_IO_write_end - f->_IO_write_ptr;

    if (count > 0) {
        if (count > to_do)
            count = to_do;
        f->_IO_write_ptr = __mempcpy(f->_IO_write_ptr, s, count);
        s += count;
        to_do -= count;
    }

    if (to_do + must_flush > 0) {
        size_t block_size, do_write;
        if (_IO_OVERFLOW(f, EOF) == EOF)
	        return to_do == 0 ? EOF : n - to_do;

        block_size = f->_IO_buf_end - f->_IO_buf_base;
        do_write = to_do - (block_size >= 128 ? to_do % block_size : 0);

        if (do_write) {
            count = new_do_write(f, s, do_write);
            to_do -= count;
            if (count < do_write)
                return n - to_do;
        }

        if (to_do)
	        to_do -= _IO_default_xsputn(f, s + do_write, to_do);
    }

    return n - to_do;
}
```

```c
size_t _IO_default_xsputn(FILE *f, const void *data, size_t n) {
    const char *s = (char *)data;
    size_t more = n;

    if (more <= 0)
        return 0;

    for (;;) {
        if (f->_IO_write_ptr < f->_IO_write_end) {
            size_t count = f->_IO_write_end - f->_IO_write_ptr;
            if (count > more)
                count = more;

            if (count > 20) {
                f->_IO_write_ptr = __mempcpy(f->_IO_write_ptr, s, count);
                s += count;
            } else if (count) {
                char *p = f->_IO_write_ptr;
                ssize_t i;
                for (i = count; --i >= 0; )
                    *p++ = *s++;
                f->_IO_write_ptr = p;
            }

            more -= count;
        }

        if (more == 0 || _IO_OVERFLOW(f, (unsigned char)*s++) == EOF)
            break;
        more--;
    }

    return n - more;
}
```


---
## fclose

```c
int _IO_new_fclose(FILE *fp) {
    int status;

    // 沒做任何事
    CHECK_FILE(fp, EOF);

    if (fp->_flags & _IO_IS_FILEBUF)
        _IO_un_link((struct _IO_FILE_plus *)fp);

    _IO_acquire_lock(fp);
    if (fp->_flags & _IO_IS_FILEBUF)
        // 呼叫 _IO_file_close_it 實際上會呼叫 _IO_new_file_close_it
        status = _IO_file_close_it(fp);
    else
        status = fp->_flags & _IO_ERR_SEEN ? -1 : 0;
    _IO_release_lock(fp);

    _IO_FINISH(fp);

    if (fp->_mode > 0) {
        // ...
    } else {
        if (_IO_have_backup(fp))
            _IO_free_backup_area(fp);
    }

    _IO_deallocate_file(fp);

    return status;
}
```

```c
int _IO_new_file_close_it(FILE *fp) {
    int write_status;
    // _IO_file_is_open 檢查 fp->_fileno != -1
    if (!_IO_file_is_open(fp))
        return EOF;

    if ((fp->_flags & _IO_NO_WRITES) == 0 && (fp->_flags & _IO_CURRENTLY_PUTTING) != 0)
        write_status = _IO_do_flush(fp);
    else
        write_status = 0;

    _IO_unsave_markers(fp);

    // _IO_SYSCLOSE 就是對 fp->_fileno 執行 close 這個 syscall
    int close_status = ((fp->_flags2 & _IO_FLAGS2_NOCLOSE) == 0 ? _IO_SYSCLOSE(fp) : 0);

    if (fp->_mode > 0) {
        // ...
    }

    // 把 fp->_IO_buf_base free 掉，並把 fp->_flags 的 _IO_USER_BUF set 起來
    // 把 fp 的 _IO_buf_* _IO_read_* _IO_write_* 全 set 成 0
    _IO_setb(fp, NULL, NULL, 0);
    _IO_setg(fp, NULL, NULL, NULL);
    _IO_setp(fp, NULL, NULL);

    _IO_un_link((struct _IO_FILE_plus *)fp);
    fp->_flags = _IO_MAGIC | CLOSED_FILEBUF_FLAGS;
    fp->_fileno = -1;
    fp->_offset = _IO_pos_BAD;

    return close_status ? close_status : write_status;
}
```

```c
#define _IO_FINISH(FP) JUMP1(__finish, FP, 0)
```

```c
// 呼叫 _IO_file_finish 實際上會去呼叫 _IO_new_file_finish
void _IO_new_file_finish(FILE *fp, int dummy) {
    if (_IO_file_is_open(fp)) {
        _IO_do_flush(fp);
        if (!(fp->_flags & _IO_DELETE_DONT_CLOSE))
            _IO_SYSCLOSE(fp);
    }

    _IO_default_finish(fp, 0);
}
```

```c
void _IO_default_finish(FILE *fp, int dummy) {
    struct _IO_marker *mark;

    if (fp->_IO_buf_base && !(fp->_flags & _IO_USER_BUF)) {
        free(fp->_IO_buf_base);
        fp->_IO_buf_base = fp->_IO_buf_end = NULL;
    }

    for (mark = fp->_markers; mark != NULL; mark = mark->_next)
        mark->_sbuf = NULL;

    if (fp->_IO_save_base) {
        free(fp->_IO_save_base);
        fp->_IO_save_base = NULL;
    }

    _IO_un_link((struct _IO_FILE_plus *)fp);

#ifdef _IO_MTSAFE_IO
    if (fp->_lock != NULL)
        _IO_lock_fini(*fp->_lock);
#endif
}
```

```c
static inline void _IO_deallocate_file(FILE *fp) {
    if (fp == (FILE *)&_IO_2_1_stdin_ || fp == (FILE *)&_IO_2_1_stdout_ || fp == (FILE *)&_IO_2_1_stderr_)
        return;

    free(fp);
}
```
