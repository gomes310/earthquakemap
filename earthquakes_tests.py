import os
import earthquakes
import unittest
import tempfile

class EarthquakesTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, earthquakes.app.config['DATABASE'] = tempfile.mkstemp()
        earthquakes.app.config['TESTING'] = True
        self.app = earthquakes.app.test_client()
        earthquakes.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(earthquakes.app.config['DATABASE'])

    def test_contains_earthquake_data(self):
    	rv = self.app.get('/')

if __name__ == '__main__':
    unittest.main()