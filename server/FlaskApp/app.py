from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html',
							title = 'RFID Door Lock')
@app.route('/logs')
def logs():
	conn = sqlite3.connect('logs.db')
	curs = conn.cursor()
	data = curs.execute(''' SELECT * from USERS''')
	return render_template('logs.html'
							title = 'View Logs')

if __name__ == '__main__':
	app.run(debug=True)