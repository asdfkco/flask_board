import json
from urllib import request

from .db import database

from module import google_Login,naver_Login

from flask import Flask, render_template, request, redirect, session, make_response, url_for, Blueprint
import pymysql
import math

bp = Blueprint("board",__name__,url_prefix='/')

with open("./config/config.json", 'r') as file:
    data_json = json.load(file)


@bp.route('/')
def index():
    print(session.keys())
    return redirect(location="/1")


@bp.route('/<int:pages>')
def index_page(pages):
    print(session.values())
    sql = f"select * from board where num between {((pages - 1) * 15) + 1 if ((pages - 1) * 15) > 1 else (pages - 1) * 15} and {pages * 15}"
    total_pages = database.cur.execute("select * from board order by num")
    count = (math.trunc(total_pages / 10) + 1)
    print("sql : ", sql)
    database.cur.execute(sql)
    data_list = database.cur.fetchall()
    print(data_list)
    print("maxPage : ", count)
    if 'id' not in session or session["id"] == "":
        return render_template('index.html', data_list=data_list, page=count)
    else:
        return render_template('index.html', data_list=data_list, page=count, session=True)


@bp.route('/write')
def write():
    return render_template('write.html')


@bp.route('/write_action',methods=['POST'])
def write_action():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        sql = "insert into board (title,writer,content,views) values (%s,%s,%s,0);"

        values = (title, session['id'], content)
        print(sql, values)
        database.cur.execute(sql, values)
        database.db.commit()
        return redirect(location="/")
    else:
        return '잘못된 접근입니다'


@bp.route('/board_detail/<num>')
def board_details(num):
    sql = "select * from board where num=%s"
    database.cur.execute(sql, num)
    data = database.cur.fetchall()
    print(data)

    views = "update board set views = views+1 where num = %s"
    database.cur.execute(views, num)
    database.db.commit()
    print(views)

    try:
        sql = "select writer from board where writer=%s"
        database.cur.execute(sql, session['id'])
        a = database.cur.fetchall()
        print(len(a))
        if len(a) != 0:
            return render_template('board_detail.html', data=data,update='update')
    except:
        print('비로그인 세션')
    # 번호 제목 글쓴이 본사람수 글
    return render_template('board_detail.html', data=data)


@bp.route('/board_delete/<num>')
def board_delete(num):
    sql = f"delete from board where num=%s"
    database.cur.execute(sql, num)
    database.db.commit()
    return redirect(location="/")

@bp.route('/board_update/<num>')
def board_update(num):
    return render_template('board_update.html',num=num)

@bp.route('/board_update_action/<num>',methods=['POST'])
def board_update_action(num):
    form_title = request.form.get('title')
    form_centent = request.form.get('content')
    sql = "update board set title = %s,content = %s where num = %s"
    database.cur.execute(sql,(form_title,form_centent,num))
    return redirect('/')
