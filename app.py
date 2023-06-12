from flask import Flask, render_template, request, redirect
import pymysql

db = pymysql.connect(host="localhost",user="root",passwd="1234",db="free_board",charset="utf8")
cur = db.cursor()




app = Flask(__name__)

@app.route('/')
def index():
    sql = "select * from board"
    cur.execute(sql)

    data_list = cur.fetchall()
    print(data_list)

    return render_template('index.html' ,data_list=data_list)

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
    cur.execute(sql,values)
    db.commit()

    print(sql,values)
    return redirect(location="/")

@app.route('/board/<num>')
def board_details(num):
    sql = f"select * from board where num={num}"
    cur.execute(sql)
    data = cur.fetchall()


    return render_template('board_detail.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)