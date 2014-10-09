import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from obspy.imaging.beachball import Beachball

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

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# @app.route('/')
# def show_map():
#     return render_template('index.html')

# def parse_data():
# 	raw_data = open('static/1976.txt').readlines()
# 	earthquakes = list(chunker(raw_data, 5))

# 	mt_arrays = [eq[3].strip().split() for eq in earthquakes]
# 	moment_tensors = [[float(el) for el in arr[1::2]] for arr in mt_arrays]

# 	sdr_arrays = [eq[4].strip().split() for eq in earthquakes]
# 	strike_dip_rakes = [[float(el) for el in arr[11:14]] for arr in sdr_arrays]

# 	event_names = [eq[1][:16].strip() for eq in earthquakes]

# 	data = zip(event_names, moment_tensors, strike_dip_rakes)
# 	return data

# def chunker(seq, size):
#     return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

# def plot_beachballs():
# 	data = parse_data()
# 	for event in list(data):
# 		try:
# 			Beachball(event[1], facecolor='r', outfile='static/' + event[0] + '.png')
# 		except IndexError:
# 			Beachball(event[2], facecolor='r', outfile='static/' + event[0] + '.png')
# 			print "One of the moment tensor components was 0. Using strike/dip/rake values for event" + event[0]

# parse_data()
# plot_beachballs()

if __name__ == '__main__':
    app.run()