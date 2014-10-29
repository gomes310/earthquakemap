from data_handler import parse_data, draw_beachballs, add_db_records
from earthquakes import connect_db

parse_data()
draw_beachballs()

# db = connect_db()
# add_db_records(db)