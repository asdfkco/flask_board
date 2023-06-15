import json
from urllib import request


from flask import Flask, render_template, request, redirect, session, make_response, url_for, Blueprint
import pymysql
import math

bp = Blueprint("user",__name__,url_prefix='/')

with open("./config/config.json", 'r') as file:
    data_json = json.load(file)

db = pymysql.connect(host=data_json["host"], user=data_json["user"], passwd=data_json["passwd"], db="free_board",
                     charset="utf8")
cur = db.cursor()



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
    sql = f"select * from users where id = '{form_id}'"
    cur.execute(sql)
    a = cur.fetchall()
    if len(a) >= 1:
        return redirect(url_for('board_register', id="fail"))
    sql = f"select * from users where email = '{form_email}'"
    cur.execute(sql)
    b = cur.fetchall()
    if len(b) >= 1:
        return redirect(url_for('board_register', email="fail"))
    sql = f"insert into users values('{form_id}','{form_passwd}',now(),'{form_email}')"
    cur.execute(sql)
    db.commit()
    print(sql)
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
        sql = f"select * from users where id = '{form_id}' and password = '{form_passwd}'"
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
        if len(data) == 1:
            print(data)
            session["id"] = form_id
            return redirect("/")
        else:
            return redirect(url_for('board_login', id="fail"))
    else:
        return "잘못된 접근입니다."
