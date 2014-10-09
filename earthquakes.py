from flask import Flask, render_template
from obspy.imaging.beachball import Beachball

app = Flask(__name__)

@app.route('/')
def show_map():
    return render_template('index.html')

def parse_data():
	raw_data = open('static/1976.txt').readlines()
	earthquakes = chunker(raw_data, 5)
	mt_arrays = [eq[3].strip().split() for eq in earthquakes]
	moment_tensors = [[float(arr[1]), float(arr[3]), float(arr[5]), float(arr[7]), float(arr[9]), float(arr[11])] for arr in mt_arrays]
	return moment_tensors

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def plot_beachballs():
	moment_tensors = parse_data()
	for i, mt in enumerate(moment_tensors):
		try:
			Beachball(mt, facecolor='r', outfile='static/' + str(i) + '.png')
		except IndexError:
			# Beachball(sdr, facecolor='r', outfile='static/' + str(i) + '.png')
			print "One of the moment tensor components was 0. Using strike/dip/rake values for beach ball #" + str(i)

parse_data()
plot_beachballs()

if __name__ == '__main__':
    app.run()