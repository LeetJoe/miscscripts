from elasticsearch import Elasticsearch

# Single node via URL
es = Elasticsearch(
    "http://192.168.1.114:9200",
    basic_auth=("elastic", "8-INTbKDAs8Fsm8dqtBS")
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

