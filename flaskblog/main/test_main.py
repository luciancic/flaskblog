from flaskblog.init_test import client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.mimetype == 'text/html'

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert response.mimetype == 'text/html'
