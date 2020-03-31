import json
import unittest
import os
import tempfile

from mobile.config import TestConfig
from mobile.factory import create_application
from mobile.extensions import db
from mobile.models import User, Job, Permission
from mobile.utils import decode_auth_token


class AdminRoutesTestCase(unittest.TestCase):
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

    def get_auth_token_for(self, email, password, name):
        reg_resp = self.register(email, password, name)
        reg_json = reg_resp.data.decode()

        _json = json.loads(reg_json)
        return _json['token']

    def register(self, email, password, name):
        return self.app.test_client().post('/api/auth/register/', data=json.dumps(dict(
            email=email,
            password=password,
            name=name
        )), content_type="application/json")

    def test_admin_perms_required(self):
        user_token = self.get_auth_token_for("test@test.com", "test", "test user")

        _req = self.app.test_client().get('/api/admin/permissions/',
                                          headers={'Authorization': "Bearer {0}".format(user_token)})

        self.assertEqual(_req.status_code, 401)

        permission = Permission(name="admin")

        db.session.add(permission)
        db.session.commit()

        user = User.query.filter_by(id=1).first()

        user.permissions.append(permission)

        db.session.add(user)
        db.session.commit()

        _req = self.app.test_client().get('/api/admin/permissions/',
                                          headers={'Authorization': "Bearer {0}".format(user_token)})

        self.assertEqual(_req.status_code, 200)

    def test_admin_perms_add_to_user(self):

        admin_token = self.get_auth_token_for('test@test.com','test','test user')

        user = User.query.filter_by(id=1).first()

        permission = Permission(name='admin')

        db.session.add(permission)
        db.session.commit()

        _req = self.app.test_client().post('/api/admin/users/permissions/',data=json.dumps(dict(
            user_id=user.id,
            permission_id=permission.id
        )),headers={'Authorization': 'Bearer {0}'.format(admin_token)},content_type='application/json')

        self.assertEqual(_req.status_code,200)

        resp = json.loads(_req.data.decode())

        self.assertEqual(resp['message'],'Permission added to user')

    def test_admin_perms_delete_from_user(self):

        admin_token = self.get_auth_token_for("test@test.com","test","Test Admin")

        user = User.query.filter_by(id=1).first()

        permission = Permission(name="admin")

        db.session.add(permission)
        user.permissions.append(permission)
        db.session.add(user)
        db.session.commit()

        _req = self.app.test_client().delete("/api/admin/users/permissions/",data=json.dumps(dict(
            user_id=user.id,
            permission_id=permission.id
        )),headers={'Authorization': 'Bearer {0}'.format(admin_token)}, content_type='application/json')

        self.assertEqual(_req.status_code,200)

        resp = json.loads(_req.data.decode())

        self.assertEqual(resp['message'],"Permission removed from the user")


if __name__ == "__main__":
    unittest.main()
