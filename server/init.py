from flask import Flask, render_template, redirect, url_for, request
import sqlite3, os
dbDir = os.path.join(os.path.dirname(__file__), "../resources/main.db")
app = Flask(__name__)

'''@app.route('/')
def index():
	if 'username' in session:
    	return redirect(url_for('home'))
	else
		return redirect(url_for('login'))
'''
@app.route('/')
def home():
	return render_template('index.html', title = 'RFID Door Lock')

@app.route('/logs')
def logs():
	conn = sqlite3.connect(dbDir)
	conn.text_factory = str
	curs = conn.cursor()
	uids = curs.execute("SELECT UID FROM LOGS").fetchall()
	times = curs.execute("SELECT TIME FROM LOGS").fetchall()
	success = curs.execute("SELECT SUCCESS FROM LOGS").fetchall()
	listLen = len(uids)
	return render_template('logs.html', title = 'View Logs', uids = uids, times = times, success = success, listLen = listLen)

'''@app.route('/login')
def login():
	password = request.form['login']
	if password = 'admin'



@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))
'''
if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")
