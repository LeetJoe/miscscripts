from elastic_enterprise_search import AppSearch
from config import appsearch as asconfig


app_search = AppSearch(
    asconfig.host,
    http_auth=asconfig.token
)

# get all engines(by page)
def listEngines():
    return app_search.list_engines()

# get engine info by name
def getEngine(ename: str):
    return app_search.get_engine(engine_name=ename)

# create engine
def createEngine(ename: str, lang = "en"):
    return app_search.create_engine(
        engine_name=ename,
        language=lang,
    )

# delete engine by name
def delEngine(ename: str):
    app_search.delete_engine(engine_name=ename)

# get schema of engine
def getSchema(ename: str):
    return app_search.get_schema(
        engine_name=ename
    )

# update / create schema
def updateSchema(ename: str, schema: dict):
    return app_search.put_schema(
        engine_name=ename,
        schema=schema
    )

# add documents and index it to engine
def indexDoc(ename: str, docs: list):
    return app_search.index_documents(
        engine_name=ename,
        documents=docs
    )

# list documents (by page)
def listDoc(ename: str):
    return app_search.list_documents(engine_name=ename)

# get documents by ids
def getDocByIds(ename: str, ids: list):
    return app_search.get_documents(
        engine_name=ename,
        document_ids=ids
    )

# udpate document by ids
def udpateDocByIds(ename: str, docsWithId: list):
    app_search.put_documents(
        engine_name=ename,
        documents=docsWithId
    )

# delete documents by ids
def deleteDocByIds(ename: str, ids: list):
    return app_search.delete_documents(
        engine_name=ename,
        document_ids=ids
    )

# single search, multi search, create curation and so on, meta engines and so on see:
# https://www.elastic.co/guide/en/enterprise-search-clients/python/8.7/app-search-api.html#_create_and_index_documents

