# Flask Debug Mode

## PIN & Cookie
### Generate
如果沒有做什麼特別的環境變數設定的話，可以從 `werkzeug/debug/__init__.py` 中得到 PIN、cookie name 和 cookie value 在 Linux 中是怎麼被 generate 的

PIN & cookie name : 
```python
def get_machine_id():
    linux = b""

    for filename in "/etc/machine-id", "/proc/sys/kernel/random/boot_id":
        try:
            with open(filename, "rb") as f:
                value = f.readline().strip()
        except OSError:
            continue
        
        if value:
            linux += value
            break

    try:
        with open("/proc/self/cgroup", "rb") as f:
            linux += f.readline().strip().rpartition(b"/")[2]
    except OSError:
        pass

    return linux


def get_pin_and_cookie_name(app: WSGIApplication):
    modname = getattr(app, "__module__", t.cast(object, app).__class__.__module__)
    try:
        username = getpass.getuser()
    except (ImportError, KeyError):
        username = None
    mod = sys.modules.get(modname)

    probably_public_bits = [
        username,                                     # Default : current user's username
        modname,                                      # Default : "flask.app"
        getattr(app, "__name__", type(app).__name__), # Default : "Flask"
        getattr(mod, "__file__", None),               # Default : "{Python packages path}/flask/app.py"，通常在 debug page 會直接寫出來
    ]

    private_bits = [
        str(uuid.getnode()), # uuid.getnode() 是把電腦的 MAC address 合併然後轉成十進位
        get_machine_id()
    ]

    h = hashlib.sha1()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode("utf-8")
        h.update(bit)
    h.update(b"cookiesalt")

    cookie_name = f"__wzd{h.hexdigest()[:20]}"

    h.update(b"pinsalt")
    num = f"{int(h.hexdigest(), 16):09d}"[:9]

    # rv 的值就是 PIN
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = "-".join(
                num[x : x + group_size].rjust(group_size, "0")
                for x in range(0, len(num), group_size)
            )
            break
    else:
        rv = num

    return rv, cookie_name
```

cookie value :
```python
def hash_pin(pin: str):
    return hashlib.sha1(f"{pin} added salt".encode("utf-8", "replace")).hexdigest()[:12]

cookie = f"{int(time.time())}|{hash_pin(pin)}"
```

> 因為 PIN 的產生方式是直接從電腦的固定資訊經過一些運算得出，如果可以得知電腦的那些固定資訊，那 PIN 碼或 cookie name/value 就可以直接被計算出來


### Auth
同樣的也可以從 `werkzeug/debug/__init__.py` 得到 PIN 或 cookie 的驗證邏輯

cookie 驗證 :
```python
def check_pin_trust(self, environ: WSGIEnvironment):
    val = parse_cookie(environ).get(self.pin_cookie_name)
    if not val or "|" not in val:
        return False
    ts_str, pin_hash = val.split("|", 1)

    try:
        ts = int(ts_str)
    except ValueError:
        return False

    if pin_hash != hash_pin(self.pin):
        return None
    return (time.time() - PIN_TIME) < ts
```

PIN 驗證 :
```python
def _fail_pin_auth(self):
    time.sleep(5.0 if self._failed_pin_auth > 5 else 0.5)
    self._failed_pin_auth += 1

def pin_auth(self, request: Request):
    exhausted = False
    auth = False
    trust = self.check_pin_trust(request.environ)
    pin = t.cast(str, self.pin)

    bad_cookie = False
    if trust is None:
        self._fail_pin_auth()
        bad_cookie = True
    elif trust:
        auth = True
    elif self._failed_pin_auth > 10:
        exhausted = True
    else:
        entered_pin = request.args["pin"]
        if entered_pin.strip().replace("-", "") == pin.replace("-", ""):
            self._failed_pin_auth = 0
            auth = True
        else:
            self._fail_pin_auth()

    rv = Response(
        json.dumps({"auth": auth, "exhausted": exhausted}),
        mimetype="application/json",
    )
    if auth:
        rv.set_cookie(
            self.pin_cookie_name,
            f"{int(time.time())}|{hash_pin(pin)}",
            httponly=True,
            samesite="Strict",
            secure=request.is_secure,
        )
    elif bad_cookie:
        rv.delete_cookie(self.pin_cookie_name)
    return rv
```

> `pin_auth` 要在驗證 PIN 是否正確時才會被呼叫到，而且最多只能錯誤 10 次，之後 debug 的功能就會直接被鎖起來。但 `check_pin_trust` 在 render debug page、debug console 之類的操作時都會被呼叫到，而且沒有次數限制，所以可以直接透過觀察 debug page 來確認 cookie 是否是正確的

