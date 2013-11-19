#coding=utf8
import re,message

class RegistForm():
    def __init__(self,webform):
        self.username = webform.get('username')
        self.password = webform.get('password')

    def valid(self):
        if self.username == None:
            return message.SuccessInfo(False,u'email不能为空')
        if not email_pattern(self.username):
            return message.SuccessInfo(False,u'email格式错误')
        if not len(self.password) > 5:
            return message.SuccessInfo(False,u'密码不能少于5位')
        return message.SuccessInfo(True)

class LoginForm():
    def __init__(self,webform):
        self.username = webform.get('username')
        self.password = webform.get('password')

    def valid(self):
        if self.username == None:
            return message.SuccessInfo(False,u'email不能为空')
        if not email_pattern(self.username):
            return message.SuccessInfo(False,u'email格式错误')
        if not len(self.password) > 5:
            return message.SuccessInfo(False,u'密码不能少于5位')
        return message.SuccessInfo(True)

class WriteNoteForm():
    def __init__(self,webform):
        self.title = webform.get('title')
        self.date = webform.get('date')
        self.content = webform.get('content')

    def valid(self):
        if self.title == None:
            return message.SuccessInfo(False,u'主题不能为空')
        if self.date == None:
            return message.SuccessInfo(False,u'时间不能为空')
        if self.content == None:
            return message.SuccessInfo(False,u'内容不能为空')
        return message.SuccessInfo(True)

def email_pattern(email):
    pattern = re.compile(r'^[a-zA-Z0-9_+.-]+\@([a-zA-Z0-9-]+\.)+[a-zA-Z0-9]{2,4}$')
    return pattern.match(email)