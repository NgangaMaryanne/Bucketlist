import unittest
import json

from bucketlist import db, create_app


class ApiEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        user_data1 = {'email': 'maryanne.nganga@andela.com', 'first_name': 'maryanne', 'last_name': 'Nganga',
                     'username': 'maryanne', 'password': 'saxophone'}
        self.register_response = self.client.post(
            '/auth/register', data=user_data1)
        self.login_response = self.client.post('/auth/login', data = {'email': 'maryanne.nganga@andela.com', 'password': 'saxophone'})

    def test_bucketlist_get_all(self):
        auth_token = json.loads(self.login_response.data)['auth_token']
        response = self.client.post('/api/v1/bucketlists/', data={"name":"hello awesome"}, headers={'Content-Type': 'application/json',
                                    'Authorization':auth_token})

        self.assertEqual(response.status_code, 200)


    def tearDown(self):
        db.session.remove()
        db.drop_all()