import pymysql
import hashlib
import random
import time
import json


def connect(host,port,user,password,database,charset):
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset=charset,
    )
    return conn


def createtable(cursor, tablename):
    sql = "create table if not exists " + tablename + " (`id` int(10) unsigned NOT NULL COMMENT 'id',`name` varchar(32) NOT NULL COMMENT 'hash')"
    cursor.execute(sql)


def myList(value):
    new_list = []
    t = time.time()
    for i in range(1, value + 1):
        id = random.randint(1, int((value)/10000+1))
        name = "number"+str(random.randint(1,value+1))
        tup = (id,name)
        new_list.append(tup)
    print("*"*5+"generate list ok,spent "+str(time.time()-t)+"*"*5)
    return new_list


def myInsert(conn,cursor,tablename,newList):
    try:
        t = time.time()
        sql = "insert into "+tablename+" (id,name) values(%s,%s)"
        cursor.executemany(sql,newList)
        conn.commit()
        cursor.close()
        conn.close()
        print('insert ok, spent ',time.time()-t)
    except Exception as e:
        print(e)


def md5(source):
    hash = hashlib.md5()
    hash.update(bytes(source, encoding='utf-8'))
    return str(hash.hexdigest())


def main():
    with open("config.json",'r') as f:
        data = json.load(f)
    conn = connect(data['host'],data['port'],data['user'],data['password'],data['database'],data['charset'])
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    createtable(cursor, data['tablename'])
    value = 10000000
    newList = myList(value)
    myInsert(conn,cursor,data['tablename'],newList)
    # print(md5('0'))



if __name__ == '__main__':
    main()
