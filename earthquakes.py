import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from data_handler import parse_data, draw_beachballs, add_db_records

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
	db = connect_db()
	earthquakes = db.execute('select * from earthquakes')
	return render_template('index.html', earthquakes=earthquakes)

# parse_data()
# draw_beachballs()

# db = connect_db()
# add_db_records(db)

if __name__ == '__main__':
    app.run()