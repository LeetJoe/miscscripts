import csv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from config import es as esconf

es_index = 'nmdis_test_sst'


def create_index(client):
    """Creates an index in Elasticsearch if one isn't already there."""
    return client.indices.create(
        index=es_index,
        settings={
            "number_of_shards": 1
        },
        #  timeh,latit,longt,slp,at,rh,sst
        mappings={
            "properties": {
                "dtime": {
                    "type": "date",
                    "format": "yyyyMMddHH||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                },
                "location": {
                    "type": "geo_point"
                },
                "slp": {
                    "type": "scaled_float",
                    "scaling_factor": 10
                },
                "at": {
                    "type": "scaled_float",
                    "scaling_factor": 10
                },
                "rh": {
                    "type": "short"
                },
                "sst": {
                    "type": "scaled_float",
                    "scaling_factor": 10
                }
            }
        },
        # ignore is a global param, it means if the response is a 400 or 404 error status.
        ignore=[400,404]
    )


def bulk_index(client, csv_data_path):
    def generate_actions(f):
        reader = csv.DictReader(f)
        for row in reader:
            doc = {
                "dtime": row['timeh'],
                "location": {
                    "lon": int(row['longt'])/60,
                    "lat": int(row['latit'])/60
                },
                "slp": row['slp'],
                "at": row['at'],
                "rh": row['rh'],
                "sst": row['sst']
            }
            # print(doc)
            yield doc

    f = open(csv_data_path, mode="r")
    print("Indexing %s ..." % csv_data_path)

    successes = 0
    total_num = 0

    for ok, action in streaming_bulk(
        client=client, index=es_index, actions=generate_actions(f),
    ):
        successes += ok
        total_num += 1

    print("Indexed %d/%d documents" % (successes, total_num))


def geo_search(es, query):
    resp = es.search (
        index=es_index,
        size=60,
        query=query,
        # filter_path=[]
    )

    if not 'hits' in resp.keys():
        return []
    if not 'hits' in resp['hits'].keys():
        return []
    return [{"id": hit["_id"], "date": hit['_source']['dtime'],
            "location": [round(hit['_source']['location']['lon'], 2), round(hit['_source']['location']['lat'], 2)],
            "at": hit['_source']['at'], "rh": hit['_source']['rh'], "sst": hit['_source']['sst']}
            for hit in resp['hits']['hits']
        ]

query_bbox = {
    "bool": {
        "must": [
            {
                "range": {
                    "at": {
                        "gte": 32,
                        "lte": 33
                    }
                }
            },
            {
                "range": {
                    "rh": {
                        "gte": 85
                    }
                }
            },
            {
                "match": {
                    "sst": 30.0
                }
            }
        ],
        "filter": {
            "geo_bounding_box": {
                "location": {  # 字段名
                    "top_left": {
                        "lat": 21,
                        "lon": 113
                    },
                    "bottom_right": {
                        "lat": 19,
                        "lon": 115
                    }
                }
            }
        }
    }
}

query_distance = {
    "bool": {
        "must": {
            "match_all": {}
        },
        "filter": {
            "geo_distance": {
                "distance": "200km",
                "location": {  # 字段名
                    "lat": 21,
                    "lon": 113
                }
            }
        }
    }
}



# Single node via URL
es = Elasticsearch(esconf['host']).options(basic_auth=(esconf['username'], esconf['password']))

# print(create_index(es))

# bulk_index(es, '../downloads/NMDIS/S1400-Y2019-SSM_sst.CSV')

print(geo_search(es, query_distance))

es.close()
