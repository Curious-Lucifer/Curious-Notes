# Python Requests

## GET
```python
import requests as req

r = req.get('<url>')

r = req.get('<url>', allow_redirects=False)

r = req.get('<url>', timeout=0.01)

r = req.get('<url>', headers={'<header key>': '<header val>'})

r = req.get('<url>', params={'<key1>': '<val1>', '<key2>': '<val2>'})

r = req.get('<url>', cookies={'<key>': '<val>'})

jar = req.cookies.RequestsCookieJar()
jar.set('<cookie key>', '<cookie val>', domain='<domain>', path='<path>')
r = req.get('<url>', cookies=jar)
```


---
## POST
```python
import requests as req

r = req.post('<url>', data='some string')

r = req.post('<url>', data={'<key1>': '<val1>', '<key2>': '<val2>'})

r = req.post('<url>', json={'<key>': '<val>'})

# multipart/form-data
r = req.post('<url>', files={'<name>': open('<filename>', 'rb')})
# if dont's want the <new_filename>/<MIME type>, set it to None
r = req.post('<url>', files={'<name>': ('<new_filename>', open('<filename>', 'rb'), '<MIME type>', {'<header key>': '<header val>'})})
```


---
## Response Object
```python
import requests as req

# r will be the response obeject of <url> or the url that <url> redirect to
r = req.get('<url>')
```

Attribute :

- `url`
- `status_code`
- `headers`
- `cookies`
- `content` : response body (bytes)
- `text` : response body decode by `r.encoding`
- `history` : a list of response object that were created when redirecting.
- `request` : corresponding request object of the response object

Method :
- `json()` : loads body in json format, if body isn’t json format then raise an error


---
## Session Object
```python
import requests as req

s = req.Session()

s.cookies.set('<cookie key>', '<cookie val>', domain='<domain>', path='<path>')
s.headers.update({'<header key>': '<header val>'})

s.get('<url>')
s.post('<url>')
```


---
## Proxy
```python
import requests as req

proxies = {"http": "http://localhost:8080"}
r = req.get('<url>', proxies=proxies)

s = req.Session()
s.proxies.update(proxies)
```
