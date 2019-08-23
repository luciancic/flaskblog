'''Makes the tester available in all inheriting test cases'''
import unittest

from flaskblog import app


class InitTest(unittest.TestCase):
    app = app.test_client()
