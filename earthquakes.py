import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

DATABASE = '/tmp/earthquakes.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def show_map():
	d = request.args.get('bounds')
	print d
	if type(d) != "None":
		lat_min = d[0][0]
		long_min = d[0][1]
		lat_max = d[1][0]
		long_max = d[1][1]
	db = connect_db()
	earthquakes = db.execute('select * from earthquakes')
	return render_template('index.html', earthquakes=earthquakes)

if __name__ == '__main__':
    app.run()
