# Python Proxy Utils

A set of python 3 utils to help with web scraping. Currently only a free
proxy utility is implemented. It can be used as a proxy rotator or however
you like.

## Install

```bash
pip install python-proxy-utils
```

## ProxyHelper Example Usage

When the class is initialised it scrapes a list of free proxies from a
number of free proxy list websites concurrently using aiohttp.


```python
>>> from proxy_utils import ProxyHelper
>>> p = ProxyHelper()
>>> p.get_count()
13224
>>> p.get_random()
'http://103.9.188.143:56368'
>>>
>>> import requests
>>> random_proxy = p.get_random()
>>> proxies = {'http': random_proxy, 'https': random_proxy}
>>> r = requests.get('http://example.com', proxies=proxies)
```

### Free Proxy Lists Used

This class currently uses the below free lists. At the time of writing
this these lists usually produced around 13,000 proxies.

- proxy-list.download
- free-proxy-list.net

## Todo
- Testing
- Add ProxyHelper method that returns the proxies in the format requests wants it in
- Add more free proxy lists
- Add a clean method to the proxy helper to remove bad proxies
- Add a UserAgentHelper

## Author
Jeremy Storer <storerjeremy@gmail.com>
