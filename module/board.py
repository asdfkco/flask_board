import json
from urllib import request

from module import google_Login,naver_Login

from flask import Flask, render_template, request, redirect, session, make_response, url_for, Blueprint
import pymysql
import math

bp = Blueprint("board",__name__,url_prefix='/')

with open("./config/config.json", 'r') as file:
    data_json = json.load(file)

db = pymysql.connect(host=data_json["host"], user=data_json["user"], passwd=data_json["passwd"], db="free_board",
                     charset="utf8")
cur = db.cursor()

@bp.route('/')
def index():
    print(session.keys())
    return redirect(location="/1")


@bp.route('/<int:pages>')
def index_page(pages):
    print(session.values())
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


@bp.route('/write')
def write():
    return render_template('write.html')


@bp.route('/write_action')
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


@bp.route('/board_detail/<num>')
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


@bp.route('/board_delete/<num>')
def board_delete(num):
    sql = f"delete from board where num=%s"
    cur.execute(sql, num)
    db.commit()
    return redirect(location="/")


