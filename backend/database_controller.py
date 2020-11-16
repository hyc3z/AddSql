import csv
import os
import sqlite3
import pymysql

class DatabaseController:


    def __init__(self, filename="database.db", dbtype="sqlite3"):
        self.retry = False
        if dbtype == "sqlite3":
            self.dbtype = "sqlite3"
            self.connection = sqlite3.connect(filename)
            self.cursor = self.connection.cursor()
        elif dbtype == "mysql":
            self.dbtype = "mysql"
            self.connection = None
            self.cursor = None
            self.getconfigure()

    def getconfigure(self):
        #
        try:
            if os.path.exists("../utils/db.csv"):
                f = open("../utils/db.csv", "r")
                reader = csv.DictReader(f)
                for i in reader:
                    self.host = (i['host'])
                    self.port = int(i['port'])
                    self.user = (i['user'])
                    self.password = i['password']
                    self.charset = i['charset']
                    self.database = i['database']
                f.close()
            else:
                data = {"host": "127.0.0.1",
                        "port":3306,
                        "user":"root",
                        "password":"000000",
                        "charset":"utf8",
                        "database":"ceju"
                       }
                f = open("../utils/db.csv", "w")
                fieldname = {"host", "port", "user","password","charset","database"}
                writer = csv.DictWriter(f, fieldnames=fieldname)
                writer.writeheader()
                writer.writerow(data)
                f.close()
                f = open("../utils/db.csv", "r")
                reader = csv.DictReader(f)
                for i in reader:
                    self.host = (i['host'])
                    self.port = int(i['port'])
                    self.user = (i['user'])
                    self.password = i['password']
                    self.charset = i['charset']
                    self.database = i['database']
                f.close()
        except:
            pass

    def mysqlConnect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                charset=self.charset,
                database=self.database,
                connect_timeout=3
            )
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            return 0
        except Exception as e:
            print(e)
            return e


    def formatted_arg(self,key,value):
        real_value =  "'{}'".format(value) if len(value) > 0 else 'NULL'
        join_word = '=' if len(value) > 0 else ' IS '
        return "`{}`".format(key)+join_word+str(real_value)

    def get_column_data(self, table_name):
        if self.dbtype == "mysql":
            if self.connection is None or self.retry:
                retval = self.mysqlConnect()
                if retval != 0:
                    self.retry = True
                    return -1
        if self.dbtype == "sqlite3":
            sql_statement = "DESCRIBE `{}`;".format(table_name)
        else:
            sql_statement = "DESCRIBE `{}`;".format(table_name)
        self.cursor.execute(sql_statement)
        res = self.cursor.fetchall()
        if len(res) > 0:
            return res
        else:
            return 1

if __name__ == '__main__':
    controller = DatabaseController(dbtype="mysql")
    res = controller.get_column_data("user_info")
    from utils import dict2py
    dict2py.dumpDict2Py(res, "output.py", "USER_COLUMNS")


