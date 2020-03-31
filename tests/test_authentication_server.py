import json
import unittest
import os
import tempfile

from mobile.config import TestConfig
from mobile.factory import create_application
from mobile.extensions import db
from mobile.utils import decode_auth_token


class AuthenticationServerTestCase(unittest.TestCase):
    """
    Test cases for the authentication server and its supporting API Methods.
    """
    def setUp(self):
        self.app = create_application(config_override=TestConfig)

        self.db_fb, self.app.config['DATABASE'] = tempfile.mkstemp()

        self.app.testing = True

        with self.app.app_context():
            import mobile.models
            db.create_all(app=self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()
        os.close(self.db_fb)
        os.unlink(self.app.config['DATABASE'])

    def register(self, email, password, name):
        return self.app.test_client().post('/api/auth/register/', data=json.dumps(dict(
            email=email,
            password=password,
            name=name
        )), content_type="application/json")

    def login(self,email,password):
        return self.app.test_client().post('/api/auth/login/', data=json.dumps(dict(
            email=email,
            password=password
        )), content_type="application/json")

    def check(self,token):
        return self.app.test_client().get('/api/auth/check/{0}'.format(token))

    def test_user_registration(self):
        response = self.register("example@example.com", "testpassword", "test user")
        self.assertEqual(response.status_code, 200)
        self.assertIn('registration complete',response.data.decode('utf-8').lower())

        reg_json = json.loads(response.data.decode('utf-8'))
        token = reg_json['token']
        self.assertIsNotNone(token)

        email_token = reg_json['email_token']
        self.assertIsNotNone(email_token)

    def test_user_login(self):
        register_response = self.register("example@example.com","testpassword","test user")
        self.assertEqual(register_response.status_code,200)

        login_response = self.login("example@example.com","testpassword")
        self.assertEqual(login_response.status_code, 200)
        self.assertIn('login successful', login_response.data.decode('utf-8').lower())

    def test_token_check(self):
        reg_resp = self.register("example@example.com","testpassword","test user")
        self.assertEqual(reg_resp.status_code,200)

        reg_json = json.loads(reg_resp.data.decode('utf-8'))
        token = reg_json['token']

        self.assertIsNotNone(token)

        token_resp = self.check(token)
        self.assertEqual(token_resp.status_code,200)




if __name__ == "__main__":
    unittest.main()
