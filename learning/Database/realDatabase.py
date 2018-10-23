from __future__ import print_function
import mysql.connector
# from sample import database
# from sample import database
from mysql.connector import errorcode
import json


if __name__ == '__main__':
    # connect to the server
    con = mysql.connector.connect(
        user="Ruijie",
        password="gengruijie123",
        host="142.93.59.116",
        database="mysql"
    )

    cur = con.cursor()

    # cur.execute('CREATE TABLE autoGradingDatabase(key TEXT, result INTEGER)')
    # cur.execute('CREATE TABLE Density(province TEXT, population INTEGER, land_area REAL)')
    try:
        cur.execute('CREATE TABLE autoGradingDatabase(id TEXT, result INTEGER, image JSON)')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("DATABASE already exists.")
        else:
                print(err.msg)
    else:
                print("OK")
