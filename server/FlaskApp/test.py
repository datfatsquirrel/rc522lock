import sqlite3
def main():
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    uid = curs.execute('SELECT uid FROM logs')
    print uid.fetchall()
    conn.close()

def create():
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    curs.execute('''CREATE TABLE logs (uid text, time text)''')
    curs.execute("INSERT INTO logs VALUES ('8938', '24-07-1999')")
    curs.execute("INSERT INTO logs VALUES ('1236', '15-02-2014')")
    curs.execute("INSERT INTO logs VALUES ('8938', '09-11-1936')")
    conn.commit()
    
main()
