import sqlite3
import types
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
	bounds = request.args.get('bounds')
	if type(bounds) != types.NoneType:
		b = eval(bounds)
		lat_min = str(b[0][0])
		long_min = str(b[0][1])
		lat_max = str(b[1][0])
		long_max = str(b[1][1])
	else:
		lat_min = str(-90)
		long_min = str(-180)
		lat_max = str(90)
		long_max = str(180)

	db = connect_db()
	earthquakes_cursor = db.execute('select * from earthquakes where latitude between ' + lat_min + ' and ' + lat_max + ' and longitude between ' + long_min + ' and ' + long_max)
	earthquakes = earthquakes_cursor.fetchall()
	return render_template('index.html', earthquakes=earthquakes)

if __name__ == '__main__':
    app.run()
