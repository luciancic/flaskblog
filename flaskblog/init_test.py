'''Makes the tester available in all inheriting test cases'''
import unittest

from flaskblog import app, db

app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'wejn1rkjn9v0df21fe5dfhh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

class InitTest(unittest.TestCase):
    app = app.test_client()

    def setUpClass(self):
        db.create_all()

    def setUp(self):
        pass

    def tearDownClass(self):
        db.drop_all()
