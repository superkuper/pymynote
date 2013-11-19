#coding=utf8
import random,hashlib,views,message
from flask import session
from db import DBconn




def create_account(registform):
    if valid_account_exist(registform.username):
        return message.SuccessInfo(False,u'用户已经存在')
    password,randomcode = ret_password(registform.password)
    dbconn = DBconn()
    dbconn.cursor.execute('insert into user (username,password,randomcode) values(%s,%s,%s)',(registform.username,password,randomcode))
    dbconn.connection.commit()
    return message.SuccessInfo(True,u'用户注册成功')

def account_login(loginform):
    if valid_account_exist(loginform.username):
        return valid_account_password(loginform)
    return message.SuccessInfo(False,u'用户不存在')

def valid_account_exist(username):
    dbconn = DBconn()
    dbconn.cursor.execute('select id from user where username = %s',username)
    return dbconn.cursor.fetchone()

def valid_account_password(loginform):
    dbconn = DBconn()
    sql = 'select password,randomcode from user where username = %s'
    dbconn.cursor.execute(sql,loginform.username)
    ret = dbconn.cursor.fetchone()
    retrandomcode = ret[1]
    retpassword = ret[0]
    password = hashlib.md5(loginform.password+retrandomcode).hexdigest()
    if retpassword != password:
        return message.SuccessInfo(False,u'密码错误')
    return message.SuccessInfo(True,u'用户登录成功')


def ret_password(formpassword):
    x = random.randint(1,9)
    randomcode = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz',x))
    password = hashlib.md5(formpassword+randomcode).hexdigest()
    return password,randomcode

def valid_cookiecode(username,cookiecode):
    dbconn = DBconn()
    sql = 'select cookiecode from user where username = %s'
    dbconn.cursor.execute(sql,username)
    ret = dbconn.cursor.fetchone()[0]
    return ret == cookiecode


def write_cookiecode(formemail):
    cookiecode = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz',6))
    dbconn = DBconn()
    sql = 'update user set cookiecode = %s where username = %s'
    dbconn.cursor.execute(sql,(cookiecode,formemail))
    dbconn.connection.commit()
    return cookiecode

def get_user_id(username):
    dbconn = DBconn()
    dbconn.cursor.execute('select id from user where username = %s',username)
    return dbconn.cursor.fetchone()[0]

def get_user_name(uid):
    dbconn = DBconn()
    dbconn.cursor.execute('select username from user where id = %s',uid)
    return dbconn.cursor.fetchone()[0]

def write_cookie(resp,username):
    resp.set_cookie('username', username)
    resp.set_cookie('cookiecode', write_cookiecode(username))

def write_session(uid):
    session['uid'] = uid