import csv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from config import es as esconf



def create_index(client):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index='analyzer_test_index_standard',
        settings={
            "number_of_shards": 1
        },
        mappings={
            "properties": {
                "from": {
                    "type": "text"
                },
                "relation": {
                    "type": "text"
                },
                "to": {
                    "type": "text"
                }
            }
        },
        # ignore is a global param, it means if the response is a 400 or 404 error status.
        ignore=[400,404]
    )

    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index='analyzer_test_index_ik_smart',
        mappings={
            "properties": {
                "from": {
                    "type": "text"
                },
                "relation": {
                    "type": "text"
                },
                "to": {
                    "type": "text"
                }
             }
        },
        settings={
            "number_of_shards": 1,
            "analysis": {
                "analyzer": {
                    "default": {
                        "type": "ik_smart"
                    }
                }
            }
        },
        # ignore is a global param, it means if the response is a 400 or 404 error status.
        ignore=[400,404]
    )

    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index='analyzer_test_index_ik_max_word',
        mappings={
            "properties": {
                "from": {
                    "type": "text"
                },
                "relation": {
                    "type": "text"
                },
                "to": {
                    "type": "text"
                }
            }
        },
        settings={
            "number_of_shards": 1,
            "analysis": {
                "analyzer": {
                    "default": {
                        "type": "ik_max_word"
                    }
                }
            }
        },
        # ignore is a global param, it means if the response is a 400 or 404 error status.
        ignore=[400,404]
    )

def bulk_index(client, index, csv_data_path, relation):
    def generate_actions(f):
        reader = csv.DictReader(f)
        for row in reader:
            doc = {
                "from": row["from"],
                # "key_from": row["from"],
                "relation": relation,
                # "key_relation": relation,
                "to": row["to"],
                # "key_to": row["to"],
            }
            # print(doc)
            yield doc

    f = open(csv_data_path, mode="r")
    print("Indexing %s ..." % csv_data_path)

    successes = 0
    total_num = 0

    for ok, action in streaming_bulk(
        client=client, index=index, actions=generate_actions(f),
    ):
        successes += ok
        total_num += 1

    print("Indexed %d/%d documents" % (successes, total_num))


def search_prompt(es, index, query):
    resp = es.search(
        index=index,
        size=60,
        query=query,
        filter_path=[
            'hits.hits._id',
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
    return [{"id": hit["_id"], "score": hit["_score"], "text": hit['_source']['from'] + hit['_source']['relation'] + hit['_source']['to']} for hit in resp['hits']['hits']]


def explain_search(id, index, query):
    resp = es.explain(
        id=id,
        index=index,
        query=query
    )

    return resp


def init_data(es):
    edgelist = [
        {"relation": "的惩罚范围是", "file": "edge_chengfa.csv"},
        {"relation": "的出台机关是", "file": "edge_chutai.csv"},
        {"relation": "提到的的规范内容是", "file": "edge_guifan.csv"},
        {"relation": "提到的鼓励内容是", "file": "edge_guli.csv"},
        {"relation": "提到的减免内容是", "file": "edge_jianmian.csv"},
        {"relation": "提到的禁令内容是", "file": "edge_jinzhi.csv"},
        {"relation": "颁布的目的是", "file": "edge_mudi.csv"},
        {"relation": "涉及的法律是", "file": "edge_sheji.csv"},
        {"relation": "的实践范围是", "file": "edge_shijian.csv"},
        {"relation": "的适用范围是", "file": "edge_shiyong.csv"},
        {"relation": "的受理流程是", "file": "edge_shouli.csv"},
        {"relation": "的约束条件是", "file": "edge_tiaojian.csv"},
        {"relation": "的主题是", "file": "edge_title.csv"},
        {"relation": "的要求对象是", "file": "edge_yaoqiu.csv"},
        {"relation": "的依据是", "file": "edge_yiju.csv"},
        {"relation": "的触发条件是", "file": "edge_yuanyin.csv"},
        {"relation": "赋予的执行权力是", "file": "edge_zhixing.csv"},
    ]

    for item in edgelist:
        print("\n\nanalyzer_test_index_standard")
        bulk_index(client=es, index="analyzer_test_index_standard", csv_data_path='../downloads/' + item['file'],
                   relation=item['relation'])
        print("\n\nanalyzer_test_index_ik_smart")
        bulk_index(client=es, index="analyzer_test_index_ik_smart", csv_data_path='../downloads/' + item['file'],
                   relation=item['relation'])
        print("\n\nanalyzer_test_index_ik_max_word")
        bulk_index(client=es, index="analyzer_test_index_ik_max_word", csv_data_path='../downloads/' + item['file'],
                   relation=item['relation'])


# Single node via URL
es = Elasticsearch(esconf['host']).options(basic_auth=(esconf['username'], esconf['password']))

# create_index(es)
# init_data(es)


prompt="防治海洋工程建设项目污染损害海洋环境管理条例第二十二条提到的禁止内容什么？"

query={
    "function_score": {
        "query": {
            "bool": {
                "must": {
                    "combined_fields": {
                        "query": prompt,
                        "fields": ["relation^10", "from", "to"]
                    }
                },
                "should": [
                    {
                        "match": {
                            "relation": prompt
                        }
                    }
                ]
            }
        },
        "min_score": 20
    }
}


# analyzer_test_index_standard
# analyzer_test_index_ik_smart
# analyzer_test_index_ik_max_word
index = "analyzer_test_index_ik_max_word"



# jOjxAIkBVfXQnJDtMYOv
# 0ujxAIkBVfXQnJDtL396


for item in search_prompt(es, index, query):
    print(item['id'], item['score'])
    print(item['text'])

