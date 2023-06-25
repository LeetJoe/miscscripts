from elasticsearch import Elasticsearch

from config import es as esconf

# Single node via URL
es = Elasticsearch(
    esconf['host'],
    basic_auth=(esconf['username'], esconf['password'])
)

'''
# Multiple nodes via URL
es = Elasticsearch([
    "http://localhost:9200",
    "http://localhost:9201",
    "http://localhost:9202"
])

# Single node via dictionary
es = Elasticsearch({"scheme": "http", "host": "localhost", "port": 9200})

# Multiple nodes via dictionary
es = Elasticsearch([
    {"scheme": "http", "host": "localhost", "port": 9200},
    {"scheme": "http", "host": "localhost", "port": 9201},
])

'''

def create_index(client, index_name):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index=index_name,
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "from": {"type": "text"},
                    "relation": {"type": "keyword"},
                    "to": {"type": "text"}
                }
            },
        },
        ignore=400,
    )


import datetime
def index():
    doc = {
        'author': 'author_name',
        'text': 'Interensting content...',
        'timestamp': datetime.now(),
    }
    resp = es.index(index="test-index", id=1, document=doc)
    # print(resp['result'])
    return resp

def getdoc():
    resp = es.get(index="test-index", id=1)
    # print(resp['_source'])
    return resp

def refresh_index():
    es.indices.refresh(index="test-index")

def query_simple():
    resp = es.search(index="test-index", query={"match_all": {}})
    # print("Got %d Hits:" % resp['hits']['total']['value'])
    # for hit in resp['hits']['hits']:
        # print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

    return resp

def update_simple(id, doc):
    resp = es.update(index="test-index", id=id, document=doc)
    return resp

def delete_by_id(id):
    es.delete(index="test-index", id=id)


import csv
from elasticsearch.helpers import streaming_bulk

def bulk_index(client, csv_data_path):
    def generate_actions(f):
        reader = csv.DictReader(f)
        for row in reader:
            doc = {
                "from": row["from"],
                "relation": '惩罚',
                "to": row["to"],
            }
            # print(doc)
            yield doc

    f = open(csv_data_path, mode="r")
    print("Indexing documents...")
    # generate_actions(f)

    successes = 0
    total_num = 0

    for ok, action in streaming_bulk(
        client=client, index="elasicsearch-kg-test", actions=generate_actions(f),
    ):
        print(ok)
        print(action)
        successes += ok
        total_num += 1

    print("Indexed %d/%d documents" % (successes, total_num))

# create_index(es, 'elasicsearch-kg-test')
# bulk_index(es, '/Users/neosong/Work/code/git/ucasai/miscscripts/downloads/edge_chengfa.csv')
