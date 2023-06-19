class User_Data:
    def __init__(self):
        self.__Google_Data = dict
        self.__Naver_Data = dict
        print("초기화")

    @property
    def Google_GetData(self):
        print('게러')
        return self.__Google_Data

    @Google_GetData.setter
    def Google_SetData(self, gdata: dict):
        self.__Google_Data: dict = gdata
        print('세러')

    @property
    def Naver_GetData(self):
        print('게러')
        return self.__Naver_Data

    @Naver_GetData.setter
    def Naver_SetData(self, gdata: dict):
        self.__Naver_Data: dict = gdata
        print('세러')


user_data = User_Data()


def user_data_set_google(data):
    user_data.Google_SetData = data


def user_data_set_naver(data):
    user_data.Naver_SetData = data


def user_data_get_google():
    data = user_data.Google_GetData
    return data


def user_data_get_naver():
    data = user_data.Naver_GetData
    return data
