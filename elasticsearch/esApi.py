from elasticsearch import Elasticsearch

from config import es as esconf

# Single node via URL
es = Elasticsearch(
    esconf.host,
    basic_auth=(esconf.username, esconf.password)
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

