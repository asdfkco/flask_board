import json
from urllib import request

import requests
from flask import Flask, render_template, request, redirect, session, make_response, url_for
import pymysql
import math

with open("config/config.json", 'r') as file:
    data_json = json.load(file)

db = pymysql.connect(host=data_json["host"], user=data_json["user"], passwd=data_json["passwd"], db="free_board", charset="utf8")
cur = db.cursor()
app = Flask(__name__)
app.secret_key = "ex_id"


@app.route('/')
def index():
    return redirect(location="/1")


@app.route('/<int:pages>')
def index_page(pages):
    sql = f"select * from board where num between {((pages - 1) * 15) + 1 if ((pages - 1) * 15) > 1 else (pages - 1) * 15} and {pages * 15}"
    total_pages = cur.execute("select * from board order by num")
    count = (math.trunc(total_pages / 10) + 1)
    print("sql : ", sql)
    cur.execute(sql)
    data_list = cur.fetchall()
    print(data_list)
    print("maxPage : ", count)
    if 'id' not in session or session["id"] == "":
        return render_template('index.html', data_list=data_list, page=count)
    else:
        return render_template('index.html', data_list=data_list, page=count, session=True)


@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/write_action')
def write_action():
    if request.method == 'POST':
        title = request.form.get('title')
        writer = request.form.get('writer')
        content = request.form.get('content')

        sql = "insert into board (title,writer,content,views) values (%s,%s,%s,0);"

        values = (title, writer, content)
        print(sql, values)
        cur.execute(sql, values)
        db.commit()
        return redirect(location="/")
    else:
        return '잘못된 접근입니다'


@app.route('/board_detail/<num>')
def board_details(num):
    sql = "select * from board where num=%s"
    cur.execute(sql, num)
    data = cur.fetchall()
    print(data)
    views = "update board set views = views+1 where num = %s"
    cur.execute(views, num)
    db.commit()
    print(views)
    # 번호 제목 글쓴이 본사람수 글
    return render_template('board_detail.html', data=data)


@app.route('/board_delete/<num>')
def board_delete(num):
    sql = f"delete from board where num=%s"
    cur.execute(sql, num)
    db.commit()
    return redirect(location="/")


@app.route('/login')
def board_login():
    if (request.args.get("id")):
        print('asdfasdf')
        return render_template('login.html', data='check')
    else:
        return render_template('login.html')


@app.route('/logout')
def board_logout():
    session.pop('id', None)
    return redirect('/')


@app.route('/register_action', methods=['POST'])
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


@app.route('/register')
def board_register():
    if request.args.get('id'):
        return render_template('/register.html', data='id')
    elif request.args.get('email'):
        return render_template('/register.html', data='email')
    else:
        return render_template('/register.html')


@app.route('/login_action', methods=['POST', 'GET'])
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

@app.route('/CallBack')
def Naver_Login_CallBack():
    return

@app.route('/GoogleLogin/')
def Google_Login():
    return

@app.route('/GoogleLogin/redirect')
def Google_Login_Url():
    Google_code_Data = request.args

    data = {
        'code':Google_code_Data['code'],
        'client_id' : data_json['GoogleClientId'],
        'client_secret' : data_json['GoogleClientPw'],
        'redirect_uri' : 'http://localhost:5000/GoogleLogin/redirect',
        'grant_type' : 'authorization_code'
    }
    a = requests.put("https://www.googleapis.com/oauth2/v2/userinfo/",json=data)
    print(a)
    return a
# redirect('/GoogleLogin/oauth')
@app.route('/GoogleLogin/oauth')
def Google_Login_Oauth():
    Google_User_Data = request.args
    return Google_User_Data


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True)
