import json
from urllib import request

from .db import database

from flask import Flask, render_template, request, redirect, session, url_for, Blueprint

# from .naver_Login import Naver_getData
from .google_Login import Google_user_data_getter
from .naver_Login import Naver_user_data_getter

bp = Blueprint("user",__name__,url_prefix='/')

with open("./config/config.json", 'r') as file:
    data_json = json.load(file)

@bp.route('/login')
def board_login():
    if (request.args.get("id")):
        print('asdfasdf')
        return render_template('login.html', data='check')
    else:
        return render_template('login.html')


@bp.route('/logout')
def board_logout():
    session.pop('id', None)
    if session :
        session.pop('id', None)
        session.pop('social', None)
        return redirect('/NaverLogin/logout')
    return redirect('/')


@bp.route('/register_action', methods=['POST'])
def board_register_action():
    form_id = request.form.get('id')
    form_passwd = request.form.get('password')
    form_username = request.form.get('username')
    form_email = request.form.get('email')
    sql = f"select * from users where id = %s"
    database.cur.execute(sql,(form_id))
    a = database.cur.fetchall()
    if len(a) >= 1:
        return redirect(url_for('user.board_register', id="fail"))
    sql = f"select * from users where email = %s"
    database.cur.execute(sql,form_email)
    b = database.cur.fetchall()
    if len(b) >= 1:
        return redirect(url_for('user.board_register', email="fail"))
    sql = f"insert into users (id, password,username, register_date, email) values(%s,%s,%s,now(),%s)"
    database.cur.execute(sql,(form_id,form_passwd,form_username,form_email))
    database.db.commit()
    print(sql)
    return redirect('/')

@bp.route('/register_action_social')
def board_register_action_social():
    social = request.args.get('social')
    if(social == 'google'):
        google_data = Google_user_data_getter()
        sql = f"insert into users (id, password,username, register_date, email,social) values(%s,%s,%s,now(),%s,%s)"
        database.cur.execute(sql,(google_data['id'],' ',google_data['name'],google_data['email'],'google'))
        database.db.commit()
        return redirect('/')

    elif(social== 'naver'):
        naver_data = Naver_user_data_getter()
        naver_data = naver_data['response']
        sql = f"insert into users (id, password,username, register_date, email,social) values(%s,%s,%s,now(),%s,%s)"
        database.cur.execute(sql, (naver_data['id'][0:16], ' ', naver_data['name'], naver_data['email'],'naver'))
        database.db.commit()
        return redirect('/')

@bp.route('/register')
def board_register():
    if request.args.get('id'):
        return render_template('/register.html', data='id')
    elif request.args.get('email'):
        return render_template('/register.html', data='email')
    else:
        return render_template('/register.html')


@bp.route('/login_action', methods=['POST', 'GET'])
def board_login_action():
    if request.method == 'POST':
        form_id = request.form.get('id')
        form_passwd = request.form.get('password')
        sql = "select * from users where id = %s and password = %s"
        print(sql, (form_id, form_passwd))
        database.cur.execute(sql, (form_id, form_passwd))
        data = database.cur.fetchall()
        if len(data) == 1:
            print(data)
            session["id"] = form_id
            return redirect("/")
        else:
            return redirect(url_for('user.board_login', id="fail"))
    elif request.method == 'GET':
        social = request.args.get('social')
        sql = 'select * from users where social = %s and email = %s'
        if(social=='google'):
            google_data = Google_user_data_getter()
            print('값 : ㅋㅋ', google_data)
            # User_Data 객체 생성
            database.cur.execute(sql,(social,google_data['email']))
            len_sql = database.cur.fetchall()
            print(len_sql)
            if len_sql == ():
                session['id'] = google_data['name']
                return redirect("/")
            else :
                return redirect(url_for('user.board_register_action_social',social="google"))
        else:
            naver_data = Naver_user_data_getter()
            naver_data = naver_data['response']
            print('값 : ㅋㅋ', naver_data)
            # User_Data 객체 생성
            database.cur.execute(sql,(social,naver_data['id'][0:16]))
            len_sql = database.cur.fetchall()
            print(len_sql)
            if len_sql == ():
                session['id'] = naver_data['name']
                session['social'] = 'naver'
                return redirect("/")
            else:
                return redirect(url_for('user.board_register_action_social',social="naver"))


