# -*- coding: utf-8 -*-

import os
import sys
import time
import urllib3
import socket
import json
import get_access_token


def wrap_msg(user_open_id, template_id, hostname, message, user, datetime):
    body = '{"touser": "'.encode('utf-8') + \
           user_open_id.encode('utf-8') + \
           '","template_id": "'.encode('utf-8') + \
           template_id.encode('utf-8') + \
           '","topcolor": "#FF0000","data": {"thing01": {"value": "'.encode('utf-8') + \
           hostname.encode('utf-8') + \
           '","color": "#173177"},"thing02": {"value":"'.encode('utf-8') + \
           message.encode('utf-8') + \
           '","color": "#173177"},"thing03": {"value":"'.encode('utf-8') + \
           user.encode('utf-8') + \
           '","color": "#173177"},"time01": {"value":"'.encode('utf-8') + \
           datetime.encode('utf-8') + \
           '","color": "#173177"}}}'.encode('utf-8')
    return body

if len(sys.argv) < 2:
    print('Pass a parameter as the message.')
    exit(1)

user_open_id = 'odJxP5h3Ao9wgrELxb8VDlYzdmeM'
template_id = 'uStrBBrOH-j03t9BFDqW2-QdhNvRUJkiEUKgzyVQ0i4'
access_token = get_access_token.get()
api_wechat = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token

http = urllib3.PoolManager()

stdout = os.popen("ps aux | grep python | grep train_sft | grep -v grep")
running = stdout.read() != ''

body=wrap_msg(user_open_id=user_open_id, template_id=template_id,
                      hostname=socket.gethostname(), message=sys.argv[1],
                      user=os.getlogin(), datetime=time.ctime(time.time()))

if running == False or True:
    http = urllib3.PoolManager()
    resp = http.request(
        'POST',
        api_wechat,
        body=wrap_msg(user_open_id=user_open_id, template_id=template_id,
                      hostname=socket.gethostname(), message=sys.argv[1],
                      user=os.getlogin(), datetime=time.ctime(time.time())),
        headers={"Content-Type": "application/json", "encoding": "UTF-8"}
    )
    print(resp.data)
