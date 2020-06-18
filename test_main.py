'''
Tests for jwt flask app.

06/17/2020
    Re-wrote tests using unittest instead of pytest.
    See https://knowledge.udacity.com/questions/75031 for error details.
    Simply, pytest is using python2 instead of python3, and is missing a module.
'''

import os
import json
import unittest
# import pytest
import main

## globals ##
SECRET = 'TestSecret'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjEzMDY3OTAsIm5iZiI6MTU2MDA5NzE5MCwiZW1haWwiOiJ3b2xmQHRoZWRvb3IuY29tIn0.IpM4VMnqIgOoQeJxUbLT-cRcAjK41jronkVrqRLFmmk'
EMAIL = 'wolf@thedoor.com'
PASSWORD = 'huff-puff'


class TestApp(unittest.TestCase):

    def setUp(self):
        os.environ['JWT_SECRET'] = SECRET
        main.APP.config['TESTING'] = True

    def tearDown(self):
        pass

    def test_health(self):
        client = main.APP.test_client()

        response = client.get('/')
        assert response.status_code == 200
        assert response.json == 'Healthy'

    def test_auth(self):
        client = main.APP.test_client()

        body = {'email': EMAIL,
                'password': PASSWORD}
        response = client.post('/auth',
                               data=json.dumps(body),
                               content_type='application/json')

        assert response.status_code == 200
        token = response.json['token']
        assert token is not None


if __name__ == '__main__':
    unittest.main()


"""
SECRET = 'TestSecret'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjEzMDY3OTAsIm5iZiI6MTU2MDA5NzE5MCwiZW1haWwiOiJ3b2xmQHRoZWRvb3IuY29tIn0.IpM4VMnqIgOoQeJxUbLT-cRcAjK41jronkVrqRLFmmk'
EMAIL = 'wolf@thedoor.com'
PASSWORD = 'huff-puff'

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client


def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth',
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None
"""
