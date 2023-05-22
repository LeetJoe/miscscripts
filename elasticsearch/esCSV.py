import _csv

from elasticsearch import Elasticsearch
import csvmappings
import csv


# 在
index_name = 'search-test-csv'

es = Elasticsearch(
    "http://192.168.1.114:9200",
    basic_auth=("elastic", "8-INTbKDAs8Fsm8dqtBS")
)

filepath = '/mnt/data1/neosong/data/obis/split/split_obis'

columnarr = []

for i in range(0, 1) :
    cur_file = filepath + str(i).zfill(2)
    with open(cur_file, encoding="utf-8-sig", mode="r") as f:
        reader = csv.DictReader(f)
        print('neosong log: current file is ' + cur_file)
        linenum = 1
        for row in reader:
            linenum += 1
            id = row.pop('id')
        try:
            resp = es.index(index=index_name, id=id, document=row)
            # print(resp)
        except _csv.Error as e:
            print(id)
            print(e)

print("finished")
