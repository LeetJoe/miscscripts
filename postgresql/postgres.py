import psycopg2
import time

from psycopg2 import extras

from config import pg as pgconfig


# print data
def show_data(data, iter):
    new_arr = []
    print('we got ' + str(len(data)) + ' rows of records')
    for item in data:
        list_item = list(item)
        list_item[0] = list_item[0] + "_" + str(iter)
        new_arr.append(list_item)
    return new_arr


# open db connection
db = psycopg2.connect(host=pgconfig.host,
                      port=pgconfig.port,
                      user=pgconfig.user,
                      password=pgconfig.passwd,
                      database=pgconfig.db)

# when bulk inserting we should comment this line
# db.autocommit = True

# get the cursor
cursor = db.cursor()


def insert_data(arr):
    insert_sql = 'insert into class_table (class_name, "comment", en_name, ch_name, class_num) values %s'
    extras.execute_values(cursor, insert_sql, arr, page_size=len(arr))
#    cursor.executemany(sql, arr)
    print(f"successfully added {cursor.rowcount} rows")


# for loop
pageSize = 2000000
for i in range(13, 15):
    j = 0
    while True:
        sql = "SELECT * FROM class_table where class_name not like '%\_" + str(i) + "' order by class_name limit " + \
              str(pageSize) + " offset " + str(j) + ";"
        print(sql)
        qst = time.time()
        cursor.execute(sql)
        allrows = cursor.fetchall()
        qet = time.time()
        if len(allrows) > 0:
            arr = show_data(allrows, i)
            insert_data(arr)
            iet = time.time()
            j += pageSize
            print('query time is ' + str(qet - qst) + 's while insert time is ' + str(iet - qet) + 's.')
        else:
            break
    db.commit()        # it is faster than put this in the InsertData method
    print('turn of num ' + str(i) + ' complete')

# close connection
cursor.close()
db.close()
