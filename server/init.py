from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', title = 'RFID Door Lock')

@app.route('/logs')
def logs():
	conn = sqlite3.connect('main.db')
	conn.text_factory = str
	curs = conn.cursor()
	uids = curs.execute(''' SELECT UID FROM LOGS''').fetchall()
	times = curs.execute(''' SELECT TIME FROM LOGS''').fetchall()
	listLen = len(uids)
	return render_template('logs.html', title = 'View Logs', uids = uids, times = times, listLen = listLen)

if __name__ == '__main__':
	app.run(debug=True)
