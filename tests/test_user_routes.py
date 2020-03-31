import json
import unittest
import os
import tempfile

from mobile.config import TestConfig
from mobile.factory import create_application
from mobile.extensions import db
from mobile.models import User, JobCategory, UserSkills

from mobile.utils import decode_auth_token,get_user_id


class UserRoutesTestCase(unittest.TestCase):
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

    def test_user_profile(self):
        user_token = self.get_auth_token_for("test@test.com","test","test 1")

        profile_request = self.app.test_client().get('/api/users/info/',headers={'Authorization': "Bearer {0}".format(user_token)})

        self.assertEqual(profile_request.status_code,200)

        _json = json.loads(profile_request.data.decode())

        self.assertEqual(_json['user']['email'],"test@test.com")

    def test_user_job_experience(self):
        user_token = self.get_auth_token_for("test@test.com","test","test 1")

        uid = decode_auth_token(user_token)['sub']
        # Define the skill
        job_category_it = JobCategory(name="IT")

        db.session.add(job_category_it)
        db.session.commit()

        skill_experience_request = self.app.test_client().post('/api/users/experience/',headers={'Authorization': "Bearer {0}".format(user_token)}, data=json.dumps(dict(
            skills=[
                dict(id=job_category_it.id,years_experience=8)
            ]
        )),content_type="application/json")

        self.assertEqual(skill_experience_request.status_code,200)

        _json = json.loads(skill_experience_request.data.decode())

        self.assertEqual(_json['status'],"success")

        user = User.query.filter_by(id=1).first()

        self.assertGreaterEqual(len(user.job_experience),1)

        self.assertEqual(user.job_experience[0].job_category_id,job_category_it.id)

    def test_user_about(self):
        user_token = self.get_auth_token_for("test@test.com","test","test 1")

        uid = decode_auth_token(user_token)['sub']

        user_about_request = self.app.test_client().post('/api/users/about/',headers={'Authorization': "Bearer {0}".format(user_token)},content_type="application/json",
                                                         data=json.dumps(dict(about="This is my about")))

        self.assertEqual(user_about_request.status_code,200)

        _json = json.loads(user_about_request.data.decode())

        self.assertEqual(_json['status'],'success')

        user = User.query.filter_by(id=1).first()

        self.assertEqual(user.about,"This is my about")

    def test_user_skills(self):
        user_token = self.get_auth_token_for("test@test.com","test","test 1")

        uid = decode_auth_token(user_token)['sub']

        user_skills_request = self.app.test_client().post('/api/users/skills/',headers={'Authorization': "Bearer {0}".format(user_token)},content_type='application/json',
                                                          data=json.dumps(dict(
                                                              skill="Python Development"
                                                          )))

        self.assertEqual(user_skills_request.status_code,200)

        _json = json.loads(user_skills_request.data.decode())

        self.assertEqual(_json['status'],'success')
        self.assertEqual(_json['message'],'Skill Added')

        user_skill = UserSkills.query.filter_by(user_id=uid,name="Python Development").first()

        self.assertIsNotNone(user_skill)


if __name__ == "__main__":
    unittest.main()
