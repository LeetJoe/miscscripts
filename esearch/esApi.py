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
        # ignore is a global param, it means if the response is a 400 or 404 error status.
        ignore=[400,404]
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



def search():
    resp = es.search(index='elasicsearch-kg-test', size=2, filter_path=['hits.hits._*'])
    return resp



# print(es.search(index='elasicsearch-kg-test', size=2, query={'term': {'from': {'value': '中国海域管理法'}}}))



# print(es.search(index='elasicsearch-kg-test', size=20, query={'match': {'from': {'query': '关于进一步规范裁量权行使的若干意见'}}}, filter_path=['hits.hits._score', 'hits.hits._source.from']))


# resp = es.search(index='elasicsearch-kg-test', size=20, query={'match': {'from': {'query': '关于进一步规范裁量权行使的若干意见'}}}, filter_path=['hits.hits._score', 'hits.hits._source.from', 'hits.hits._source.relation', 'hits.hits._source.to'])



def search_prompt(prompt):
    resp = es.search(
        index='elasicsearch-kg-test',
        size=20,
        query={
            "function_score": {
                "query": {
                    "bool": {
                        "must": {
                            "match": {
                                "from": {
                                    "query": prompt
                                }
                            }
                        }
                    }
                },
                "min_score": 8
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



print(search_prompt('关于进一步规范裁量权行使的若干意见第三十五条,接负责的主管人员和其他直接, 然后加进去很多无关的内容，这些都是一些废话，用来干扰的，其实没什么用。随便说都行。'))





# see: https://www.elastic.co/guide/en/elasticsearch/reference/8.8/search-search.html
def search_sample():
    resp = es.search(
        index='index1, index2',  # 支持多个index查询, if '' is passed to it, all indices will be searched.
        allow_no_indices=True, # if wildcard index pattern match nothing, return empty or use all indices
        allow_partial_search_results=True, # if partial search failure or timeout, indicate an error or not
        analyze_wildcard=False, # Specify whether wildcard and prefix queries should be analyzed (default: false)
        analyzer=None, # The analyzer to use for the query string, todo: check it
        batched_reduce_size=10, # The number of shard results that should be reduced at once on the coordinating node.
        ccs_minimize_roundtrips=True, # Indicates whether network round-trips should be minimized as part of
                                      # cross-cluster search requests execution
        default_operator=None, #  The default operator for query string query (AND or OR) todo: check it
        df='', # The field to use as default where no field prefix is given in the query string
        docvalue_fields=[], # Array of wildcard (*) patterns. The request returns doc values for field
                            # names matching these patterns in the hits.fields property of the response.
        expand_wildcards='open', # Whether to expand wildcard expression to concrete indices that are open, closed or both.
        explain=True, # If true, returns detailed information about score computation as part of a hit.
        ext={}, # Configuration of search extensions defined by Elasticsearch plugins.
        fields=[], # Array of wildcard (*) patterns. The request returns values for field names matching these
                   # patterns in the hits.fields property of the response.
        from_=0, # Starting document offset. By default, you cannot page through more than 10,000 hits
                 # using the from and size parameters. To page through more hits, use the search_after parameter.
        ignore_throttled=True, # Whether specified concrete, expanded or aliased indices should be ignored when throttled
        ignore_unavailable=True, # Whether specified concrete indices should be ignored when unavailable (missing or closed)
        indices_boost=[], # Boosts the _score of documents from specified indices.
        knn=query_simple(), # Defines the approximate kNN search to run.
        lenient=True, # Specify whether format-based query failures (such as providing text to a numeric field) should be ignored
        max_concurrent_shard_requests=2, # The number of concurrent shard requests per node this search executes concurrently.
                                         # This value should be used to limit the impact of the search on the cluster
                                         # in order to limit the number of concurrent shard requests
        min_compatible_shard_node='', # The minimum compatible version that all shards involved in search should have for this request to be successful
        min_score=0.6, # Minimum _score for matching documents. Documents with a lower _score are not included in the search results.
        pit={}, # Limits the search to a point in time (PIT). If you provide a PIT, you cannot specify an <index> in the request path.
        pre_filter_shard_size=1, # A threshold that enforces a pre-filter roundtrip to prefilter search shards based
                                 # on query rewriting if the number of shards the search request expands to exceeds the threshold.
        preference='random', # Specify the node or shard the operation should be performed on (default: random)
        q='', # Query in the Lucene query string syntax
        query={}, # Defines the search definition using the Query DSL.
        rank=1, # Defines the Reciprocal Rank Fusion (RRF) to use
        request_cache=False, # Specify if request cache should be used for this request or not, defaults to index level setting
        rest_total_hits_as_int=True, # Indicates whether hits.total should be rendered as an integer or an object in the rest search response
        routing='a, b, c', # A comma-separated list of specific routing values
        runtime_mappings=[], # Defines one or more runtime fields in the search request. These fields take precedence over mapped fields with the same name.
        script_fields=[], # Retrieve a script evaluation (based on different fields) for each hit.
        scroll=10, # Specify how long a consistent view of the index should be maintained for scrolled search
        search_type='', # Search operation type
        seq_no_primary_term=True, # If true, returns sequence number and primary term of the last modification of each hit.
                                  # See Optimistic concurrency control.
        size=10, # The number of hits to return. By default, you cannot page through more than 10,000 hits
                 # using the from and size parameters. To page through more hits, use the search_after parameter.
        source='', # Indicates which source fields are returned for matching documents. These fields are returned in
                   # the hits._source property of the search response.
        source_excludes=[], # A list of fields to exclude from the returned _source field
        source_includes=[], # A list of fields to extract and return from the _source field
        stats='', # Stats groups to associate with the search. Each group maintains a statistics aggregation for its
                  # associated searches. You can retrieve these stats using the indices stats API.
        stored_fields=['a', 'b'], # List of stored fields to return as part of a hit. If no fields are specified,
                                  # no stored fields are included in the response. If this field is specified,
                                  # the _source parameter defaults to false. You can pass _source: true to return
                                  # both source fields and stored fields in the search response.
        suggest_field=[], # Specifies which field to use for suggestions.
        suggest_mode='', # Specify suggest mode
        suggest_size=10, # How many suggestions to return in response
        suggest_text='', # The source text for which the suggestions should be returned.
        terminate_after='', # Maximum number of documents to collect for each shard. If a query reaches this limit,
                            # Elasticsearch terminates the query early. Elasticsearch collects documents before sorting.
                            # Defaults to 0, which does not terminate query execution early.
        timeout=10, # Specifies the period of time to wait for a response from each shard. If no response is received
                    # before the timeout expires, the request fails and returns an error. Defaults to no timeout.
        track_scores=True, # If true, calculate and return document scores, even if the scores are not used for sorting.
        track_total_hits=True, # Number of hits matching the query to count accurately. If true, the exact number of
                               # hits is returned at the cost of some performance. If false, the response does not
                               # include the total number of hits matching the query. Defaults to 10,000 hits.
        typed_keys=True, # Specify whether aggregation and suggester names should be prefixed by their respective types in the response
        version=True, # If true, returns document version as part of a hit.

        post_filter={}, # ?
        highlight=None, # ?
        aggregations=None,  # ?
        aggs=None, # ?
        collapse=None, # ?
        profile=query_simple(), # ?
        rescore=False, # ?
        search_after=0, # ?
        slice=True, # ?
        sort=True, # ?
        suggest='', # ?

    )

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
