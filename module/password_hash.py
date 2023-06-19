import bcrypt


class Hashed:

    def __init__(self):
        self.__hashed_pw = ""

    def hash_pw(self, pw):
        self.__hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
        return self.__hashed_pw

    def hasing_pw(self, pw):
        print(self.__hashed_pw)
        return bcrypt.checkpw(pw, self.__hashed_pw)
