import sqlite3, os

databasePath = os.path.join(os.path.dirname(__file__), "../resources/userDB.db")

def createDatabase():
   conn = sqlite3.connect(databasePath)
   print ("Opened database successfully")

   conn.execute('''CREATE TABLE USERS
         (ID INT PRIMARY KEY     NOT NULL);''')
   print ("Table created successfully")
   conn.close()

def insertValues():
   conn = sqlite3.connect(databasePath)
   print ("Opened database successfully")
   curs = conn.cursor()

   curs.execute("INSERT INTO USERS (ID) VALUES (7660887599)")
   conn.commit()

def query():
   conn = sqlite3.connect(databasePath)
   print ("Opened database successfully")
   curs = conn.cursor()
   uidStr = "543253215"
   returnValue = curs.execute("SELECT id from USERS where id = "+uidStr).fetchone()
   if returnValue is not None:
      print int(returnValue)
   else:
      print "We got nufink"
   conn.close()

insertValues()
