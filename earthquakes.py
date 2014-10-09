from flask import Flask, render_template
from obspy.imaging.beachball import Beachball

app = Flask(__name__)

@app.route('/')
def show_map():
    return render_template('index.html')

def parse_data():
	raw_data = open('static/1976.txt').readlines()
	earthquakes = list(chunker(raw_data, 5))

	mt_arrays = [eq[3].strip().split() for eq in earthquakes]
	moment_tensors = [[float(arr[1]), float(arr[3]), float(arr[5]), float(arr[7]), float(arr[9]), float(arr[11])] for arr in mt_arrays]

	sdr_arrays = [eq[4].strip().split() for eq in earthquakes]
	strike_dip_rakes = [[float(arr[11]), float(arr[12]), float(arr[13])] for arr in sdr_arrays]

	event_names = [eq[1][:16].strip() for eq in earthquakes]

	data = zip(event_names, moment_tensors, strike_dip_rakes)
	return data

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def plot_beachballs():
	data = parse_data()
	for event in list(data):
		try:
			Beachball(event[1], facecolor='r', outfile='static/' + event[0] + '.png')
		except IndexError:
			Beachball(event[2], facecolor='r', outfile='static/' + event[0] + '.png')
			print "One of the moment tensor components was 0. Using strike/dip/rake values for event" + event[0]

parse_data()
plot_beachballs()

if __name__ == '__main__':
    app.run()