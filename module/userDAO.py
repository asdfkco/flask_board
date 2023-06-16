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