import os

import requests
import argparse


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='ding message.',
        usage='dingmsg.py [<args>] [-h | --help]'
    )

    parser.add_argument('--text', type=str, help='text message')
    parser.add_argument('--file', type=str, help='file to send its content')

    return parser.parse_args(args)

def send_dingtalk_message(webhook_url, msg):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    response = requests.post(webhook_url, json=data, headers=headers)
    return response.json()


# 使用示例
args = parse_args()
webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=0c64dfd5a298962650301d3edeb3b536c9ebcee7a336d137a93ad52a8c9d4512'

message = 'casia server message:\n\n'
if args.text is not None:
    message += args.text
elif args.file is not None and os.path.exists(args.file):
    with open(args.file, 'r') as f:
        message += f.read()
else:
    message = ''

if message != '':
    result = send_dingtalk_message(webhook_url, message)
    print(result)
