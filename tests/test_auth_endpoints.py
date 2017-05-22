import unittest
import json

from bucketlist import db, create_app


class AuthenticationTest(unittest.TestCase):

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

    def test_register(self):
        self.assertEqual(self.register_response.status_code, 201)

    def test_register_existing_email(self):
        user_data = {'email': 'maryanne.nganga@andela.com', 'first_name': 'maryanne', 'last_name': 'Nganga',
                     'username': 'waceke', 'password': 'saxophone'}
        response = self.client.post(
            '/auth/register', data=user_data)
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_email(self):
        user_data = {'email': 'lavender@com', 'username': 'lavender101', 'first_name': 'lavender', 'last_name': 'ayodi',
                    'password': 'saxophone'}
        response = self.client.post(
            '/auth/register', data=user_data)
        self.assertEqual(response.status_code, 400)

    def test_register_existing_username(self):
        user_data = {'email': 'maryannewaceke@gmail.com', 'first_name': 'maryanne', 'last_name': 'waceke',
                     'username': 'maryanne', 'password': 'saxophone'}
        response = self.client.post(
            '/auth/register', data=user_data)
        self.assertEqual(response.status_code, 400)

    def test_register_wrong_email(self):
        user_data = {'email': 'maryanne@.wacekegmail.com', 'first_name': 'maryanne', 'last_name': 'waceke',
                     'username': 'maryanne', 'password': 'saxophone'}
        response = self.client.post(
            '/auth/register', data=user_data)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        login_credentials = {"email": "maryanne.nganga@andela.com", "password": "saxophone"}
        response = self.client.post(
            '/auth/login', data=login_credentials)
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_credentials(self):
        login_credentials = {"email": "maryanne.nganga@andela.com", "password": ""}
        response = self.client.post(
            '/auth/login', data=login_credentials)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
