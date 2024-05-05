# Beautiful Soup

## Usage
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'html.parser')

# return str, a prettier version of html_doc
soup.prettify()

# return list, contain bs4's element objects of all a tag
soup.find_all('a')

# return list, contain bs4's element objects of all a tag with href='/link'
soup.find_all('a', href='/link')

# return list, contain bs4's element objects of all a tag that attribute href match '^/link' regular expression
soup.find_all('a', href=re.compile('^/link'))

# return list, contain bs4's element objects of all a tag in class btn
soup.find_all('a', class_='btn')

# return list, contain bs4's element objects of all a tag that content of a tag match '^Link' regular expression
soup.find_all('a', string=re.compile('^Link'))

# return list, contain bs4's element objects of all elements match a.btn css selector
soup.select('a.btn')

# return bs4's element objects of first a tag
soup.find('a')

# return bs4's element objects of id='form-btn'
soup.find(id='form-btn')

# return str, whole content of first a tag
str(soup.find('a'))

# return str, first a tag's content
str(soup.find('a').string)
```