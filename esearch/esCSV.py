import _csv

from elasticsearch import Elasticsearch
import csvmappings
import csv

from config import es as esconf


def test():
    # 在
    index_name = 'search-test-csv'

    es = Elasticsearch(
        esconf.host,
        basic_auth=(esconf.username, esconf.password)
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


# 预处理输入到es中的三元组csv文件数据
def prefrocess(path_to_file):
    # 将""替换为“”
    # 在文件开头增加一行：from,to，可以使用 sed -i "1 ifrom,to" *.csv 来完成。
    return path_to_file
