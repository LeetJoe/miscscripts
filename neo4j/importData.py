from neo4j import GraphDatabase

from config import db

import csv
import re


csv_file = '../downloads/neo4j/Disease_checked.csv'

# 使用 session 开启事务，以事务运行
def tx_create_rows(driver, dbname, items):
    with driver.session(dbname) as session:
        for item in items:
            session.execute_write(batch_tx, item)


# 事务方法
def batch_tx(tx, node_names, label):
    result = tx.run(f"CREATE (a:{label}) "
                    "SET a.name = $message "
                    "RETURN a.message + ', from node ' + id(a)", message=label)
    return result.single()[0]


# 创建疾病节点
def create_disease_query(driver, data):
    response = driver.execute_query(
        """
        MERGE (:疾病 {名称: $name, 简介: $intro, 病因: $cause, 预防方式: $precaution, 注意事项: $tips, 医保疾病: $assurance, 
        患病比例: $ratio, 治疗费用: $fee, 治愈率: $cure_ratio, 治疗概述: $treatment_intro, 易感人群: $susceptibility, 
        治疗周期: $period, 并发症: $complication})
        """
        ,
        name=data['name'],
        intro=data['intro'],
        cause=data['cause'],
        precaution=data['precaution'],
        tips=data['tips'],
        assurance=data['assurance'],
        ratio=data['ratio'],
        fee=data['fee'],
        cure_ratio=data['cure_ratio'],
        treatment_intro=data['treatment_intro'],
        susceptibility=data['susceptibility'],
        period=data['period'],
        complication=data['complication'],
    )
    return response


def create_node_query(driver, label, name):
    response = driver.execute_query("MERGE (:" + label + " {名称: $name})", name=name)
    return response


# 创建有向关系 (:label1{名称:name1})-[:$relation]->(:label2{名称:name2})
def create_dircted_relation_query(driver, node_label1, node_label2, node_name1, node_name2, relation):
    query = ("MATCH (a:" + node_label1 + "), (b:" + node_label2 + ") WHERE a.名称 = $node_name1" +
             " AND b.名称 = $node_name2 MERGE (a)-[r:" + relation + "]->(b)" + " RETURN type(r)")
    response = driver.execute_query(
        query,
        node_name1=node_name1,
        node_name2=node_name2
    )
    return response


# 将 “名称（标签）” 里的“名称”和“标签”
def extract_label(str, left='[', right=']'):
    i_start = str.find(left)
    i_end = str.rfind(right)
    if i_start > -1 and i_end > -1:
        label = str[i_start+1:i_end]
        head = str[:i_start]
    else:
        label = ''
        head = str
    return label, head


# 提取所有疾病名称
def extract_relations():
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    merge_list = {}
    num_all = 0
    for row in reader:
        num_all += 1
        if row['relation']:
            merge_list[row['relation']] = 1

    print(f"total rows: {num_all}, relations: {len(merge_list)}")
    return merge_list


# 提取所有的疾病名称
def extract_disease_names():
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    disease_dict = {}
    # symptom_dict = {}
    num_all = 0
    num_disease = 0
    # num_symptom = 0
    for row in reader:
        num_all += 1
        label, node_name = extract_label(row['head'])
        if label == '疾病':
            num_disease += 1
            disease_dict[node_name] = 1
        '''
        # 检查 疾病 + 症状 对所有 head 是否完备：是
        elif label == '症状':
            num_symptom += 1
            symptom_dict[label] = 1
    
    # 检查所有疾病对“可能疾病”关系中的疾病是否完备: 是
    for row in reader:
        if row['relation'] == '可能疾病':
            if not row['tail'] in disease_dict:
                print(row['tail'])
    '''

    print(f"total rows: {num_all}, disease: {num_disease}")
    # print(f"symptom: {num_symptom}, others: {num_all-num_disease-num_symptom}")
    return disease_dict.keys()   #, symptom_dict.keys()


