import json
from urllib import request

import requests
from flask import Flask, render_template, request, redirect, session, make_response, url_for, Blueprint
import pymysql
import math

bp = Blueprint("GoogleLogin",__name__,url_prefix='/GoogleLogin')

with open("./config/config.json", 'r') as file:
    data_json = json.load(file)

@bp.route('/')
def Google_Login():
    return redirect(
        f'https://accounts.google.com/o/oauth2/v2/auth?client_id={data_json["GoogleClientId"]}&redirect_uri=http://localhost:5000/GoogleLogin/redirect&scope=email profile&response_type=code')


@bp.route('/redirect')
def Google_Login_Url():
    Google_code_Data = request.args
    a = requests.post(
        f"https://oauth2.googleapis.com/token?code={Google_code_Data['code']}&client_id={data_json['GoogleClientId']}&client_secret={data_json['GoogleClientPw']}&redirect_uri=http://localhost:5000/GoogleLogin/redirect&grant_type=authorization_code")
    try:
        a = a.json()['access_token']
    except:
        return '400 bad request'
    print(a)
    return redirect(url_for('GoogleLogin.Google_Login_Oauth', data=a))


@bp.route('/oauth')
def Google_Login_Oauth():
    token = request.args.get('data')
    Google_User_Data = requests.get(f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={token}')
    Google_User_Data = Google_User_Data.json()
    return Google_User_Data