import json

import pymysql

with open("./config/config.json", 'r') as file:
    data_json = json.load(file)

db = pymysql.connect(host=data_json["host"], user=data_json["user"], passwd=data_json["passwd"], db="free_board",
                     charset="utf8")
cur = db.cursor()