# 提取所有的症状名称
def extract_symptom_names():
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    # head_symptom_dict = {}
    symptom_dict = {}
    num_all = 0
    num_symptom = 0
    for row in reader:
        num_all += 1
        if row['relation'] == '症状':
            num_symptom += 1
            symptom_dict[row['tail']] = 1

    '''
        # 提取 head 里的症状，用于检查“症状”关系里症状对 head 里的“症状”是否完备：是
        label, node_name = extract_label(row['head'])
        if label == '症状':
            head_symptom_dict[node_name] = 1

    for k in head_symptom_dict:
        if k not in symptom_dict:
            print(k)
    '''

    print(f"total rows: {num_all}, symptoms: {num_symptom}")
    return symptom_dict.keys()


# 提取所有科室分类, 返回内容结构为 {'一级科室分类': {'二级科室分类': {'三级科室分类': 1}}}
def extract_department_names():
    department_dict = {}
    num_all = 0
    num_department = [0, 0, 0]

    # 防止因顺序问题导致 head 未初始化，循环两次
    for row in csv.DictReader(open(csv_file, mode="r")):
        num_all += 1
        if not row['head'] in department_dict:
            department_dict[row['head']] = ['', '', '']  # 按 head 组织为一级、二级、三级分类的列表

    for row in csv.DictReader(open(csv_file, mode="r")):
        if row['relation'] == '一级科室分类':
            num_department[0] += 1
            department_dict[row['head']][0] = row['tail']
        elif row['relation'] == '二级科室分类':
            num_department[1] += 1
            department_dict[row['head']][1] = row['tail']
        elif row['relation'] == '三级科室分类':
            num_department[2] += 1
            department_dict[row['head']][2] = row['tail']

    '''
    # 检查“就诊科室”中的分类是否从属于一/二/三级科室分类：是
    for row in reader:
        if row['relation'] == '就诊科室':
            jzks = row['tail'].split(' ')
            for i in jzks:
                if jzks[i] == '':
                    continue
                if not (jzks[i] in department_dict[0] or jzks[i] in department_dict[1] or jzks[i] in department_dict[2]):
                    print(jzks[i])
    '''

    print(f"total rows: {num_all}, department 1,2,3: {num_department[0]},{num_department[1]},{num_department[2]}")

    result_dict = {}
    for k in department_dict:
        item = department_dict[k]
        if item[0] == '':
            continue
        if not item[0] in result_dict:
            result_dict[item[0]] = {}

        if not item[1] in result_dict[item[0]]:
            result_dict[item[0]][item[1]] = {}

        result_dict[item[0]][item[1]][item[2]] = 1

    return result_dict


# 提取所有的传染方式
def extract_infection_names():
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    infection_dict = {}
    num_all = 0
    num = 0
    for row in reader:
        num_all += 1
        if row['relation'] == '传染方式':
            num += 1
            inf_list = re.split('[ ]', row['tail'])
            for inf in inf_list:
                if inf != '':
                    infection_dict[inf] = 1

    print(f"total rows: {num_all}, infections: {num}")
    return infection_dict.keys()


# 提取所有的治疗方式
def extract_treatment_names():
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    treatment_dict = {}
    num_all = 0
    num = 0
    for row in reader:
        num_all += 1
        if row['relation'] == '治疗方式':
            num += 1
            # inf_list = row['tail'].split()
            inf_list = re.split('[，、 ]', row['tail'])
            for inf in inf_list:
                if inf != '':
                    inf = inf.strip('，。 、')
                    treatment_dict[inf] = 1

    print(f"total rows: {num_all}, treatments: {num}")
    return treatment_dict.keys()


# 提取所有的"常用药品"，不带生产厂家名称的药物名称
def extract_medicine_names():
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    medicine_dict = {}
    num_all = 0
    num = 0
    for row in reader:
        num_all += 1
        if row['relation'] == '常用药品':
            num += 1
            inf_list = row['tail'].split()
            for inf in inf_list:
                if inf != '':
                    medicine_dict[inf] = 1

    print(f"total rows: {num_all}, medicine: {num}")
    return medicine_dict.keys()


