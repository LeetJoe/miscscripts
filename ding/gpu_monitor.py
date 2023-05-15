# -*- coding: utf-8 -*-


import time
import hmac
import hashlib
import base64
import urllib
import urllib3
from nvitop import Device



def wrap_msg(title, msg):
    body = "{'msgtype': 'markdown','markdown': {'text': '".encode('utf-8') + msg + "', 'title': '".encode('utf-8') + title + "'}}".encode('utf-8')
    return body

api_ding = 'https://oapi.dingtalk.com/robot/send?access_token=e34c34a76c3a4a9b5a5634b5d44adddf75e2848dfee13113fbb35c7fb77958d7'
sign = 'SECf01703886cba07bfa72e04ea9e55f482b7f78528fa7c99803fdbdd89b5e2ba4f'
temp_thresh = 25

devices = Device.all()
too_hot = False
for device in devices:
    processes = device.processes()  # type: Dict[int, GpuProcess]
    sorted_pids = sorted(processes)

    if device.temperature() > temp_thresh:
        too_hot = True
        break
    '''
    print(f'  - Fan speed:       {device.fan_speed()}%')
    print(f'  - Temperature:     {device.temperature()}C')
    print(f'  - GPU utilization: {device.gpu_utilization()}%')
    print(f'  - Total memory:    {device.memory_total_human()}')
    print(f'  - Used memory:     {device.memory_used_human()}')
    print(f'  - Free memory:     {device.memory_free_human()}')
    print(f'  - Processes ({len(processes)}): {sorted_pids}')
    for pid in sorted_pids:
        print(f'    - {processes[pid]}')
    print('-' * 120)
    '''

if too_hot:
    timestamp = str(round(time.time() * 1000))
    string_to_sign = '{}\n{}'.format(timestamp, sign)
    hmac_code = hmac.new(sign.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    sign_final = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    http_api = api_ding + "&timestamp=" + timestamp + "&sign=" + sign_final
    http = urllib3.PoolManager()
    resp = http.request(
        'POST',
        http_api,
        body=wrap_msg(title='服务器通知'.encode('utf-8'), msg='## GPU过热：超过'.encode('utf-8') + str(temp_thresh).encode('utf-8') + '度！'.encode('utf-8')),
        headers={"Content-Type": "application/json"}
    )
