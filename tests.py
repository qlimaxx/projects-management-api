import base64
import unittest

from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from app import create_app
from app.config import TestingConfig
from app.enums import Role, Status
from app.models import Project, Result, Test, User, db


ADMIN_EMAIL = 'admin@mail.com'
ADMIN_PASSWORD = 'admin'
USER_EMAIL = 'user@mail.com'
USER_PASSWORD = 'pass'
USER = {'email': USER_EMAIL, 'phash': generate_password_hash(
    USER_PASSWORD), 'role': Role.USER.value}
PROJECT = {'name': 'Project'}
TEST = {'name': 'Test'}


class ApiTest(TestCase):

    def _create_authorization_header(self, username, password):
        return 'Basic {}'.format(
            str(base64.b64encode('{0}:{1}'.format(
                username, password).encode('utf-8')), 'utf-8'))

    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.user = User(
            email=ADMIN_EMAIL,
            phash=generate_password_hash(ADMIN_PASSWORD),
            role=Role.ADMIN.value)
        db.session.add(self.user)
        db.session.commit()
        self.headers = {'Authorization': self._create_authorization_header(
            ADMIN_EMAIL, ADMIN_PASSWORD)}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        response = self.client.post(
            '/api/v1/user', headers=self.headers, json=USER)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(User.query.filter_by(**USER).first())

    def test_create_duplicate_user(self):
        db.session.add(User(**USER))
        db.session.commit()
        response = self.client.post(
            '/api/v1/user', headers=self.headers, json=USER)
        self.assertEqual(response.status_code, 400)

    def test_create_project(self):
        response = self.client.post(
            '/api/v1/project', headers=self.headers, json=PROJECT)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Project.query.filter_by(**PROJECT).first())

    def test_create_duplicate_project(self):
        db.session.add(Project(**PROJECT))
        db.session.commit()
        response = self.client.post(
            '/api/v1/project', headers=self.headers, json=PROJECT)
        self.assertEqual(response.status_code, 400)

    def test_create_project_with_insufficient_role(self):
        db.session.add(User(**USER))
        db.session.commit()
        self.headers['Authorization'] = self._create_authorization_header(
            USER_EMAIL, USER_PASSWORD)
        response = self.client.post(
            '/api/v1/user', headers=self.headers, json=USER)
        self.assertEqual(response.status_code, 403)

    def test_create_test(self):
        db.session.add(Project(**PROJECT, user=self.user))
        db.session.commit()
        response = self.client.post(
            '/api/v1/{0}/test'.format(PROJECT['name']),
            headers=self.headers, json=TEST)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Test.query.filter_by(**TEST).first())

    def test_run_test(self):
        project = Project(**PROJECT, user=self.user)
        db.session.add(project)
        db.session.add(Test(**TEST, project=project, user=self.user))
        db.session.commit()
        response = self.client.post(
            '/api/v1/{0}/{1}/run'.format(PROJECT['name'], TEST['name']),
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Result.query.filter_by(
            run_id=response.json['id']).first())

    def test_get_test_result(self):
        project = Project(**PROJECT, user=self.user)
        db.session.add(project)
        test = Test(**TEST, project=project, user=self.user)
        db.session.add(test)
        result = Result(test=test, user=self.user,
                        status=Status.SUCCEEDED.value)
        db.session.add(result)
        db.session.commit()
        response = self.client.get(
            '/api/v1/{0}/{1}/{2}'.format(
                PROJECT['name'], TEST['name'], result.run_id),
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], Status.SUCCEEDED.value)


if __name__ == '__main__':
    unittest.main()
