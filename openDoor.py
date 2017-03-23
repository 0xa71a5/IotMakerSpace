 # -*- coding:utf-8 -*-
import thread
import os
import sys
import json
import time
import tornado.httpserver
import tornado.web
import tornado.ioloop
import thread
from tornado import websocket
import random
import uuid
import sys
import serial
import string
import SendMail
import identify
import Students
reload(sys)
sys.setdefaultencoding('utf-8')
log=open("log.txt","a")
listenPort=80


try:
    uno=serial.Serial("/dev/ttyUSB0",115200)
    pass
except Exception as e:
    print e 
    uno=serial.Serial("/dev/ttyUSB1",115200)

todayPassword="S4(mAVdR3yX2ptw"
rootPassword="12345k"

def notify():
    global notifyNeededName
    SendMail.SendMail("497425817@qq.com","Inform","门被"+notifyNeededName+"打开")
    print "SendMail"

def getRandomPassword():
    baseStr='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()0123456789'
    password=string.join(random.sample(baseStr,15)).replace(' ','')
    return password

def arduinoOpenDoor():
    global uno
    try:
        uno.write("k")
    except Exception as e:
        print e
        print "open error"
        uno=serial.Serial("/dev/ttyUSB1",19200)
        uno.write("k")
    thread.start_new_thread(notify,())
    return 'k'



def arduinoCloseDoor():
    global uno
    try:
        uno.write("g")
    except Exception as e:
        print e
        print "close error"
        uno=serial.Serial("/dev/ttyUSB0",115200)
        uno.write("g")
    return 'g'


def remoteOpen(order):
    print "Send command to locker..."
    data='f'
    if(order==1):
        data=arduinoOpenDoor()
    else:
        data=arduinoCloseDoor()
    if(order==1):
        return 1
    elif(order==2):
        return 3
    else:
       return 2

def timeCompare(t):
    try:
        settingTime=time.mktime(time.strptime(t+" 23:59:59","%Y/%m/%d %H:%M:%S"))
        currentTime=time.time()+3600*8
        if(settingTime<currentTime):return False
        else:return True
    except:
        return False

class OpenDoorIndex(tornado.web.RequestHandler):
    def get(self):
        loginState=self.get_secure_cookie("token")
        cardNumber=self.get_secure_cookie("cardNumber")
        username=self.get_secure_cookie("userName")
        if(loginState=="logined"):
            identification=Students.getIdentification(cardNumber)
            authority=Students.getAuthority(cardNumber)
            authorityContinous=Students.getAuthorityContinous(cardNumber)
            opStatus=""
            self.render('openDoor.html',username=username,identification=identification,authority=authority,authorityContinous=authorityContinous,opStatus=opStatus)
        else:
            self.render('login.html',success=False)

    def post(self):
        global notifyNeededName
        username=self.get_secure_cookie("userName")
        cardNumber=self.get_secure_cookie("cardNumber")
        identification=Students.getIdentification(cardNumber)
        authority=Students.getAuthority(cardNumber)
        authorityContinous=Students.getAuthorityContinous(cardNumber)
        timeStamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()+3600*8))
        if(timeCompare(authorityContinous)):
            opStatus="开门成功"
            notifyNeededName=username
            log.write("["+timeStamp+"]"+self.request.remote_ip+" opendoor->"+" Card:"+cardNumber+" Name:"+username+" Result:Success\n")
            log.flush()
            remoteOpen(1)
        else:
            log.write("["+timeStamp+"]"+self.request.remote_ip+" opendoor->"+" Card:"+cardNumber+" Name:"+username+" Result:Fail\n")
            log.flush()
            opStatus="无权限开门"
        self.render('openDoor.html',username=username,identification=identification,authority=authority,authorityContinous=authorityContinous,opStatus=opStatus)

