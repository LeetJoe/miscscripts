
es = {
    'host' : 'http://127.0.0.1:9200',
    'username': 'elastic',
    'password': '123456',
    'index': 'elasicsearch-kg-test'
}

appsearch = {
    'host': 'http://127.0.0.1:3002',
    'token': 'private-xxxxxx'
}

pg = {
    'host': '127.0.0.1',
    'port': 5432,
    'user': 'postgre',
    'passwd': '123456',
    'db': 'dbname'
}

neo4j = {
    'host': 'https://demo.neo4jlabs.com',
    'port': 7473,
    'user': 'recommendations',
    'passwd': 'recommendations',
    'db': 'recommendations'
}

tokens = {
    'replicate': 'r8_4KZOwXOssvQKUCwMegkXXEA52YWTGKH42738I'
}

LLM_ego = {
    'cn': "你是一个 Neo4j Cypher 专家，你可以把一个问题转换成 Cypher 格式。请使用给出的图数据库的 schema，将 User 的问题转换为 Cypher 格式。只输出 Cypher 部分，其它内容不要输出。",
    'en': "You are a Neo4j Cypher expert and you can tranform the question of user into Cypher format. Please use the given schema and complete the transformation of user's question. Only the Cypher sentences should be printed.",
}
