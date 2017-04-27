import unittest
import json
from flask import current_app

from bucketlist.models import User, Bucketlist, Item
from bucketlist import db, create_app

class BaseTestcase(unittest.TestCase):
    '''
    Base tests for all test classes.
    '''
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        user_data = {'email': 'maryanne.nganga@andela.com', 'firstname': 'maryanne', 'lastname': 'Nganga',
                     'username': 'maryanne', 'password': 'saxophone'}
        response = self.client.post('/auth/register', data=json.dumps(user_data))
        self.response = self.client.post(
            '/bucketlist', data={'name': 'Crazy Stuff Bucketlist'})

class ModelTestCase(BaseTestcase):
    '''
    Models tests
    '''
    def test_model_can_add_bucketlist(self):
        original_bucket_count = Bucketlist.query.count()
        bucketlist = Bucketlist(name='travel bucketlist')
        db.session.add(bucketlist)
        new_count = Bucketlist.query.count()
        self.assertTrue(new_count > original_bucket_count)

    def test_model_can_add_item(self):
        item = Item(name='go to India')
        original_count = Item.query.count()
        db.session.add(item)
        new_count = Item.query.count()
        self.assertTrue(new_count > original_count)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class ApiTestCase(BaseTestcase):
    '''
    Tests for the API endpoint.
    '''
    def test_app_configuration(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_register(self):
        user_data = {'email': 'daisy.ndungu@andela.com', 'firstname': 'daisy', 'lastname': 'Ndungu',
                     'username': 'daisy', 'password': 'guitar'}
        response = self.client.post('/auth/register', data=json.dumps(user_data))
        self.assertEqual(response.status_code, 201)

    def test_register_existing_email(self):
        user_data = {'email': 'maryanne.nganga@andela.com', 'firstname': 'maryanne', 'lastname': 'Nganga',
                     'username': 'maryanne', 'password': 'saxophone'}
        response = self.client.post('/auth/register', data=json.dumps(user_data))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_register_invalid_email(self):
        user_data = {'email': 'lavender.com', 'firstname': 'lavender', 'lastname': 'ayodi',
                     'username': 'lavender101', 'password': 'saxophone'}
        response = self.client.post('/auth/register', data=json.dumps(user_data))
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_register_existing_username(self):
        puser_data = {'email': 'maryannewaceke@gmail.com', 'firstname': 'maryanne', 'lastname': 'waceke',
                     'username': 'maryanne', 'password': 'saxophone'}
        response = self.client.post('/auth/register', data=json.dumps(user_data))
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_login(self):
        login_credentials = {'email': 'maryanne.nganga@andela.com', 'password': 'saxophone'}
        response = self.client.post('/auth/login', data=json.dumps(login_credentials))
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_username(self):
        pass

    def test_login_invalid_password(self):
        pass


    def test_bucketlist_add(self):
        new_bucketlist = {'name': "travel", 'date_created': '2016-09-12 11:57:23',
                             'date_modified': '2017-08-12 08:45:12', 'created_by': '118746'}
        response = self.client.post('/bucketlists', data=json.dumps(new_bucketlist) )
        self.assertEqual(response.status_code, 201)

        # get all bucketlists
        response = self.client.get('/bucketlists')
        self.assertEqual(response.status_code, 200)
        

    def test_bucketlist_insufficient_information(self):
        new_bucketlist=data={'name': 'food bucketlist', 'created_by': '118746'}
        response = self.client.post('/bucketlist')
        self.assertEqual(response.status_code, 400)

    def test_bucketlist_get_one_bucketlist(self):
        response = self.client.get(
            '/bucketlists/1')
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_update(self):
        changed_bucketlist = {'name': "live life", 'date_modified': '2017-08-12 08:45:12', 'created_by': '118746'}
        response = self.client.put('/bucketlist/1', data=json.dumps(changed_bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_delete(self):
        response = self.client.delete('/bucketlist/1')
        self.assertEqual(response.status_code, 200)


    def test_bucketlist_item_post(self):
        new_item = {'name': 'go to jamaica with Evans', 'date_created': '2016-09-12 11:57:23',
                         'date_modified': '2016-09-12 11:57:23'}
        response = self.client.post('/bucketlist/1/items', data=json.dumps(new_item))
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/bucketlist/1/items')
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_item_update(self):
        changed_item = {'name':'Go to India with Lisa'}
        response = self.client.put('/bucketlist/1/items/1', data=json.dumps(changed_item))
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_item_delete(self):
        response = self.client.delete('/bucketlist/1/items/1')
        self.assertEqual(response.status_code, 200)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
