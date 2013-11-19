#coding=utf8
from flask import render_template,request,redirect,flash,url_for,session,make_response,g
import forms,models,account,random,note
from server import app
from functools import wraps



@app.before_request
def before_request():
    g.user = None
    if request.cookies.get('username') and request.cookies.get('cookiecode'):
        if account.valid_cookiecode(request.cookies.get('username'),request.cookies.get('cookiecode')):
            if not session.get('uid'):
                account.write_session(account.get_user_id(request.cookies.get('username')))
            g.user = models.User(request.cookies.get('username'),session.get('uid'))
        else:
            return redirect(url_for('logout'))

def login_required(f):
    @wraps(f)
    def validuserlogin():
        if not g.user:
            return redirect(url_for('login'))
        return f()
    return validuserlogin


@app.route('/')
def index():
    if g.user:
        notes = note.notes_index(g.user.id)
        return render_template('userindex.html',notes=notes)
    return render_template('index.html')

@app.route('/regist',methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        registform = forms.RegistForm(request.form)
        formvalidinfo = registform.valid()
        if formvalidinfo.is_success:
            accountcreateInfo = account.create_account(registform)
            if accountcreateInfo.is_success:
                return redirect(url_for('login'))
            else:
                flash(accountcreateInfo.message)
        else:
            flash(formvalidinfo.message)
    return render_template('regist.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        loginform = forms.LoginForm(request.form)
        formvalidinfo = loginform.valid()
        if formvalidinfo.is_success:
            logininfo = account.account_login(loginform)
            if logininfo.is_success:
                g.user = models.User(loginform.username, account.get_user_id(loginform.username))
                resp = make_response(redirect(url_for('index')))
                account.write_cookie(resp,g.user.username)
                account.write_session(g.user.id)
                return resp
            else:
                flash(logininfo.message)
                print logininfo.message
        else:
            flash(formvalidinfo.message)
            print formvalidinfo.message
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('username')
    resp.delete_cookie('cookiecode')
    return resp

@app.route('/profile')
@login_required
def profile():
    return 'profile page'

@app.route('/write_note',methods=['GET','POST'])
@login_required
def write_note():
    if request.method == 'POST':
        writenoteform = forms.WriteNoteForm(request.form)
        formvalidinfo = writenoteform.valid()
        if formvalidinfo.is_success:
            note.write_note(writenoteform,g.user.id)
            return redirect(url_for('index'))
        else:
            flash(logininfo.message)
    return render_template('write_note.html')