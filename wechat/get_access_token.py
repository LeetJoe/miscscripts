# -*- coding: utf-8 -*-

import os
import time
import hmac
import hashlib
import base64
import urllib
import urllib3
import json

from config import appid, secret

file_name = 'accesstoken.tmp'
expire_time = 7200

api_wechat = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret


def get_new():
    http = urllib3.PoolManager()
    resp = http.request(
        'GET',
        api_wechat,
        headers={"Content-Type": "application/json"}
    )
    data = json.loads(resp.data.decode('utf-8'))
    if data.__contains__('access_token'):
        with open(file_name, 'w') as file:
            file.write(data['access_token'])
        return data['access_token']
    else:
        return ''


def get():
    if (os.path.exists(file_name)):
        mtime = os.path.getmtime(file_name)
        if mtime + expire_time - 1 > time.time():    # 没过期
            with open(file_name, 'r') as exfile:
                access_token = exfile.readline()
                if access_token.strip() == '':
                    access_token = get_new()
        else:    # 过期了
            access_token = get_new()
    else:
        print('file not exists')
        access_token = get_new()
    return access_token
