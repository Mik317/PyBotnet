import sqlite3
import sys

#DBs' Variables
DB_PATH = "C:\\Users\\MIKI\\workspace1\\PythonProject\\PyBotnet\\Server\\DBs\\"
BOTS_DB = sqlite3.connect(DB_PATH+'bots.db')
CMDS_DB = sqlite3.connect(DB_PATH+'cmds.db')
CRED_DB = sqlite3.connect(DB_PATH+'creds.db')
BOTS_EXE = BOTS_DB.cursor()
CMDS_EXE = CMDS_DB.cursor()
CRED_EXE = CRED_DB.cursor()

if __name__ == "__main__":
    
    if sys.argv[1] == 'init':
        BOTS_EXE.execute('''CREATE TABLE IF NOT EXISTS Bots (User TEXT, Uname TEXT, Geo TEXT, IP TEXT, 
                            Lat TEXT, Long TEXT, Os TEXT, Key TEXT)''')
        CMDS_EXE.execute('CREATE TABLE IF NOT EXISTS CmdsIn (Key TEXT, Inp TEXT)')
        CMDS_EXE.execute('CREATE TABLE IF NOT EXISTS CmdsOut (Key TEXT, Out TEXT, Inp TEXT)')
        CRED_EXE.execute('CREATE TABLE IF NOT EXISTS Creds (Key TEXT, User TEXT, Pass TEXT, Url TEXT)')
        
    if sys.argv[1] == 'del':
        BOTS_EXE.execute('DROP TABLE IF EXISTS Bots')
        CMDS_EXE.execute('DROP TABLE IF EXISTS CmdsIn')
        CMDS_EXE.execute('DROP TABLE IF EXISTS CmdsOut')
        CRED_EXE.execute('DROP TABLE IF EXISTS Creds')
        
    if sys.argv[1] == 'view':
        print("\nBots: \n")
        print(BOTS_EXE.execute('SELECT * FROM Bots').fetchall())
        print("\nCmdsIn: \n")
        print(CMDS_EXE.execute('SELECT * FROM CmdsIn').fetchall())
        print("\nCmdsOut: \n")
        print(CMDS_EXE.execute('SELECT * FROM CmdsOut').fetchall())
        print('\nCreds: \n')
        print(CRED_EXE.execute('SELECT * FROM Creds').fetchall())
    
    if sys.argv[1] == 'help':
        print("\n\tDB Utility Tool")
        print("\t\tMade by Mik              Version Beta 1.0")
        print("\t\tThis simple tool permit do some simple things for manage the DBs:")
        print("\n\tUsage: py db.py <command>. Commands are: ")
        print("\t\thelp: show this help banner")
        print("\t\tview: se all the items in the DBs")
        print("\t\tdel: delete all the items and the tables of the DBs")
        print("\t\tinit: initialize all the DBs' tables")
    
    BOTS_DB.commit()
    CMDS_DB.commit()
    BOTS_DB.close()
    CMDS_DB.close()
    
        