import sqlite3
conn = sqlite3.connect("main.db")
curs = conn.cursor()
return curs
