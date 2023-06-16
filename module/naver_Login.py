import json
from urllib import request

import requests
from flask import Flask, render_template, request, redirect, session, make_response, url_for, Blueprint
import pymysql
import math

bp = Blueprint("NaverLogin", __name__, url_prefix='/NaverLogin')

with open("./config/config.json", 'r') as file:
    data_json = json.load(file)

Naver_User_Data = ""

@bp.route('/')
def Naver_Login():
    return redirect(
        f'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={data_json["NaverClientId"]}&redirect_url=http://localhost:5000/NaverLogin/redirect&state=board')


@bp.route('/redirect')
def Naver_Login_Url():
    Naver_code_Data = request.args
    print(Naver_code_Data)
    a = requests.post(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={data_json['NaverClientId']}&client_secret={data_json['NaverClientPw']}&code={Naver_code_Data['code']}&state=board")
    print(a.text)
    try:
        a = a.json()['access_token']
    except:
        return '400 bad request'
    print(a)
    return redirect(url_for('NaverLogin.Naver_Login_Oauth', data=a))


@bp.route('/oauth')
def Naver_Login_Oauth():
    token = request.args.get('data')
    Naver_User_Data = requests.get(f'https://openapi.naver.com/v1/nid/me',headers={"Authorization" : f"Bearer {token}"})
    Naver_User_Data = Naver_User_Data.json()
    return redirect(url_for('user.board_login_action', social='Naver'))


@bp.route('/logout')
def logout():
    requests.post('https://nid.naver.com/oauth2.0/token?grant_type=delete&client_id=jyvqXeaVOVmV&client_secret=527300A0_COq1_XV33cf&access_token=c8ceMEJisO4Se7uGCEYKK1p52L93bHXLnaoETis9YzjfnorlQwEisqemfpKHUq2gY&service_provider=NAVER')
    return redirect('/')


def Naver_getData():
    return Naver_User_Data