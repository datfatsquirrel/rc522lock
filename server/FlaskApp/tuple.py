from flask import Flask, render_template
import sqlite3
def logs():
        conn = sqlite3.connect('data.db')
        conn.text_factory = str
        curs = conn.cursor()
        uids = curs.execute(''' SELECT uid from logs''').fetchall()
        times = curs.execute(''' SELECT time from logs''').fetchall()
        uids = list(uids)
        times = list(times)
        print(type(uids))

logs()
