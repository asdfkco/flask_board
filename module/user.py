import json
from urllib import request

from .db import database

from flask import Flask, render_template, request, redirect, session, url_for, Blueprint

from .naver_Login import Naver_getData
from .userDAO import User_Data

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
    return redirect('/')


@bp.route('/register_action', methods=['POST'])
def board_register_action():
    form_id = request.form.get('id')
    form_passwd = request.form.get('password')
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
    sql = f"insert into users (id, password, register_date, email) values(%s,%s,%s)"
    database.cur.execute(sql,(form_id,form_passwd,form_email))
    database.db.commit()
    print(sql)
    return redirect('/')

@bp.route('/register_action_social')
def board_register_action_social():
    return

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
        print(sql,(form_id,form_passwd))
        database.cur.execute(sql,(form_id,form_passwd))
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
        user_data = User_Data()
        data = user_data.Google_GetData
        print('값 : ㅋㅋ',data)
        # database.cur.execute(sql,(social,user_data.Google_GetData))
        return redirect("/")