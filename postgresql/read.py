import psycopg2
import time

from config import pg as pgconfig

# open db connection
db = psycopg2.connect(host=pgconfig.host,
                      port=pgconfig.port,
                      user=pgconfig.user,
                      password=pgconfig.passwd,
                      database=pgconfig.db)

db.autocommit = True

# get the cursor
cursor = db.cursor()

# read test


# for loop
pageSize = 1000000
j = 3000000
while True:
    sql = "SELECT * FROM class_table order by class_name limit " + str(pageSize) + " offset " + str(j) + ";"
#    sql = "SELECT * FROM class_table limit " + str(j) + ";"
    qst = time.time()
    cursor.execute(sql)
    qet = time.time()
    allrows = cursor.fetchall()
    fet = time.time()
    if len(allrows) < 100000000:
        print('offset:' + str(j) + ', page size:' + str(pageSize))
        print('execute time is ' + str(qet - qst) + 's and fetch time is ' + str(fet - qet) + 's.')
        j += pageSize
        time.sleep(3)
    else:
        break
# db.commit()        # it is faster than put this in the InsertData method

# close connection
cursor.close()
db.close()
