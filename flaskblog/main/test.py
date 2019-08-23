'''Test main routes'''
from flaskblog.init_test import InitTest

class MainTests(InitTest):
    '''Test main routes'''
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
