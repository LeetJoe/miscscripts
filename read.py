import psycopg2
import time


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

db.autocommit = True

# get the cursor
cursor = db.cursor()

# read test


# for loop
pageSize = 2000000
j = 0
while True:
    sql = "SELECT * FROM class_table order by class_name limit " + str(pageSize) + " offset " + str(j) + ";"
    qst = time.time()
    cursor.execute(sql)
    allrows = cursor.fetchall()
    qet = time.time()
    if len(allrows) > 0:
        j += pageSize
        print('query time is ' + str(qet - qst) + 's.')
    else:
        break
# db.commit()        # it is faster than put this in the InsertData method

# close connection
cursor.close()
db.close()
