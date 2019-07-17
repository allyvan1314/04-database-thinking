import pymysql.cursors
from myClass import alUser, MySQL_Connect
from myFunc import Hompage, SignIn, checkUsrName, Register, CheckRela, UpdateStt, UserHomepage, GetUserInfor, FindFriend
from myFunc import AcceptFrRq, SendFrRq, RejectFrRq, CheckNewFrRq

try:
    hp = Hompage()
    usrp = ""
    ch = ""
    while True:
        if hp == "S":
            res = SignIn()
            if res == 0:
                print "[-] Wrong username or password, try again!!"
                hp = Hompage()
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
                    elif usrp == "L":
                        CheckNewFrRq()
                        usrp = UserHomepage()
        elif hp == "R":
            Register()
            hp = Hompage()
        elif hp == "E":
            break
        else:
            hp = Hompage()


finally:
    print "------------------------Good bye!-------------------------"