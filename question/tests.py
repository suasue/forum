import json
import jwt

from django.test import TestCase, Client

from question.models import Question
from user.models     import User
from forum.settings  import SECRET_KEY, ALGORITHM


client = Client()

class QuestionTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		user = User.objects.create_user(
			email    = 'test01@example.com',
			name     = 'test_name01',
			password = 'test1234'
		)
		
		cls.access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
	
	def tearDown(self):
		User.objects.all().delete()

	def test_question_post_success(self):
		headers = {'HTTP_Authorization': self.access_token}
		data = {
			'title'  : 'test_title',
			'content': 'test_content'
		}
		response = client.post('/question', json.dumps(data), content_type='application/json', **headers)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json(), {'message': 'SUCCESS'})

	def test_question_post_key_error(self):
		headers = {'HTTP_Authorization': self.access_token}
		data = {
			'content': 'test_content'
		}
		response = client.post('/question', json.dumps(data), content_type='application/json', **headers)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), {'message': 'KEY_ERROR'})
