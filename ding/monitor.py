# -*- coding: utf-8 -*-

import os
import time
import hmac
import hashlib
import base64
import urllib
import urllib3
from config import api_ding, sign


def wrap_msg(title, msg):
    body = "{'msgtype': 'markdown','markdown': {'text': '".encode('utf-8') + msg + "', 'title': '".encode('utf-8') + title + "'}}".encode('utf-8')
    return body

stdout = os.popen("ps aux | grep python | grep train_sft | grep -v grep")
running = stdout.read() != ''

if running == False or True:
    timestamp = str(round(time.time() * 1000))
    string_to_sign = '{}\n{}'.format(timestamp, sign)
    hmac_code = hmac.new(sign.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    sign_final = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    http_api = api_ding + "&timestamp=" + timestamp + "&sign=" + sign_final
    http = urllib3.PoolManager()
    resp = http.request(
        'POST',
        http_api,
        body=wrap_msg(title='服务器通知'.encode('utf-8'), msg='## 训练已完成。'.encode('utf-8')),
        headers={"Content-Type": "application/json"}
    )
