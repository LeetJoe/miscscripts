import appsearchApi
import psycopg2

engine_name = 'neosong-test-app-search-engine'


'''
new_schema = {
    "class_name": "text",
    "comment": "text",
    "en_name": "text",
    "ch_name": "text",
    "class_num": "text"
}
print(appsearchApi.updateSchema(engine_name, new_schema))

'''


# open db connection

db = psycopg2.connect(host = '127.0.0.1',
                      port = '5432',
                      user = 'neosong',
                      password = '123456',
                      database = 'owltest')

db.autocommit = True

# get the cursor
cursor = db.cursor()

# read test

columnarr = ["class_name", "en_name", "ch_name", "comment", "class_num"]
# for loop
queryPageSize = 100000
pageSize = 100
j = 157914000      #   40063700    85564600    118543600     146992000
jend = 197700000   #   57700000    97700000    137700000     197700000
while True:
    sql = "SELECT class_name,en_name,ch_name,comment,class_num FROM class_table limit " + str(queryPageSize) + " offset " + str(j) + ";"
    cursor.execute(sql)
    allrows = cursor.fetchall()
    if len(allrows) > 0:
        allrowsnum = len(allrows)
        allrowscount = 0
        newrows = []
        innerTurn = 0
        print("now offset is " + str(j) + " and limit is " + str(queryPageSize) + " and we got " + str(allrowsnum))
        for item in allrows:
            allrowscount += 1
            j += 1
            newitem = {}
            for i in range(0, 5):
                if item[i] is None:
                    newitem[columnarr[i]] = ""
                else:
                    newitem[columnarr[i]] = item[i]
            newrows.append(newitem)

            if (len(newrows) >= 100 or allrowscount >= allrowsnum) :
                resp = appsearchApi.indexDoc(engine_name, newrows)
                print(str(innerTurn * pageSize + 1) + " ~ " + str(allrowscount) + " of " + str(queryPageSize))
                if resp is not None:
                    useless = 1  # print(resp)
                else:
                    print("get None response! something may be wrong")
                newrows = []
                innerTurn += 1

            if j >= jend :   # the last turn may not cover the allrows and should stop if j reached jend
                break
        if j >= jend :
            break
    else:
        break
# db.commit()        # it is faster than put this in the InsertData method

# close connection
cursor.close()
db.close()

print("Done")
