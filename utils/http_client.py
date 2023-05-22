# -*- coding: utf-8 -*-

import urllib3


api = 'http://172.18.34.41:8070'

http = urllib3.PoolManager()
resp = http.request(
    'POST',
    api + '/generate',
    body='',
    headers={"Content-Type": "application/json"}
)


