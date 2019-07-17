import pymysql.cursors
from myClass import alUser, MySQL_Connect
from myFunc import Hompage, SignIn, checkUsrName, Register, CheckRela, UpdateStt, UserHomepage, GetUserInfor, FindFriend, SendFrRq


alUsr = alUser("", "", "", "", "", "")
conn = MySQL_Connect("localhost", "admin", "13081410", "MYCHAT")
conn.connect()


try:
    hp = Hompage()
    usrp = ""
    ch = ""
    while True:
        if hp == "S":
            res = SignIn()
            if res == 0:
                print "[-] Wrong username or password, try again!!"
            else:
                print "[+] Welcome to my chat!!"
                usrp = UserHomepage()
                while True:
                    if usrp == "F":
                        frName = raw_input("Enter your friend name: ")
                        ch = FindFriend(frName)
                        if ch == "S":
                            SendFrRq(frName)
                            usrp = UserHomepage()
        elif hp == "R":
            Register()
            hp = Hompage()
        elif hp == "E":
            break
        else:
            hp = Hompage()


finally:
    conn.close()
    print "------------------------Good bye!-------------------------"