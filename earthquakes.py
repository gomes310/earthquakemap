import sqlite3
import types
import pdb
from flask import Flask, request, render_template, json

DATABASE = '/tmp/earthquakes.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def query_db():
	lat_min = str(request.args.get('lat_min') or -90)
	lat_max = str(request.args.get('lat_max') or 90)
	long_min = str(request.args.get('long_min') or -180)
	long_max = str(request.args.get('long_max') or 180)

	db = connect_db()	
	req_string = 'select * from earthquakes where latitude between ' + lat_min + ' and ' + lat_max + ' and longitude between ' + long_min + ' and ' + long_max
	earthquakes_cursor = db.execute(req_string)
	return earthquakes_cursor.fetchall()

@app.route('/get_earthquakes')
def get_earthquakes():
	earthquakes = query_db()
	result = json.JSONEncoder().encode(earthquakes)
	print result
	return result

@app.route('/')
def index():
	earthquakes = query_db()
	return render_template('index.html', eqs=earthquakes)

if __name__ == '__main__':
    app.run()
