import _csv

from elasticsearch import Elasticsearch
import csvtemp
import csv
import os

index_name = 'neosong-test-engine-csv'

es = Elasticsearch(
    "http://192.168.1.114:9200",
    basic_auth=("elastic", "8-INTbKDAs8Fsm8dqtBS")
)

filepath = '/mnt/data1/neosong/data/obis/split/split_obis'

columnarr = []

while True:
    has_exception = False
    for i in range(0, 100) :
        cur_file = filepath + str(i).zfill(2)
        with open(cur_file, encoding="utf-8-sig", mode="r") as f:
            try:
                reader = csv.DictReader(f)
                print('neosong log: current file is ' + cur_file)
                linenum = 1
                for row in reader:
                    linenum += 1
                    id = row.pop('id')
                    print(id)
                    resp = es.index(index=index_name, id=id, document=row)
                    print(resp)
                    exit(0)
                    # print(row)
            except _csv.Error as e:
                # has_exception = True
                print(e)
                # print(id)
                # print(linenum + 1)
                # extractline = "sed -n '" + str(linenum + 1) + "p' " + cur_file + " >> /mnt/data1/neosong/data/obis/split/special.tmp"
                # print(extractline)
                # os.system(extractline)
                # delline = "sed -i '" + str(linenum + 1) + "d' " + cur_file
                # print(delline)
                # os.system(delline)
    if not has_exception:
        break

print("finished")
