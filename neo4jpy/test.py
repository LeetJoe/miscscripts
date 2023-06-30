from neo4jrestclient.client import GraphDatabase
from config import db as dbconf


gdb = GraphDatabase(dbconf["api"], username=dbconf["username"], password=dbconf["password"])

# create some nodes with labels
user = gdb.labels.create("User")
u1 = gdb.nodes.create(name="user1")
user.add(u1)
u2 = gdb.nodes.create(name="user2")
user.add(u2)

# associate a label with many nodes in one go
beer = gdb.labels.create("Language")
b1 = gdb.nodes.create(name="C++")
b2 = gdb.nodes.create(name="Python")
beer.add(b1, b2)

# create relationships
u1.relationships.create("likes", b1)
u1.relationships.create("likes", b2)
u2.relationships.create("likes", b1)

# bi-directional relationships
u1.relationships.create("friends", u2)


from neo4jrestclient import client


# match
q = 'MATCH (u:User)-[r:likes]->(m:language) WHERE u.name="Marco" RETURN u, type(r), m'
results = gdb.query(q, returns=(client.Node, str, client.Node))

# print results
for r in results:
    print("(%s)-[%s]->(%s)" % (r[0]["name"], r[1], r[2]["name"]))

