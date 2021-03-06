import mysql.connector
from mysql.connector import errorcode
import string
import  json


class Database(object):
    def __init__(self, my_user,my_password, my_host, my_database ):
        self.cnx = mysql.connector.connect(
            user=my_user,
            password=my_password,
            host=my_host,
            database=my_database
        )

        self.database = my_database
        self.acceptDataType = [list, tuple]
        self.cursor = self.cnx.cursor()

        try:
            # try to connect to database
            self.cnx.database = my_database
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(my_database)
                self.cnx.database = my_database
            else:
                print(err)
                exit(1)
    def get_cursor(self):
        return self.cursor

    def get_cnx(self):
        return self.cnx

    def create_database(self, my_database):
        try:
            self.cursor.execute(
                'CREATE DATABASE {} DEFAULT CHARACTER SET \'utf8\''.format(my_database))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def create_table_other(self,table_name, command):
        try:
            print("Creating table {}: ".format(table_name), end='')
            self.cursor.execute(command)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    def show_database(self):
        try:
            query = "show databases;"
            self.cursor.execute(query)
            return self.cursor.fetchall()

        except mysql.connector.Error as err:
            print(err.msg)

    def show_tables(self,database=None):
        if database == None:
            print("Please use show_tables(database) in this function call")
            exit(1)
        self.cursor.execute("use {};".format(database))
        self.cursor.execute("show tables;")
        return self.cursor.fetchall()

    def drop_database(self,database=None):
        if database == None:
            print("Please use show_tables(database) in this function call")
            exit(1)
        try:
            query = "DROP DATABASE {};".format(database)
            self.cursor.execute(query)
            print("Drop database {} successfully".format(database))
        except mysql.connector.Error as err:
            print(err.msg)

    def drop_table(self,table):
        try:
            query = "DROP TABLE {}".format(table)
            self.cursor.execute(query)
            print("Success to drop table {} from database {}".format(table, self.database))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)

    def create_tables(self, table_name, element, key):
        # table = "Courses2"
        query = "CREATE TABLE {} (".format(table_name)
        for item in element:
            query += " {} {} , ".format(item[0], item[1])
        query += "PRIMARY KEY ({}) )".format(key)
        try:
            print("Creating table {}: ".format(table_name), end='')
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
        self.cnx.commit()

    """
    [('time', 'datetime', 'NO', 'PRI', None, ''), ('comments', 'varchar(11)', 'YES', '', None, '')]
    [ (column1, type, Null, keyOrNot, None, "), (), () ]
    """

    def describe_table(self,table=None):
        if table == None:
            print("Please use show_tables(database) in this function call")
            exit(1)
        query = "DESCRIBE {:s}; ".format(table)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    '''
    # INSERT INTO tbl_name (col1,col2) VALUES(15,col1*2);

    def insert_data(self,table, data):
        # if not (type(table) in self.acceptDataType and type(data) in self.acceptDataType):
        #     print("table/data must be a list or tuple")
        #     raise TypeError
        # if len(table) != len(data):
        #     print("the length of table and data should be same")
        #     raise RuntimeError

        # print(data[0][1])
        # data[0][1] = "\'" + str(data[0][1]) + "'"
        query = "INSERT INTO {} (".format(table)
        for item in data:
            query += "{} ,".format(item[0])
        query = query.strip(",") + ") VALUES("

        for item in data:
            print(type(item[1]))
            if type(item[1]) == str:
                query = query + "\'{}\',".format(item[1])
            else:
                query += "{},".format(item[1])
        query = query.strip(",") + ");"

        print(query)
        self.cursor.execute(query)
        self.cnx.commit()

        # a,b,c) VALUES(1,2,3,4,5,6,7,8,9);"
    '''
    def insert_data(self, data,table=None):
        if table == None:
            table = self.table

        if type(data[0]) == list or type(data[0]) == tuple:
            column = self.describe_table(table)
            # data[0][1] = "\'" + data[0][1] + "'"
            query = "INSERT INTO {} (".format(table)
            for item in data:
                query += "{} ,".format(item[0])
            query = query.strip(",") + ") VALUES("

            for index in range(len(data)):
                # column[index][1] is the data type of this column
                # if "char" in column[index][1]:
                #     data[index][1] = "\'" + data[index][1] + "'"

                query += "{},".format(data[index][1])
            query = query.strip(",") + ");"
            # print(query)
            # self.cursor.execute(query)
            # self.cnx.commit()

        else:
            column = self.describe_table(table)
            insert_key = []
            for item in column:
                if item[5] == "auto_increment":
                    continue
                insert_key.append(item[0])

            # data[0][1] = "\'" + data[0][1] + "'"
            query = "INSERT INTO {} (".format(table)
            for item in insert_key:
                query += "{} ,".format(item)
            query = query.strip(",") + ") VALUES("

            for item in data:
                if type(item) == str:
                    item = item.replace("'", "")
                query += "'{}',".format(item)
            query = query.strip(",") + ");"
            # print(query)
        try:
            print(query)
            self.cursor.execute(query)
            self.cnx.commit()
            print("OK")
        except mysql.connector.Error as err:
            print(err.msg)

    def queryData(self, queryTable):
        """
        :param queryTable: string, the table we want to query
        :return: list, contains
        this function .....
        """
        query = "select * from {}".format(queryTable)
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def queryColsData(self, querTable, cols):
        if type(cols) != list:
            raise ("please input a list of cols")
            return
        query = "select {} from {}".format(', '.join(cols), querTable)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def user_exist(self,user_name,user_password):
        data = self.queryData("User_info")
        for i in data:
            if i[0] == user_name:
                if i[1] == user_password:
                    return True
        return False



if __name__ == '__main__':
    pass
