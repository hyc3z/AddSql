import pymysql
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


def createTable(cursor, tablename, columns, drop=False):
    if drop:
        cursor.execute("drop table if exists " + tablename)
    sql = "create table if not exists " + tablename + " ("
    for i in columns:
        sql = sql + i + " " + columns[i][0] + columns[i][1]
        sql += ","
    sql = sql[:-1]
    sql += ")"
    # print(sql)
    cursor.execute(sql)


def getType(rawType):
    if '(' in rawType:
        return [rawType.strip().split('(')[0].lower(), int(rawType.strip().split("(")[1].split(")")[0])]
    else:
        return [rawType.strip().split()[0].lower(), 256]

def randomChar(charType="all"):
    if charType.lower() == "all":
        return randomCharAll()
    elif charType.lower() == "numeric":
        return randomNumeric()
    elif charType.lower() == "lowercase":
        return randomLower()
    elif charType.lower() == "uppercase":
        return randomUpper()
    elif charType.lower() == "alphanumeric":
        return randomAlphanumeric()
    else:
        return randomCharAll()


def randomCharAll():
    return chr(random.randint(33, 126))

def randomNumeric():
    return chr(random.randint(48, 57))


def randomUpper():
    return chr(random.randint(65, 90))


def randomLower():
    return chr(random.randint(97, 122))


def randomAlphanumeric():
    choice = random.randint(1, 3)
    if choice == 1:
        return randomUpper()
    elif choice == 2:
        return randomLower()
    else:
        return randomNumeric()


def randomData(columns, num, charType, nullPercentage=0):
    newList = []
    t = time.time()
    for i in range(1, num + 1):
        if i % (int(num/100)) == 0:
            print(i, "...")
        dataList = []
        for column in columns:
            dataType = getType(columns[column][0])
            unsigned = "unsigned" in columns[column][1].lower()
            notNull = "not null" in columns[column][1].lower()
            Null = random.randint(0, 99) < nullPercentage
            # TODO:Full type support
            if Null and not notNull:
                dataList.append(None)
            else:
                if dataType[0] == 'tinyint':
                    if unsigned:
                        dataList.append(random.randint(0, min(255, 10 ** dataType[1])))
                    else:
                        dataList.append(random.randint(max(-128, -10 ** dataType[1]), min(127, 10 ** dataType[1])))
                elif dataType[0] == 'smallint':
                    if unsigned:
                        dataList.append(random.randint(0, min(65535, 10**dataType[1])))
                    else:
                        dataList.append(random.randint(max(-32768, -10 ** dataType[1]), min(32767, 10 ** dataType[1])))
                elif dataType[0] == 'mediumint':
                    if unsigned:
                        dataList.append(random.randint(0, min(16777215, 10  **dataType[1])))
                    else:
                        dataList.append(random.randint(max(-8388608, -10  ** dataType[1]), min(8388607, 10  ** dataType[1])))
                elif dataType[0] == 'int':
                    if unsigned:
                        dataList.append(random.randint(0, min(4294967295, 10  **dataType[1])))
                    else:
                        dataList.append(random.randint(max(-2147483648, -10  ** dataType[1]), min(2147483648, 10  ** dataType[1])))
                elif dataType[0] == 'bigint':
                    if unsigned:
                        dataList.append(random.randint(0, min(18446744073709551615, 10  **dataType[1])))
                    else:
                        dataList.append(random.randint(max(-9223372036854775808, -10  ** dataType[1]), min(9223372036854775807, 10  ** dataType[1])))
                elif dataType[0] == 'bit':
                    string = ""
                    for _ in range(dataType[1]):
                        string += str(random.randint(0, 1))
                    dataList.append(string)
                elif dataType[0] == 'float':
                    if unsigned:
                        dataList.append(float(random.random()))
                    else:
                        dataList.append(float('-'*random.randint(0, 1)+str(random.random())))
                elif dataType[0] == 'double':
                    if unsigned:
                        dataList.append(float(random.random()))
                    else:
                        dataList.append(float('-'*random.randint(0, 1)+str(random.random())))
                elif dataType[0] == 'varchar':
                    if Null and not notNull:
                        dataList.append(None)
                    else:
                        string = ""
                        for _ in range(dataType[1]):
                            string += randomChar(charType)
                        dataList.append(string)
        newList.append(tuple(dataList))
    print("*"*5,"generate list ok,spent ",str(time.time()-t),"*"*5)
    #print(newList)
    return newList


def myInsert(conn, cursor, tablename, columns, values):
    print(">>>inserting...")
    try:
        t = time.time()
        sql = "insert into "+tablename+" ("
        for i in columns.keys():
            sql = sql+i+","
        sql = sql[:-1]
        sql += ") values("
        for i in columns.keys():
            sql = sql+"%s,"
        sql = sql[:-1]
        sql += ")"
        cursor.executemany(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("*"*5, 'insert ok, spent ', time.time()-t, "*"*5)
    except Exception as e:
        print(e)


def main():
    with open("config.json", 'r') as f:
        data = json.load(f)
    # print(data)
    conn = connect(data['host'], data['port'], data['user'], data['password'], data['database'], data['charset'])
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    createTable(cursor, data['tableName'], data["columns"], drop=data["dropWhenCreate"])
    newList = randomData(data["columns"], data["count"], nullPercentage=data["nullPercentage"], charType=data["charType"])
    myInsert(conn, cursor, data['tableName'], data["columns"], newList)


if __name__ == '__main__':
    main()
