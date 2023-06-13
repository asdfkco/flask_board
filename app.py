import json
from flask import Flask, render_template, request, redirect
import pymysql
import math

with open("./db.json",'r') as file:
    data = json.load(file)

db = pymysql.connect(host=data["host"],user=data["user"],passwd=data["passwd"],db="free_board",charset="utf8")
cur = db.cursor()




app = Flask(__name__)

@app.route('/')
def index():
    return redirect(location="/1")

@app.route('/<int:pages>')
def index_page(pages):
    sql = f"select * from board where num between {((pages-1)*15)+1  if ((pages-1)*15) > 1 else (pages-1)*15} and {pages*15}"
    total_pages = cur.execute("select * from board order by num")
    count = (math.trunc(total_pages/10)+1)
    print(sql)
    cur.execute(sql)
    data_list = cur.fetchall()
    print(data_list)
    print(count)
    return render_template('index.html' ,data_list=data_list,page=count)

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/write_action',methods=['POST'])
def write_action():
    title = request.form.get('title')
    writer = request.form.get('writer')
    content = request.form.get('content')

    sql = "insert into board (title,writer,content,views) values (%s,%s,%s,0);"

    values = (title,writer,content)
    print(sql,values)
    cur.execute(sql,values)
    db.commit()
    return redirect(location="/")

@app.route('/board_detail/<num>')
def board_details(num):
    sql = "select * from board where num=%s"
    cur.execute(sql, num)
    data = cur.fetchall()
    print(data)
    views = "update board set views = views+1 where num = %s"
    cur.execute(views,num)
    db.commit()
    print(views)
    # 번호 제목 글쓴이 본사람수 글
    return render_template('board_detail.html',data=data)

@app.route('/board_delete/<num>')
def board_delete(num):
    sql = f"delete from board where num=%s"
    cur.execute(sql, num)
    db.commit()
    return redirect(location="/")

if __name__ == '__main__':
    app.run(debug=True)