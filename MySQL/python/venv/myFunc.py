import pymysql.cursors


# function show home page
def Hompage():
    print "--------------------Welcome to My chat--------------------"
    print "Which option do you want?\t[S]ign in\t[R]egister\t[E]xit"
    x = raw_input("Your choice: ").upper()
    if x not in "SRE" or len(x) != 1:
        print "[-] I don't know how to do that!!"
    else:
        return x


# function sign in
def SignIn():
    cursor = conn.connection.cursor()
    usrName = raw_input("___User name\t\t___: ")
    usrPass = raw_input("___Password\t\t\t___: ")
    res = 0
    inOutParams = (usrName, usrPass, res)
    cursor.callproc("SIGN_IN_WRAP", inOutParams)
    for row in cursor:
        res = row['res']

    if res == 1:
        UpdateStt(usrName, 'online')
        GetUserInfor(usrName, usrPass)

    return res


# function check user name exists or not
def checkUsrName(usrName):
    res = 0
    cursor = conn.connection.cursor()
    inOutParams = (usrName, res)
    cursor.callproc("CHECK_USRNAME_WRAP", inOutParams)
    for row in cursor:
        res = row['res']

    return res


# function register
def Register():
    cursor = conn.connection.cursor()
    userName = raw_input("___Sign in name*\t\t___: ")
    while len(userName) < 1:
        print "Sign in name cannot be blank!"
        userName = raw_input("___Sign in name*\t\t___: ")

    res = checkUsrName(userName)
    while res == 1:
        print "User name is already exists, please try again!"
        userName = raw_input("___Sign in name*\t\t___: ")
        res = checkUsrName(userName)

    userPass = raw_input("___Password*\t\t\t___: ")
    while len(userPass) < 1:
        print "Password cannot be blank!"
        userPass = raw_input("___Password*\t\t\t___: ")

    alName = raw_input("___Your name*\t\t\t___: ")
    while len(alName) < 1:
        print "Your name cannot be blank!"
        alName = raw_input("___Your name*\t\t\t___: ")

    alEmail = raw_input("___Your email\t\t\t___: ")
    alPhone = raw_input("___Your phone number\t___: ")
    alStt = "offline"
    inOutParams = (userName, userPass, alName, alEmail, alPhone, alStt)
    cursor.callproc("CREATE_ACC", inOutParams)
    conn.connection.commit()
    print "[+] ----------------Register successful!------------------"


# function update status for user
def UpdateStt (usrName, stt):
    cursor = conn.connection.cursor()
    inOutParams = (usrName, stt)
    cursor.callproc("UPDATE_STT", inOutParams)
    conn.connection.commit()


def GetUserInfor(usrName, usrPass):
    alName = ""
    alEmail = ""
    alPhone = ""
    alStt = ""
    alUsr.userName = usrName
    alUsr.userPass = usrPass
    cursor = conn.connection.cursor()
    inOutParams = (usrName, alName, alEmail, alPhone, alStt)
    cursor.callproc("GET_USR_INFOR", inOutParams)
    for row in cursor:
        alUsr.alName = row['alName']
        alUsr.alEmail = row['alEmail']
        alUsr.alPhone = row['alPhone']
        alUsr.alStt = row['alStt']


def UserHomepage():
    print "--------------------Welcome,", alUsr.alName, "--------------------"
    print "Which option do you want?\tFind [F]riend\tFind [G]roup\t[S]ign out"
    choice = raw_input("Your choice: ").upper()
    if choice not in "FGS" or len(choice) != 1:
        print "[-] I don't know how to do that!!"
    else:
        return choice


def CheckRela(frName):
    cursor = conn.connection.cursor()
    res = 0
    inOutParams = (alUsr.userName, frName, res)
    cursor.callproc("CHECK_RELA", inOutParams)
    for row in cursor:
        res = row['res']

    return res


def FindFriend(frName):
    res = checkUsrName(frName)
    ch = ""
    if res == 1:
        res2 = CheckRela(frName)
        if res2 == 1:
            print "[+]", frName, " is your friend, do you want:\t[C]hat\t[E]xit"
            ch = raw_input("Your choice: ").upper()
            if ch not in "CE" or len(ch) != 1:
                print "[-] I don't know how to do that!!"
            else:
                return ch
        else:
            print "[+]", frName, " is not your friend, do you want:\t[S]end friend request\t[E]xit"
            ch = raw_input("Your choice: ").upper()
            if ch not in "SE" or len(ch) != 1:
                print "[-] I don't know how to do that!!"
            else:
                return ch
    else:
        print "[-]", frName, " is not exists, please try again!!"
        return "F"


def SendFrRq(frName):
    mess = raw_input("Send friend request with a message: ")
    cursor = conn.connection.cursor()
    inOutParams = (alUsr.userName, frName, mess)
    cursor.callproc("SEND_FRRQ", inOutParams)
    cursor.connection.commit()
    print "Friend request to ", frName, "successful!"