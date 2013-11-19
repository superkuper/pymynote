#coding=utf8
import account,time,models
from db import DBconn

def notes_index(uid):
    dbconn = DBconn()
    sql = 'select title,content,date from notes where uid = %s'
    dbconn.cursor.execute(sql,uid)
    ret = dbconn.cursor.fetchall()
    notes = []
    for i in ret:
        title = i[0]
        content = i[1]
        date = i[2]
        note = models.Note(uid,title,content,date)
        notes.append(note)
    return notes

def write_note(noteform,uid):
    dbconn = DBconn()
    uid = uid
    title = noteform.title
    content = noteform.content
    date = noteform.date
    createdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    sql = 'insert into notes (uid,title,content,date,createdate) values(%s,%s,%s,%s,%s)'
    dbconn.cursor.execute(sql,(uid,title,content,date,createdate))
    dbconn.connection.commit()