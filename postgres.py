import psycopg2
import time

from psycopg2 import extras

# print data
def ShowData(data, i):
    arr = []
    print('we got ' + str(len(data)) + ' rows of records')
    for item in data:
        item = list(item)
        item[0] = item[0] + "_" + str(i)
        arr.append(item)
    return arr

# open db connection
'''
db = psycopg2.connect(host = '172.18.34.37',
                      port = '5003',
                      user = 'postgres',
                      password = '',
                      database = 'sc_owltest')
'''
db = psycopg2.connect(host = '127.0.0.1',
                      port = '5432',
                      user = 'neosong',
                      password = '123456',
                      database = 'owltest')

# when bulk inserting we should comment this line
# db.autocommit = True

# get the cursor
cursor = db.cursor()

def InsertData(arr):
    sql = 'insert into class_table (class_name, "comment", en_name, ch_name, class_num) values %s'
    extras.execute_values(cursor, sql, arr, page_size = len(arr))
#    cursor.executemany(sql, arr)
    print(f"successfully added {cursor.rowcount} rows")


# for loop
pageSize = 40000
for i in range(11, 14):
    j = 0
    while True:
        sql = "SELECT * FROM class_table where class_name not like '%\_" + str(i) + "' order by class_name limit " + str(pageSize) + " offset " + str(j) + ";"
        print(sql)
        qst = time.time()
        cursor.execute(sql)
        allrows = cursor.fetchall()
        qet = time.time()
        if (len(allrows) > 0):
            arr = ShowData(allrows, i)
            InsertData(arr)
            iet = time.time()
            j += pageSize
            print('query time is ' + str(qet - qst) + 's while insert time is ' + str(iet - qet) + 's.')
        else:
            break
    db.commit() # it is faster than put this in the InsertData method
    print('turn of num ' + str(i) + ' complete')

# close connection
cursor.close()
db.close()