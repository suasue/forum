import json

from django.test import TestCase, Client

from user.models import User


client = Client()

class ModelTest(TestCase):
	def test_create_user(self):
		email    = 'test@example.com'
		name     = 'test_name'
		password = 'test1234'

		user = User.objects.create_user(
			email    = email,
			name     = name,
			password = password
		)

		self.assertEqual(user.email, email)
		self.assertEqual(user.name, name)
		self.assertTrue(user.check_password(password))


class SignUpTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(
			email = 'test01@example.com',
			name  = 'test_name01',
			password = 'test1234'
		)
	
	def tearDown(self):
		User.objects.all().delete()

	def test_signup_post_success(self):
		data = {
			'email'   : 'test02@example.com',
			'name'    : 'test_name02',
			'password': 'test1234'
		}
		response = client.post('/user/signup', json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json(), {'message': 'SUCCESS'})

	def test_signup_post_key_error(self):
		data = {
			'email'   : 'test02@example.com',
			'password': 'test021234'
		}
		response = client.post('/user/signup', json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), {'message': 'KEY_ERROR'})

	def test_signup_post_user_already_exists(self):
		data = {
			'email'   : 'test01@example.com',
			'name'    : 'test_name01',
			'password': 'test1234'
		}
		response = client.post('/user/signup', json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 409)
		self.assertEqual(response.json(), {'message': 'USER_ALREADY_EXISTS'})