# 提取所有的"推荐药品"，tail 格式为： 带生产厂家的具体药物产品名称（药物名称）
def extract_mediduct_names():
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    mediduct_dict = {}
    medicine_dict = {}
    num_all = 0
    num = 0
    for row in reader:
        num_all += 1
        if row['relation'] == '推荐药品':
            num += 1
            medicine, mediduct = extract_label(row['tail'], '(', ')')
            mediduct_dict[mediduct] = 1
            medicine_dict[medicine] = 1

    print(f"total rows: {num_all}, mediduct: {num}")
    return mediduct_dict.keys(), medicine_dict.keys()


# 提取所有的"宜吃食物"
def extract_food_names():
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    food_dict = {}
    num_all = 0
    num = 0
    for row in reader:
        num_all += 1
        if row['relation'] == '宜吃食物':
            num += 1
            food_dict[row['tail']] = 1

    print(f"total rows: {num_all}, food: {num}")
    return food_dict.keys()


# 提取所有的"忌吃食物"
def extract_nofood_names():
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    no_food_dict = {}
    num_all = 0
    num = 0
    for row in reader:
        num_all += 1
        if row['relation'] == '忌吃食物':
            num += 1
            no_food_dict[row['tail']] = 1

    print(f"total rows: {num_all}, nofood: {num}")
    return no_food_dict.keys()


# 提取所有的"推荐食谱"
def extract_diet_names():
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    diet_dict = {}
    num_all = 0
    num = 0
    for row in reader:
        num_all += 1
        if row['relation'] == '推荐食谱':
            num += 1
            diet_dict[row['tail']] = 1

    print(f"total rows: {num_all}, diet: {num}")
    return diet_dict.keys()


# 提取指定 relation 下所有的 tail, 用于检查数据类型
def extract_tails(relation):
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    dict = {}
    num_all = 0
    num = 0
    for row in reader:
        num_all += 1
        if row['relation'] == relation:
            num += 1
            dict[row['tail']] = 1

    print(f"total rows: {num_all}, diet: {num}")
    return dict.keys()


def get_full_disease_nodes():
    disease_list = extract_disease_names()  # 组织为 {疾病名称: {属性: 属性值}}
    disease_dict = {}
    for disease in disease_list:
        disease_dict[disease] = {
            'name': disease,
            'intro': '',
            'cause': '',
            'precaution': '',
            'tips': '',
            'assurance': '',
            'ratio': '',
            'fee': '',
            'cure_ratio': '',
            'treatment_intro': '',
            'susceptibility': '',
            'period': '',
            'complication': '',
        }

    param_map = {
        '简介': 'intro',
        '病因': 'cause',
        '预防方式': 'precaution',
        '注意事项': 'tips',
        '医保疾病': 'assurance',
        '患病比例': 'ratio',
        '治疗费用': 'fee',
        '治愈率': 'cure_ratio',
        '治疗概述': 'treatment_intro',
        '易感人群': 'susceptibility',
        '治疗周期': 'period',
        '并发症': 'complication',
    }
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)
    for row in reader:
        label, dname = extract_label(row['head'])
        if label != '疾病':
            continue
        if row['relation'] in param_map:
            disease_dict[dname][param_map[row['relation']]] = row['tail']

    return disease_dict


def init_disease_nodes(driver):
    disease_nodes = get_full_disease_nodes()
    num = 0
    for dname in disease_nodes:
        resp = create_disease_query(driver, disease_nodes[dname])
        if resp.summary.counters.nodes_created != 1:
            print('出问题了! ' + str(resp.summary.metadata.parameters))
        else:
            num += resp.summary.counters.nodes_created

    print("total nodes number: " + str(len(disease_nodes)) + ", created: " + str(num))


