import os
import time
import hmac
import hashlib
import base64
import urllib
import urllib3


def wrap_msg(title, msg):
    body = "{'msgtype': 'markdown','markdown': {'text': '".encode('utf-8') + msg.encode('utf-8') + "', 'title': '".encode('utf-8') + title.encode('utf-8') + "'}}".encode('utf-8')
    return body

api_ding = 'https://oapi.dingtalk.com/robot/send?access_token=e34c34a76c3a4a9b5a5634b5d44adddf75e2848dfee13113fbb35c7fb77958d7'
sign = 'SECf01703886cba07bfa72e04ea9e55f482b7f78528fa7c99803fdbdd89b5e2ba4f'

stdout = os.popen("ps aux | grep python | grep train_sft | grep -v grep")
running = stdout.read() != ''

if running == False:
    timestamp = str(round(time.time() * 1000))
    string_to_sign = '{}\n{}'.format(timestamp, sign)
    hmac_code = hmac.new(sign.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    sign_final = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    http_api = api_ding + "&timestamp=" + timestamp + "&sign=" + sign_final
    http = urllib3.PoolManager()
    resp = http.request(
        'POST',
        http_api,
        body=wrap_msg(title='服务器通知', msg='## 训练已完成。'),
        headers={"Content-Type": "application/json"}
    )
