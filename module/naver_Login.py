import json
from urllib import request

import requests
from flask import Flask, render_template, request, redirect, session, make_response, url_for, Blueprint


from .userDAO import user_data_get_naver, user_data_set_naver


bp = Blueprint("NaverLogin", __name__, url_prefix='/NaverLogin')

with open("./config/config.json", 'r') as file:
    data_json = json.load(file)



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
        session['token'] = a
    except:
        return '400 bad request'
    print(a)
    return redirect(url_for('NaverLogin.Naver_Login_Oauth', data=a))


@bp.route('/oauth')
def Naver_Login_Oauth():
    token = request.args.get('data')
    Naver_User_Data = requests.get(f'https://openapi.naver.com/v1/nid/me',headers={"Authorization" : f"Bearer {token}"})
    Naver_User_Data = Naver_User_Data.json()
    print(Naver_User_Data)
    user_data_set_naver(Naver_User_Data)
    return redirect(url_for('user.board_login_action', social='naver'))


@bp.route('/logout')
def logout():
    print("session : ",session.keys())
    requests.post(f'https://nid.naver.com/oauth2.0/token?grant_type=delete&client_id={data_json["NaverClientId"]}&client_secret={data_json["NaverClientPw"]}&access_token={session["token"]}&service_provider=NAVER')
    session.pop('token',None)
    return redirect('/')

def Naver_user_data_getter():
    data = user_data_get_naver()
    return data