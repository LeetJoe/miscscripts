import psycopg2
import time

from psycopg2 import extras

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

# db.autocommit = True

# get the cursor
cursor = db.cursor()

# read test
st = time.time()
sql = 'SELECT * FROM class_table;'
cursor.execute(sql)
extras.execute_batch(cursor, sql, [], page_size = 10000000)
allrows = cursor.fetchall()
et = time.time()

print('the time cost: ' + str(et - st))