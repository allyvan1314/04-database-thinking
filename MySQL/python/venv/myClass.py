import pymysql.cursors


# class user
class alUser:
    def __init__(self, usrName, usrPass, alName, alEmail, alPhone, alStt):
        self.userName = usrName
        self.userPass = usrPass
        self.alName = alName
        self.alEmail = alEmail
        self.alPhone = alPhone
        self.alStt = alStt


# class connect to mySQL
class MySQL_Connect:

    def __init__(self, host, usr, password, db):
        self.host = host
        self.user = usr
        self.password = password
        self.db = db

    def connect(self):
        self.connection = pymysql.connect(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          db=self.db,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        print "Connect successful!!"

    def close(self):
        self.connection.close()