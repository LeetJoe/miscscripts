import requests
import json

from elasticsearch import Elasticsearch
from config import es as esconf


def json_send(url, data=None, extra_headers=None, method="POST"):
    headers = {"Content-type": "application/json",
               "Accept": "text/plain", "charset": "UTF-8"}
    if extra_headers:
        headers.update(extra_headers)

    if method == "POST":
        if data is not None:
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
        else:
            response = requests.post(url=url, headers=headers)
    else:
        response = requests.get(url=url, headers=headers)
    return response.json()

