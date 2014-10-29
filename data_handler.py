from obspy.imaging.beachball import Beachball
from flask import g

def chunker(seq, size):
  	return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def parse_data():
	raw_data = open('static/all_events.txt').readlines()
	earthquakes = list(chunker(raw_data, 5))

	event_names = [eq[1][:16].strip() for eq in earthquakes]

	line_one_arrays = [eq[0].strip().split() for eq in earthquakes]
	latitudes = [float(arr[3]) for arr in line_one_arrays]
	longitudes = [float(arr[4]) for arr in line_one_arrays]
	depths = [float(arr[5]) for arr in line_one_arrays]
	magnitudes = [float(arr[6]) for arr in line_one_arrays]

	mt_arrays = [eq[3].strip().split() for eq in earthquakes]
	moment_tensors = [[float(el) for el in arr[1::2]] for arr in mt_arrays]

	sdr_arrays = [eq[4].strip().split() for eq in earthquakes]
	strike_dip_rakes = [[float(el) for el in arr[11:14]] for arr in sdr_arrays]

	data = zip(event_names, latitudes, longitudes, moment_tensors, strike_dip_rakes, depths, magnitudes)
	return data

def parse_data_for_fusion_table():
	raw_data = open('static/all_events.txt').readlines()
	earthquakes = list(chunker(raw_data, 5))
	
	fusion_table = open('all_events_parsed.csv', 'w')
	fusion_table.write('Event_name,Location,Depth,Magnitude\n')

	for eq in earthquakes:
		event_name = eq[1][:16].strip()

		line_one = eq[0].strip().split()
		latitude = line_one[3]
		longitude = line_one[4]
		depth = line_one[5]
		magnitude = line_one[6]

		line = ','.join([event_name, latitude + ' ' + longitude, depth, magnitude]) + '\n'
		fusion_table.write(line)

def draw_beachballs():
	data = parse_data()
	for event in list(data):
		if event[5] < 70:
			face_color = '#ff0000'
		elif event[5] > 300:
			face_color = '#0000ff'
		else:
			face_color = '#ffff00'

		try:
			Beachball(event[3], facecolor=face_color, width=100, outfile='static/beachballs4/' + event[0] + '.png')
		except: # IndexError:
			print "Error for event " + event[0]
			Beachball(event[4], facecolor=face_color, width=100, outfile='static/beachballs4/' + event[0] + '.png')
			# print "One of the moment tensor components was 0. Using strike/dip/rake values for event" + event[0]

def add_db_records(db):
	db.execute('delete from earthquakes')
	data = parse_data()
	for event in list(data):
		db.execute('insert into earthquakes (event_name, latitude, longitude, moment_tensor, strike_dip_rake, depth, magnitude) values (?, ?, ?, ?, ?, ?, ?)', [event[0], event[1], event[2], str(event[3]), str(event[4]), event[5], event[6]])
		db.commit()
