import json,os

import pymysql

with open("./config/config.json", 'r') as file:
    data_json = json.load(file)

db = None

if "home" in os.getcwd():
    db = pymysql.connect(host=data_json["hostaws"], user=data_json["user"], passwd=data_json["passwdaws"], db="free_board",
                     charset="utf8")
else:
    print(os.getcwd())
    db = pymysql.connect(host=data_json["host"], user=data_json["user"], passwd=data_json["passwd"], db="free_board",
                     charset="utf8")
cur = db.cursor()

