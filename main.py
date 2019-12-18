import json
from operations import *


def main():
    with open("config.json", 'r', encoding="UTF-8") as f:
        data = json.load(f)
    conn = connect(data['host'], data['port'], data['user'], data['password'])
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    tables = data['tables']
    for tableName in tables:
        table = tables[tableName]
        columns = tuple([x for x in table['data']])
        createTable(conn=conn, cursor=cursor, table=table, tableName=tableName)
        values = generateData(table=table, tablename=tableName)
        myInsert(conn=conn, cursor=cursor, columns=columns, values=values, tablename=tableName)


if __name__ == '__main__':
    main()