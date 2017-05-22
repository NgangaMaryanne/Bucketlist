import unittest
import json

from bucketlist import db, create_app


class ApiEndpointTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        user_data1 = {"email": "gladiz.nganga@andela.com", "first_name": "gladiz", "last_name": "Nganga",
                      "username": "gladiz", "password": "saxophone"}
        self.register_response = self.client.post(
            '/auth/register', data=user_data1)
        credentials = {"email": "gladiz.nganga@andela.com", "password": "saxophone"}
        self.login_response = self.client.post(
            '/auth/login', data= credentials)
        print("ajkfayg vtyF yuafuakHJA UBAKDUHFAN UAYHBFAU JAHBDUJA", json.loads(self.login_response.data))
        self.auth_token = json.loads(self.login_response.data)['auth_token']

        self.post_response = self.client.post('/api/v1/bucketlists', data=json.dumps({"name": "cool stuff"}), headers={'Content-Type': 'application/json',
                                                                                                                       'Access-Control-Allow-Origin': '*', 'Authorization': self.auth_token})
        print("kgjakgaugiaigoaikomvavnmajfvma", json.loads(self.post_response.data))
        self.post_items = self.client.post('/api/v1/bucketlists/1/items', data=json.dumps({"name": "sky dive"}), 
                                           headers={'Content-Type': 'application/json',
                                             'Access-Control-Allow-Origin': '*', 'Authorization': self.auth_token})
        print("agkjfaugjaoujrfoaijlmvaaiuhniuhkjnvaoks", json.loads(self.post_items.data))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_bucketlist_get(self):

        response = self.client.get('/api/v1/bucketlists', headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
                                                                   'Authorization': self.auth_token})
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_get_one(self):
        response = self.client.get('/api/v1/bucketlists/1', headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
                                                                     'Authorization': self.auth_token})
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_get_inexistent(self):
        response = self.client.get('/api/v1/bucketlists/2', headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
                                                                     'Authorization': self.auth_token})
        message = json.loads(response.data)['message']
        self.assertEqual(
            message, "You do not have bucket with id 2. Please try again")

    def test_bucketlist_post(self):
        message = json.loads(self.post_response.data)['message']
        self.assertEqual(self.post_response.status_code, 200)
        self.assertEqual(message, "Bucketlist created.")

    def test_bucketlist_post_incomplete_information(self):
        post_response = self.client.post('/api/v1/bucketlists', headers={'Content-Type': 'application/json',
                                                                         'Access-Control-Allow-Origin': '*', 'Authorization': self.auth_token})
        self.assertEqual(post_response.status_code, 400)

    def test_bucketlist_put(self):
        put_response = self.client.put('/api/v1/bucketlists/1', data=json.dumps({"name": "hello awesome"}), headers={'Content-Type': 'application/json',
                                                                                                                     'Access-Control-Allow-Origin': '*', 'Authorization': self.auth_token})
        self.assertEqual(put_response.status_code, 204)

    def test_bucketlist_put_incomplete_information(self):
        put_response = self.client.put('/api/v1/bucketlists/1', headers={'Content-Type': 'application/json',
                                                                                                                     'Access-Control-Allow-Origin': '*', 'Authorization': self.auth_token})
        self.assertEqual(put_response.status_code, 400)

    def test_bucketlist_delete(self):
        response = self.client.delete('/api/v1/bucketlists/1', headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
                                                                        'Authorization': self.auth_token})
        message = json.loads(response.data)['message']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, "Bucket 1 successfully deleted")

    def test_bucketlist_items_add(self):
        message = json.loads(self.post_items.data)['message']
        self.assertEqual(self.post_items.status_code, 200)
        self.assertEqual(message, "New item added to bucketlist.")

    def test_bucketlist_items_put(self):
        update_response = self.client.put('/api/v1/bucketlists/1/items/1', data=json.dumps({"name": "sky dive in the mara"}), headers={'Content-Type': 'application/json',
                                                                                                                                       'Access-Control-Allow-Origin': '*', 'Authorization': self.auth_token})
        message = json.loads(update_response.data)['message']
        self.assertEqual(message, "item 1 updated successfully")
        self.assertEqual(update_response.status_code, 200)

    def test_bucketlist_item_delete(self):
        delete_response = self.client.delete('/api/v1/bucketlists/1/items/1', data=json.dumps({"name": "sky dive in the mara"}), headers={'Content-Type': 'application/json',
                                                                                                                                          'Access-Control-Allow-Origin': '*', 'Authorization': self.auth_token})
        message = json.loads(delete_response.data)['message']
        self.assertEqual(message, "item deleted.")
        self.assertEqual(delete_response.status_code, 200)

    
