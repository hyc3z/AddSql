import pymysql
import time
from utils.random_generator import *


def connect(host,port,user,password):
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )
    return conn


def parseTableData(data):
    statements = []
    for x in data:
        dataSetup = data[x]['dataSetup']
        if 'length/set' in dataSetup:
            statement = "`{}` {}({}) ".format(x, dataSetup['dataType'], dataSetup['length/set'])
        else:
            statement = "`{}` {} ".format(x, dataSetup['dataType'])
        if 'unsigned' in dataSetup and dataSetup['unsigned']:
            statement += "UNSIGNED "
        if 'allowNull' in dataSetup and not dataSetup['allowNull']:
            statement += "NOT NULL "
        if 'zerofill' in dataSetup and dataSetup['zerofill']:
            statement += "ZEROFILL "
        if 'hasDefault' in dataSetup and dataSetup['hasDefault']:
            try:
                statement += "DEFAULT {} ".format(dataSetup['default'])
            except Exception as e:
                print("WARNING:Ignoring default value for", x, e)
        if 'comment' in dataSetup:
            statement += "COMMENT '{}' ".format(dataSetup['comment'])
        statements.append(statement)
    return ",\n".join(statements)


def parseTableConfig(config):
    statement = ""
    if "engine" in config:
        statement += "ENGINE={} ".format(config["engine"])
    if "charset" in config:
        statement += "DEFAULT CHARSET={} ".format(config["charset"])
    if "collate" in config:
        statement += "COLLATE={} ".format(config["collate"])
    if "comment" in config:
        statement += "COMMENT='{}' ".format(config["comment"])
    return statement


def createTable(conn, cursor, table, tableName):
    print(">>>Creating table", tableName, "...")
    config = table["tableConfig"]
    data = table["data"]
    database = config["database"]
    if "createDatabaseIfNotExists" in config and config['createDatabaseIfNotExists']:
        cursor.execute("create database if not exists {};".format(database))
    cursor.execute("use " + database)
    if config["dropIfExists"]:
        cursor.execute("drop table if exists " + table)
    dataStatements = parseTableData(data)
    tableStatements = parseTableConfig(config)
    sql = "create table if not exists `{}` ({}) {};".format(tableName, dataStatements, tableStatements)
    cursor.execute(sql)
    conn.commit()


def createTables(conn, cursor, tables):
    for tableName in tables:
        table = tables[tableName]
        createTable(conn, cursor, table, tableName)


def generateData(table, tablename):
    newList = []
    t = time.time()
    config = table['tableConfig']
    num = config['generateCount']
    data = table['data']
    print(">>>Generating data for",tablename,"...")
    for i in range(1, num + 1):
        dataList = []
        for dataName in data:
            column = data[dataName]
            if 'dataGenerator' not in column:
                continue
            else:
                generateConfig = column['dataGenerator']
                dataSetup = column['dataSetup']
                fillType = "random" if "fillType" not in generateConfig else generateConfig['fillType']
                if fillType == "selective":
                    if "fillEnum" in generateConfig:
                        Enumlist = generateConfig["fillEnum"]
                        dataList.append(random.choice(Enumlist))
                        continue
                    else:
                        print("Warning: fillType is \"selective\" ,however, fillEnum not found in .json file.")
                nullPercentage = 0 if 'nullPercentage' not in generateConfig else generateConfig['nullPercentage']
                dataType = dataSetup['dataType']
                length = dataSetup['length/set']
                unsigned = False if 'unsigned' not in dataSetup else dataSetup['unsigned']
                if 'allowNull' in dataSetup and dataSetup['allowNull']:
                    appendNone = random.randint(0, 99) < nullPercentage
                    if appendNone:
                        dataList.append(None)
                        continue
                # TODO:Full type support
                if dataType == 'tinyint':
                    dataList.append(randomTinyint(int(length), unsigned))
                elif dataType== 'smallint':
                    dataList.append(randomSmallint(int(length), unsigned))
                elif dataType == 'mediumint':
                    dataList.append(randomMediumint(int(length), unsigned))
                elif dataType == 'int':
                    dataList.append(randomInt(int(length), unsigned))
                elif dataType == 'bigint':
                    dataList.append(randomBigint(int(length), unsigned))
                elif dataType == 'bit':
                    dataList.append(randomBit(int(length)))
                elif dataType == 'float' or dataType == 'double':
                    dataList.append(randomFloat(unsigned))
                elif dataType == 'varchar':
                    fillType = "all" if "fillChar" not in generateConfig else generateConfig['fillChar']
                    dataList.append(randomVarchar(int(length), fillType))
        newList.append(tuple([str(x) for x in dataList]))
    print("*"*5, "Data generation ok,spent ", str(time.time()-t), "*"*5)
    return newList


def myInsert(conn, cursor, columns, values, tablename):
    print(">>>inserting into", tablename, "...")
    t = time.time()
    sql = "insert into `{}` (".format(tablename)
    for x in columns:
        sql+=("`{}`,".format(x))
    sql = sql[:-1]
    sql += ') VALUES ({});'.format(",".join(["%s"]*len(columns)))
    cursor.executemany(sql, values)
    conn.commit()
    print("*"*5, 'Insert done, spent ', time.time()-t, "*"*5)
