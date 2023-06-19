import json
from urllib import request

from module import google_Login,naver_Login,user,board

from flask import Flask, render_template, request, redirect, session, make_response, url_for
import pymysql
import math



app = Flask(__name__)
app.secret_key = "ex_id"


app.register_blueprint(google_Login.bp)
app.register_blueprint(naver_Login.bp)
app.register_blueprint(user.bp)
app.register_blueprint(board.bp)








if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True, port=5000)

# data = {
#     'code':Google_code_Data['code'],
#     'client_id' : data_json['GoogleClientId'],
#     'client_secret' : data_json['GoogleClientPw'],
#     'redirect_uri' : 'http://localhost:5000/GoogleLogin/redirect',
#     'grant_type' : 'authorization_code'
# }
