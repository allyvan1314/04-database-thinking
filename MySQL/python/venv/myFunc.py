import pymysql.cursors
from myClass import alUser, MySQL_Connect

alUsr = alUser("", "", "", "", "", "")
conn = MySQL_Connect("localhost", "admin", "13081410", "MYCHAT")
conn.connect()


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
    print "Which option do you want?\nFind [F]riend\t\t\tFind [G]roup\t\t\t[S]ign out"
    print "See [L]ist friend\t\tCheck new [M]essage\t\tCheck new friend [R]equest"
    choice = raw_input("Your choice: ").upper()
    if choice not in "FGSLMR" or len(choice) != 1:
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
    print "[+] Send friend request to", frName, "successful!"


def AcceptFrRq(frName):
    cursor = conn.connection.cursor()
    inOutParams = (frName, alUsr.userName)
    cursor.callproc("ACCEPT_FRRQ", inOutParams)
    cursor.connection.commit()
    inOutParams = (frName, alUsr.userName, "accept")
    cursor.callproc("UPDATE_FRRQ", inOutParams)
    cursor.connection.commit()
    print "[+] Accept successful!"


def RejectFrRq(frName):
    cursor = conn.connection.cursor()
    inOutParams = (frName, alUsr.userName, "reject")
    cursor.callproc("UPDATE_FRRQ", inOutParams)
    cursor.connection.commit()
    print "[+] Reject successful!"


def CheckNewFrRq():
    cursor = conn.connection.cursor()
    res = 0
    inOutParams = (alUsr.userName, res)
    cursor.callproc("SHOW_FRRQ", inOutParams)
    for row in cursor:
        if row['AL_RQID'] is None:
            print "[-] No friend request!"
            res = 0
            break
        else:
            print "Id: ", row['AL_RQID'], "From: ", row['AL_USERNAME'], "Message: ", row['AL_CONTENT'], "Date: ", row['AL_DATE_CREATE']
            res = 1

    return res


def choiceFrRq():
    print "Do you want:\t[A]ccept friend request\t[R]eject friend request"
    frrq = raw_input("Your choice: ").upper()
    if frrq == "A":
        frName = raw_input("Your friend's name: ")
        AcceptFrRq(frName)
    elif frrq == "R":
        frName = raw_input("Your friend's name: ")
        RejectFrRq(frName)
    else:
        print "[-] I don't khow how to do that!"


def ChatUsr(frName):
    cursor = conn.connection.cursor()
    mess = raw_input("\rMess: ")
    inOutParams = (alUsr.userName, frName, mess)
    cursor.callproc("CHAT_USR", inOutParams)
    cursor.connection.commit()


def LoadOldMess(frName):
    cursor = conn.connection.cursor()
    inPutParams = (alUsr.userName, frName)
    cursor.callproc("LOAD_OLD_MSR", inPutParams)
    cursor.connection.commit()
    for row in cursor:
        print "\r", row['AL_USERNAME'], "[", row['AL_DATE'], "]:", row['AL_CONTENT']


def CheckNewMess():
    cursor = conn.connection.cursor()
    res = 0
    inOutParams = (alUsr.userName, res)
    cursor.callproc("CHECK_NEWMSG", inOutParams)
    cursor.connection.commit()
    for row in cursor:
        print "\r", row['AL_USERNAME'], "[", row['AL_DATE'], "]:", row['AL_CONTENT']


def ShowFrl():
    cursor = conn.connection.cursor()
    res = 0
    inOutParams = (alUsr.userName, res)
    cursor.callproc("SHOW_FRL", inOutParams)
    for row in cursor:
        print "UsrName:", row['AL_USERNAME'], "\tName:", row['AL_NAME'], "\tStatus:", row['AL_STATUS']


def SignOut():
    cursor = conn.connection.cursor()
    inPutParams = (alUsr.userName, 'offline')
    cursor.callproc("UPDATE_STT", inPutParams)
    cursor.connection.commit()
    print "[+] Sign out successful!"
