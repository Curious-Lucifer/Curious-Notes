# PHP Filter

對於被 `php://filter/read=zlib.deflate|convert.base64-encode/resource=<file>` 壓縮過的內容可以用以下 script 解壓縮

```python
import zlib, base64

msg = b'...'

plain = zlib.decompress(base64.b64decode(msg), wbits=-zlib.MAX_WBITS)
```

