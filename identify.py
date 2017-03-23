 # -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import traceback
import sys
def identify(cardNumber,password):
    url = 'http://myold.seu.edu.cn/userPasswordValidate.portal'
    values = {
    'Login.Token1':'213142288',
    'Login.Token2':'neverororever1',
    'goto':'http://myold.seu.edu.cn:9080/loginSuccess.portal',
    'gotoOnFail':'http://myold.seu.edu.cn:9080/loginFailure.portal'
    }
    values['Login.Token1']=str(cardNumber)
    values['Login.Token2']=str(password)
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    try:
    	response = urllib2.urlopen(req,timeout=4)
    except:
    	return "timeout"
    the_page = response.read()
    if(the_page.find("Success")!=-1):
    	return  "success"
    else:
    	return  "fail"
print identify("213142288","neverorforever1")