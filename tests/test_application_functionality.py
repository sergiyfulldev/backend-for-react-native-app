"""
Module designed to test specific bits of functionality inside the app that otherwise don't fit elsewhere.
"""
import json
import unittest
import os
import tempfile

from mobile.config import TestConfig
from mobile.factory import create_application
from mobile.extensions import db
from mobile.models import User

from mobile.utils import decode_auth_token


class AppBonesTestCase(unittest.TestCase):
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

    def get_auth_token_for(self,email,password,name):
        reg_resp = self.register(email,password,name)
        reg_json = reg_resp.data.decode()

        _json = json.loads(reg_json)
        return _json['token']

    def register(self, email, password, name):
        return self.app.test_client().post('/api/auth/register/', data=json.dumps(dict(
            email=email,
            password=password,
            name=name
        )), content_type="application/json")



if __name__ == "__main__":
    unittest.main()
