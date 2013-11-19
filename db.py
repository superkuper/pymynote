#coding=utf8
import MySQLdb

class DBconn():
    def __init__(self):
        self.connection = MySQLdb.connect(host='localhost',user='root',passwd='root',db='mynote',port=3306)
        self.cursor = self.connection.cursor()