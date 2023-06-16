class User_Data:

    def __init__(self):
        self.__Google_Data = ''
    @property
    def Google_GetData(self):
        return self.__Google_Data

    @Google_GetData.setter
    def Google_SetData(self,gdata):
        print(type(gdata))
        self.__Google_Data = gdata

@bp.route('/oauth')
def Google_Login_Oauth():
    token = request.args.get('data')
    Google_User_Data = requests.get(f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={token}')
    Google_User_Data_Set = Google_User_Data
    call_data = User_Data()
    call_data.Google_SetData(Google_User_Data_Set.text)
    return redirect(url_for('user.board_login_action', social='Google'))



@bp.route('/login_action', methods=['POST', 'GET'])
def board_login_action():
    if request.method == 'POST':
        form_id = request.form.get('id')
        form_passwd = request.form.get('password')
        sql = "select * from users where id = %s and password = %s"
        print(sql,(form_id,form_passwd))
        database.cur.execute(sql,(form_id,form_passwd))
        data = database.cur.fetchall()
        if len(data) == 1:
            print(data)
            session["id"] = form_id
            return redirect("/")
        else:
            return redirect(url_for('user.board_login', id="fail"))
    elif request.method == 'GET':
        social = request.args.get('social')
        sql = 'select * from users where social = %s and email = %s'
        user_data = User_Data()
        data = user_data.Google_GetData
        print('값 : ㅋㅋ',data)
        # database.cur.execute(sql,(social,user_data.Google_GetData))
        return redirect("/")