def init_other_nodes(driver):
    # 症状
    nodes = extract_symptom_names()
    for item in nodes:
        create_node_query(driver, '症状', item)

    # 药物
    nodes_medicine = list(extract_medicine_names())
    # 药品, 其它药物
    nodes_mediduct, nodes_other_medicine = extract_mediduct_names()

    for item in nodes_other_medicine:
        if not item in nodes_medicine:
            nodes_medicine.append(item)
    for item in nodes_medicine:
        create_node_query(driver, '药物', item)
    for item in nodes_mediduct:
        create_node_query(driver, '药品', item)

    # 食物
    nodes = extract_food_names()
    for item in nodes:
        create_node_query(driver, '食物', item)

    # 食谱
    nodes = extract_diet_names()
    for item in nodes:
        create_node_query(driver, '食谱', item)

    # 一级科室/二级科室/三级科室
    nodes = extract_department_names()
    for k1 in nodes:
        if k1 != '':
            create_node_query(driver, '一级科室', k1)
        for k2 in nodes[k1]:
            if k2 != '':
                create_node_query(driver, '二级科室', k2)
            for k3 in nodes[k1][k2]:
                if k3 != '':
                    create_node_query(driver, '三级科室', k3)

    # 治疗方式
    nodes = extract_treatment_names()
    for item in nodes:
        create_node_query(driver, '治疗方式', item)

    # 传染方式
    nodes = extract_infection_names()
    for item in nodes:
        create_node_query(driver, '传染方式', item)

    print('all done.')


def init_relations(driver):
    file = open(csv_file, mode="r")
    reader = csv.DictReader(file)

    # 疾病->科室 关系需要遍历完成才能获得
    disease_department_map = {}
    for row in reader:
        label, hname = extract_label(row['head'])
        if label != '疾病':
            continue

        resplist = []
        disease_department_map[hname] = ['', '']
        if row['relation'] == '二级科室分类':
            disease_department_map[hname][0] = row['tail']
        elif row['relation'] == '三级科室分类':
            disease_department_map[hname][1] = row['tail']
        elif row['relation'] == '症状':
            # (:疾病)-[:症状表现]->(:症状)
            resp = create_dircted_relation_query(driver, '疾病', '症状', hname, row['tail'], '症状表现')
            resplist.append(resp)
        elif row['relation'] == '常用药品':
            # (:疾病)-[:常用药物]->(:药物)
            inf_list = row['tail'].split()
            for inf in inf_list:
                if inf != '':
                    resp = create_dircted_relation_query(driver, '疾病', '药物', hname, inf, '常用药物')
                    resplist.append(resp)
        elif row['relation'] == '推荐药品':
            medicine, mediduct = extract_label(row['tail'], '(', ')')
            # (:药物)-[:药物产品]->(:药品)
            resp = create_dircted_relation_query(driver, '药物', '药品', medicine, mediduct, '药物产品')
            resplist.append(resp)
            # (:疾病)-[:推荐药品]->(:药品)
            resp = create_dircted_relation_query(driver, '疾病', '药品', hname, mediduct, '推荐药品')
            resplist.append(resp)
        elif row['relation'] == '治疗方式':
            # (:疾病)-[:治疗]->(:治疗方式)
            inf_list = re.split('[，、 ]', row['tail'])
            for inf in inf_list:
                if inf != '':
                    inf = inf.strip('，。 、')
                    resp = create_dircted_relation_query(driver, '疾病', '治疗方式', hname, inf, '治疗')
                    resplist.append(resp)
        elif row['relation'] == '传染方式':
            # (:疾病)-[:传染]->(:传染方式)
            inf_list = re.split('[ ]', row['tail'])
            for inf in inf_list:
                if inf != '':
                    resp = create_dircted_relation_query(driver, '疾病', '传染方式', hname, inf, '传染')
                    resplist.append(resp)
        elif row['relation'] == '宜吃食物':
            # (:疾病)-[:宜吃]->(:食物)
            resp = create_dircted_relation_query(driver, '疾病', '食物', hname, row['tail'], '宜吃')
            resplist.append(resp)
        elif row['relation'] == '忌吃食物':
            # (:疾病)-[:忌吃]->(:食物)
            resp = create_dircted_relation_query(driver, '疾病', '食物', hname, row['tail'], '忌吃')
            resplist.append(resp)
        elif row['relation'] == '推荐食谱':
            # (:疾病)-[:推荐食谱]->(:食谱)
            resp = create_dircted_relation_query(driver, '疾病', '食谱', hname, row['tail'], '推荐食谱')
            resplist.append(resp)

    # (:疾病)-[:科室分类]->(:二/三级科室)
    for disease_name in disease_department_map:
        if disease_department_map[disease_name][1] != '':
            department_name = disease_department_map[disease_name][1]
            target_label = '三级科室'
        else:
            department_name = disease_department_map[disease_name][0]
            target_label = '二级科室'
        resp = create_dircted_relation_query(driver, '疾病', target_label, disease_name, department_name, '科室分类')
        resplist.append(resp)

    # (:一级科室)-[:科室下属]->(:二级科室)-[:科室下属]->(:三级科室)
    department_dict = extract_department_names()
    for k1 in department_dict:
        for k2 in department_dict[k1]:
            resp = create_dircted_relation_query(driver, '一级科室', '二级科室', k1, k2, '科室下属')
            resplist.append(resp)
            for k3 in department_dict[k1][k2]:
                if k3 != '':
                    resp = create_dircted_relation_query(driver, '二级科室', '三级科室', k2, k3, '科室下属')
                    resplist.append(resp)

    for resp in resplist:
        print(resp.summary.counters)

    print('all done.')

