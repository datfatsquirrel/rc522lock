import sqlite3
def main():
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    data = curs.execute('SELECT * FROM logs')
    print (data)
    conn.close()
main()
