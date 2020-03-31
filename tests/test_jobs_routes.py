import json
import unittest
import os
import tempfile

from mobile.config import TestConfig
from mobile.factory import create_application
from mobile.extensions import db
from mobile.models import User, Job, JobCategory, JobType
from mobile.utils import decode_auth_token


class JobRoutesTestCase(unittest.TestCase):
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

    def post_job(self, title, description, longitude, latitude, auth_token, category, job_type):
        return self.app.test_client().post('/api/jobs/post/', data=json.dumps(dict(
            title=title,
            description=description,
            longitude=longitude,
            latitude=latitude,
            job_type=job_type,
            category=category,
        )), headers={
            'Authorization': "Bearer {0}".format(auth_token)
        }, content_type="application/json")

    def test_job_post_success(self):
        token = self.get_auth_token_for("test@test.com", "test", "test user")

        job_category = JobCategory(name="Kitchen")
        job_type = JobType(name="Barista",category_id=job_category.id)


        job_category.job_types.append(job_type)

        db.session.add(job_type)
        db.session.add(job_category)
        db.session.commit()

        job_post_response = self.post_job(
            title="Walk my dog",
            description="ye",
            longitude="-63.1315222",
            latitude="46.2356426",
            auth_token=token,
            job_type=job_type.name,
            category=job_category.name
        )
        self.assertEqual(job_post_response.status_code, 200)
        _json = json.loads(job_post_response.data.decode())['job']

        self.assertGreaterEqual(_json['id'], 0)
        self.assertGreaterEqual(_json['owner_id'], 0)

        jobs = Job.query.all()

        self.assertEqual(len(jobs), 1)

    def test_job_post_failure(self):
        # Fails because: title element is null, and category / job_type is also not defined.

        token = self.get_auth_token_for("test@test.com", "test", "test user")

        job_category = JobCategory(name="Kitchen")
        job_type = JobType(name="Barista",category_id=job_category.id)

        db.session.add(job_type)
        db.session.add(job_category)

        job_category.job_types.append(job_type)

        db.session.add(job_category)


        db.session.commit()

        job_post_response = self.post_job(
            title="",
            description="ye",
            longitude="-63.1315222",
            latitude="46.2356426",
            auth_token=token,
            category=job_category.name,
            job_type=job_type.name
        )
        self.assertEqual(job_post_response.status_code, 400)
        _json = json.loads(job_post_response.data.decode())

        self.assertEqual(_json['status'],"error")

    def test_job_no_auth(self):
        job_post_response = self.app.test_client().post('/api/jobs/post/', data=json.dumps(dict(
            title="",
            description="ye",
            longitude="-63.1315222",
            latitude="46.2356426"
        )), content_type="application/json")
        self.assertEqual(job_post_response.status_code, 401)

    def test_get_job_info(self):
        token = self.get_auth_token_for("test@test.com", "test", "test user")

        job_category = JobCategory(name="Kitchen")

        db.session.add(job_category)

        job_type = JobType(name="Barrista",category=job_category)

        db.session.add(job_type)

        db.session.commit()

        job_post_response = self.post_job(
            title="Walk my dog",
            description="ye",
            longitude="-63.1315222",
            latitude="46.2356426",
            auth_token=token,
            category=job_category.name,
            job_type=job_type.name
        )

        self.assertEqual(job_post_response.status_code, 200)

        jp_resp = job_post_response.data.decode()

        job_id = json.loads(job_post_response.data.decode())['job']['id']

        job_info_response = self.app.test_client().get('/api/jobs/info/{0}'.format(job_id),
                                                       headers={'Authorization': "Bearer {0}".format(token)})

        self.assertEqual(job_info_response.status_code, 200)

        _json = json.loads(job_info_response.data.decode())

        self.assertEqual(_json['status'], 'success')

    def test_get_invalid_job(self):
        token = self.get_auth_token_for("test@test.com", "test", "test user")
        job_info_response = self.app.test_client().get('/api/jobs/info/1',
                                                       headers={'Authorization': "Bearer {0}".format(token)})
        self.assertEqual(job_info_response.status_code, 400)
        _json = json.loads(job_info_response.data.decode())

        self.assertEqual(_json['status'], "error")
        self.assertEqual(_json['message'], "Invalid Job ID")

    def test_job_list(self):
        token = self.get_auth_token_for("test@test.com", "test", "test user")
        job_list_response = self.app.test_client().get('/api/jobs/list',
                                                       headers={'Authorization': "Bearer {0}".format(token)})

        self.assertEqual(job_list_response.status_code, 200)

        _json = json.loads(job_list_response.data.decode())

        self.assertEqual(len(_json['jobs']), 0)

        # Now add a job to the list and see if we can see it.

        category = JobCategory(name="Test Cat")
        category.save()

        job_type = JobType(name="Test Type",category=category)
        job_type.save(commit=True)

        job_post_response = self.post_job("Title", "Description", "-1", "1", token,category=category.name,job_type=job_type.name)

        self.assertEqual(job_post_response.status_code, 200)

        job_list_response = self.app.test_client().get('/api/jobs/list/all',
                                                       headers={'Authorization': "Bearer {0}".format(token)})
        _json = json.loads(job_list_response.data.decode())

        self.assertGreaterEqual(len(_json['jobs']), 1)

        job_list_response = self.app.test_client().get('/api/jobs/list/applied',
                                                       headers={'Authorization': "Bearer {0}".format(token)})
        _json = json.loads(job_list_response.data.decode())

        self.assertGreaterEqual(len(_json['jobs']), 0)

    def test_job_apply(self):
        token = self.get_auth_token_for("test@test.com", "test", "test user")

        category = JobCategory(name="Kitchen")

        db.session.add(category)

        job_type = JobType(name="Barrista",category_id=category.id)

        db.session.add(job_type)

        category.job_types.append(job_type)

        db.session.add(category)

        db.session.commit()

        post_data = self.post_job("Title", "description", "-1", "1", token,category=category.name,job_type=job_type.name)

        self.assertEqual(post_data.status_code, 200)

        apply_response = self.app.test_client().post(
            '/api/jobs/apply/',
            data=json.dumps(dict(id=1)),
            headers={'Authorization': 'Bearer {0}'.format(token)},
            content_type="application/json"
        )

        _json = json.loads(apply_response.data.decode())

        self.assertEqual(apply_response.status_code, 200)

        self.assertEqual(_json['status'], 'success')

        user = User.query.filter_by(id=decode_auth_token(token)['sub']).first()

        self.assertEqual(len(user.jobs_applied), 1)

        job_1 = Job.query.all()[0]

        self.assertEqual(job_1.id, user.jobs_applied[0].job_id)

        # Now we apply a second time to the same job
        # And get an error stating we've already applied
        apply_response = self.app.test_client().post(
            '/api/jobs/apply/',
            data=json.dumps(dict(id=1)),
            headers={'Authorization': 'Bearer {0}'.format(token)},
            content_type="application/json"
        )

        self.assertEqual(apply_response.status_code, 400)

        _json = json.loads(apply_response.data.decode())
        self.assertEqual(_json['status'], 'error')
        self.assertEqual(_json['message'], 'An application has already been submitted for this job.')

    def test_job_search(self):
        user_1_token = self.get_auth_token_for("test@test.com", "test", "test user")

        user_2_token = self.get_auth_token_for("test2@test.com", "test1", "test user 2")

        user_2_long = 46.2570767
        user_2_lat = -63.1264856

        job_category = JobCategory(name="Kitchen")

        job_type = JobType(name="Barrista",category_id=job_category.id)

        job_category.job_types.append(job_type)

        db.session.add(job_category)
        db.session.add(job_type)

        job_1 = Job(owner_id=1, title="Babysit my pet", description="I need my dog watched", longitude="46.2588051",
                    latitude="-63.1245543", category=job_category, job_type=job_type)
        db.session.commit()

        user_2 = User.query.filter_by(id=2).first()

        db.session.add(job_1)
        db.session.add(user_2)
        db.session.commit()

        search_request = self.app.test_client().post(
            '/api/jobs/search/',
            data=json.dumps(dict(
                search=dict(
                    radius=5,
                    long=user_2_long,
                    lat=user_2_lat,
                    job_type="Barrista"
                )
            )),
            content_type="application/json",
            headers={'Authorization': 'Bearer {0}'.format(user_2_token)}
        )

        self.assertEqual(search_request.status_code, 200)

        _json = json.loads(search_request.data.decode())

        self.assertEqual(_json['jobs'][0]['id'], 1)

    def test_job_category_route(self):

        user_1 = self.get_auth_token_for("test@test.com","test","test user")

        category = JobCategory(name="Kitchen")
        category.save(commit=True)
        job_type = JobType(name="Barista",category=category)
        job_type.save(commit=True)

        category_request = self.app.test_client().get(
            '/api/jobs/categories',
            content_type="application/json",
            headers={'Authorization': 'Bearer {0}'.format(user_1)}
        )

        _json = json.loads(category_request.data.decode())

        self.assertEqual(len(_json['categories']),1)

        self.assertEqual(_json['categories'][0]['id'],1)

if __name__ == "__main__":
    unittest.main()