# todo "可能疾病" 的尾节点构成的疾病集合是否包含在头节点里的疾病集合里需要验证；是否需要增加”可能疾病“这一关系需要再考虑；


def query_by_nl(driver, nl, key='standardFulltext'):
    query = (f"CALL db.index.fulltext.queryNodes('{key}', $nl) YIELD node, score"
             f" WITH node, score"
             f" MATCH (node)-[:`症状表现`]-(b:`症状`)"
             f" WHERE $nl contains b.`名称` or $nl contains node.`名称`"
             f" RETURN node.`名称` AS name, node.`简介` AS intro, node.`预防方式` AS avoid, score "
             f" ORDER BY score desc LIMIT 3")

    response = driver.execute_query(query, nl=nl)
    return response

'''
driver = GraphDatabase.driver(db['uri'], auth=(db['username'], db['password']))

resp = query_by_nl(driver, '头痛发烧，干咳不止是怎么回事')
for record in resp.records:
    print(record.data())
driver.close()

exit(0)

'''
# resp = {}

# print("node created: %d" % resp.summary.counters.nodes_created)
# print("query parameters: %s" % str(resp.summary.metadata.parameters))







'''









-----作为属性-----




----作为节点-----

可能疾病:疾病（检查完成）
症状:症状（检查完成）

一级科室分类:一级科室（检查完成）
二级科室分类:二级科室（检查完成）
三级科室分类:三级科室（检查完成）
三级科室构成一个树状结构，然后使用“科室分类”关系将“疾病”与其叶节点关联即可。
注意：某些分类里没有三级科室，只到二级科室。

常用药物:药物分类，空格分隔的多个治疗方式（检查完成）
推荐药品:药品产品（药物分类）（检查完成）
将“常用药品”作为分类，“推荐药品”作为子类，创建 药物-药品 关系；
“常用药品”中分类不完备，需要与从“推荐药品”中提取的药物分类名称合并；

传染方式:传染（检查完成）
治疗方式:治疗（检查完成）

宜吃食物:食物（检查完成）
忌吃食物:食物（检查完成），都包含在“宜吃食物”的列表中；

推荐食谱:食谱（检查完成）

就诊科室: 与科室分类重复（检查完成，删除即可）


-----作为关系-----



（:疾病)-[:症状表现]->(:症状)
（:症状)-[:可能疾病]->(:疾病)  todo 这两行可以合并？


(:一级科室)-[:科室下属]->(:二级科室)-[:科室下属]->(:三级科室)
(:疾病)-[:科室分类]->(:二/三级科室)

(:药物)-[:药物产品]->(:药品)
(:疾病)-[:常用药物]->(:药物)
(:疾病)-[:推荐药品]->(:药品)

(:疾病)-[:治疗]->(:治疗方式)
(:疾病)-[:传染]->(:传染方式)

(:疾病)-[:宜吃]->(:食物)
(:疾病)-[:忌吃]->(:食物)

(:疾病)-[:推荐食谱]->(:食谱)



'''











