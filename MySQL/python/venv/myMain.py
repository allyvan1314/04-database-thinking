import pymysql.cursors
from myClass import alUser, MySQL_Connect
from myFunc import *

try:
    hp = Hompage()
    usrp = ""
    ch = ""
    while True:
        if hp == "S":
            res = SignIn()
            if res == 0:
                print "\n[-] Wrong username or password, try again!!\n"
                hp = Hompage()
            else:
                print "\n[+] Welcome to my chat!!\n"
                usrp = UserHomepage()
                while True:
                    if usrp == "F":
                        frName = raw_input("Enter your friend name: ")
                        ch = FindFriend(frName)
                        if ch == "S":
                            SendFrRq(frName)
                            usrp = UserHomepage()
                        elif ch == "C":
                            while True:
                                LoadOldMess(frName)
                                # ChatUsr(frName)
                    elif usrp == "R":
                        res1 = CheckNewFrRq()
                        if res1 == 1:
                            choiceFrRq()
                        else:
                            usrp = UserHomepage()
                    elif usrp == "M":
                        CheckNewMess()
                        usrp = UserHomepage()
                    elif usrp == "L":
                        ShowFrl()
                        usrp = UserHomepage()
                    elif usrp == "S":
                        SignOut()
                        hp = "E"
                        break
        elif hp == "R":
            Register()
            hp = Hompage()
        elif hp == "E":
            break
        else:
            hp = Hompage()


finally:
    print "------------------------Good bye!-------------------------"