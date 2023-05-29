# -*- coding: utf-8 -*-

import urllib3

from config import api as apiconf

api = apiconf.host

http = urllib3.PoolManager()
resp = http.request(
    'POST',
    api + '/generate',
    body='',
    headers={"Content-Type": "application/json"}
)