class LoginIndex(tornado.web.RequestHandler):
    def get(self):
        loginState=self.get_secure_cookie("token")
        cardNumber=self.get_secure_cookie("cardNumber")
        username=self.get_secure_cookie("userName")
        if(loginState=="logined"):
            identification=Students.getIdentification(cardNumber)
            authority=Students.getAuthority(cardNumber)
            authorityContinous=Students.getAuthorityContinous(cardNumber)
            opStatus=""
            self.render('openDoor.html',username=username,identification=identification,authority=authority,authorityContinous=authorityContinous,opStatus=opStatus)
        else:
            self.render('login.html',success=False)
    def post(self):
        loginState=self.get_secure_cookie("token")
        cardNumber=self.get_secure_cookie("cardNumber")
        username=self.get_secure_cookie("userName")
        if(loginState=="logined"):
            identification=Students.getIdentification(cardNumber)
            authority=Students.getAuthority(cardNumber)
            authorityContinous=Students.getAuthorityContinous(cardNumber)
            opStatus=""
            self.render('openDoor.html',username=username,identification=identification,authority=authority,authorityContinous=authorityContinous,opStatus=opStatus)
        else:
            cardNumber=self.get_argument('CardNumber')
            password=self.get_argument('CardPassword')
            print cardNumber,password
            identifyStatus=identify.identify(cardNumber,password)
            if(identifyStatus=="success"):
                self.set_secure_cookie("token","logined")
                self.set_secure_cookie("cardNumber",cardNumber)
                username=Students.getUsername(cardNumber)
                self.set_secure_cookie("userName",username)
                identification=Students.getIdentification(cardNumber)
                authority=Students.getAuthority(cardNumber)
                authorityContinous=Students.getAuthorityContinous(cardNumber)
                timeStamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()+3600*8))
                log.write("["+timeStamp+"]"+self.request.remote_ip+" login->"+" Card:"+cardNumber+" Name:"+username+"\n")
                log.flush()
                opStatus=""
                self.render('openDoor.html',username=username,identification=identification,authority=authority,authorityContinous=authorityContinous,opStatus=opStatus)
            else:
                self.render('login.html',success=False)

class Index(tornado.web.RequestHandler):
    def get(self):
        loginState=self.get_secure_cookie("token")
        cardNumber=self.get_secure_cookie("cardNumber")
        username=self.get_secure_cookie("userName")
        if(loginState=="logined"):
            identification=Students.getIdentification(cardNumber)
            authority=Students.getAuthority(cardNumber)
            authorityContinous=Students.getAuthorityContinous(cardNumber)
            opStatus=""
            self.render('openDoor.html',username=username,identification=identification,authority=authority,authorityContinous=authorityContinous,opStatus=opStatus)
        else:
            self.render('login.html',success=True)
    def post(self):
        self.render('login.html',success=True)

class AdminIndex(tornado.web.RequestHandler):
    def get(self):
        loginState=self.get_secure_cookie("token")
        cardNumber=self.get_secure_cookie("cardNumber")
        username=self.get_secure_cookie("userName")
        if(cardNumber=="213142288"):
            self.render('admin.html',showInfo="")
        else:
            self.render('login.html',success=True)
    def post(self):
        cardNumber=self.get_secure_cookie("cardNumber")
        if(cardNumber=="213142288"):
            upname=self.get_argument('upname')
            upcardnumber=self.get_argument('upyicardnumber')
            upidentification=self.get_argument('upidentification')
            upauthority=self.get_argument('upauthority')
            upbegindate=self.get_argument('upbegindate')
            if(len(upname)!=0 and len(upcardnumber)==0):
                ret=Students.getInfo(upname)
                self.render('admin.html',showInfo=ret)
            elif(len(upcardnumber)!=0):
                print upcardnumber,upbegindate
                Students.update(upcardnumber,upidentification,upauthority,upbegindate)
                self.render('admin.html',showInfo="success updated")
            else:
                self.render('admin.html',showInfo="")
        else:
            self.render('login.html',success=True)

class LogIndex(tornado.web.RequestHandler):
    def get(self):
        loginState=self.get_secure_cookie("token")
        cardNumber=self.get_secure_cookie("cardNumber")
        username=self.get_secure_cookie("userName")
        if(loginState=="logined" and cardNumber=="213142288"):
            f=open("log.txt","r")
            cont=f.read()
            cont=cont.replace("\n","<br>")
            self.write(cont)
            f.close()
        else:
            self.write("No permission!")

if __name__ == '__main__':
    app = tornado.web.Application([
        ('/', Index),
	('/login',LoginIndex),
	('/openDoor',OpenDoorIndex),
    ('/admin',AdminIndex),
    ('/log',LogIndex)
    ],cookie_secret='abcdswweww2!!wsws2',
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    print "Running"
    Students.init()
    app.listen(listenPort)
    tornado.ioloop.IOLoop.instance().start()









