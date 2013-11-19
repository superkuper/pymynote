#coding=utf8
from db import DBconn
import account


class User():
    def __init__(self,username,uid):
        self.username = username
        self.id = uid


class Note():
    def __init__(self,uid,title,content,date):
        self.owner = uid
        self.title = title
        self.content = content
        self.date = date