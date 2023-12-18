import requests
import json

from elasticsearch import Elasticsearch
from config import es as esconf


def json_send(url, data=None, method="POST"):
    headers = {"Content-type": "application/json",
               "Accept": "text/plain", "charset": "UTF-8"}
    if method == "POST":
        if data != None:
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
        else:
            response = requests.post(url=url, headers=headers)
    elif method == "GET":
        response = requests.get(url=url, headers=headers)
    return json.loads(response.text)


def json_send_sea(query):
    es = Elasticsearch(
        esconf['host'],
        basic_auth=(esconf['username'], esconf['password'])
    )

    resp = es.search(
        index=esconf['index'],
        size=60,
        query={
            "function_score": {
                "query": {
                    "bool": {
                        "must": {
                            "combined_fields": {
                                "query": query,
                                "fields": ["from", "relation", "to"]
                            }
                        }
                    }
                },
                "min_score": 20
            }
        },
        filter_path=[
            'hits.hits._score',
            'hits.hits._source.from',
            'hits.hits._source.relation',
            'hits.hits._source.to',
        ]
    )

    if not 'hits' in resp.keys():
        return []
    if not 'hits' in resp['hits'].keys():
        return []
    return [hit['_source']['from'] + hit['_source']['relation'] + hit['_source']['to'] for hit in resp['hits']['hits']]


