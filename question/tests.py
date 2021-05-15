import json
import jwt
from datetime import datetime

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
		cls.question1 = Question.objects.create(
			id         = 1,
			title      = 'test_title01',
			content    = 'test_content01',
			author     = user,
			created_at = '2021-05-16 17:30:00'
		)
		cls.question2 = Question.objects.create(
			id         = 2,
			title      = 'test_title02',
			content    = 'test_content02',
			author     = user,
			created_at = '2021-05-16 19:00:00'
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

	def test_question_post_key_error1(self):
		headers = {'HTTP_Authorization': self.access_token}
		data = {
			'content': 'test_content'
		}
		response = client.post('/question', json.dumps(data), content_type='application/json', **headers)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), {'message': 'KEY_ERROR'})

	def test_question_post_key_error2(self):
		headers = {'HTTP_Authorization': self.access_token}
		data = {
			'title'  : '',
			'content': 'test_content'
		}
		response = client.post('/question', json.dumps(data), content_type='application/json', **headers)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), {'message': 'KEY_ERROR'})

	def test_question_get_success(self):
		response = client.get('/question', content_type='application/json')
		self.assertEqual(response.json(), {
			'questions': [
				{
					'id'        : 1,
					'title'     : 'test_title01',
					'content'   : 'test_content01',
					'author'    : 'test_name01',
					'created_at': self.question1.created_at.strftime('%Y-%m-%d %H:%M:%S')
				},
				{
					'id'        : 2,
					'title'     : 'test_title02',
					'content'   : 'test_content02',
					'author'    : 'test_name01',
					'created_at': self.question2.created_at.strftime('%Y-%m-%d %H:%M:%S')
				}
			]
		})
		self.assertEqual(response.status_code, 200)


class QuestionDetailTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		user1 = User.objects.create_user(
			email    = 'test01@example.com',
			name     = 'test_name01',
			password = 'test1234'
		)
		user2 = User.objects.create_user(
			email    = 'test02@example.com',
			name     = 'test_name02',
			password = 'test1234'
		)
		cls.question = Question.objects.create(
			id         = 1,
			title      = 'test_title01',
			content    = 'test_content01',
			author     = user1,
			created_at = '2021-05-16 17:30:00'
		)
		Question.objects.create(
			id         = 2,
			title      = 'test_title02',
			content    = 'test_content02',
			author     = user2,
			created_at = '2021-05-16 19:00:00'
		)
		
		cls.access_token1 = jwt.encode({'id': user1.id}, SECRET_KEY, algorithm=ALGORITHM)
		cls.access_token2 = jwt.encode({'id': user2.id}, SECRET_KEY, algorithm=ALGORITHM)
	
	def tearDown(self):
		User.objects.all().delete()

	def test_question_detail_put_success(self):
		headers = {'HTTP_Authorization': self.access_token1}
		data = {
			'title'  : 'modified_title',
			'content': 'modified_content'
		}
		response = client.put('/question/1', json.dumps(data), content_type='application/json', **headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'message': 'SUCCESS'})

	def test_question_detail_put_key_error1(self):
		headers = {'HTTP_Authorization': self.access_token1}
		data = {
			'title'  : 'modified_title',
		}
		response = client.put('/question/1', json.dumps(data), content_type='application/json', **headers)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), {'message': 'KEY_ERROR'})

	def test_question_detail_put_key_error2(self):
		headers = {'HTTP_Authorization': self.access_token1}
		data = {
			'title'  : 'modified_title',
			'content': ''
		}
		response = client.put('/question/1', json.dumps(data), content_type='application/json', **headers)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), {'message': 'KEY_ERROR'})

	def test_question_detail_put_question_does_not_exist(self):
		headers = {'HTTP_Authorization': self.access_token1}
		data = {
			'title'  : 'modified_title',
			'content': 'modified_content'
		}
		response = client.put('/question/3', json.dumps(data), content_type='application/json', **headers)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.json(), {'message': 'QUESTION_DOES_NOT_EXIST'})

	def test_question_detail_put_invalid_user(self):
		headers = {'HTTP_Authorization': self.access_token2}
		data = {
			'title'  : 'modified_title',
			'content': 'modified_content'
		}
		response = client.put('/question/1', json.dumps(data), content_type='application/json', **headers)
		self.assertEqual(response.status_code, 401)
		self.assertEqual(response.json(), {'message': 'INVALID_USER'})

	def test_question_detail_delete_success(self):
		headers = {'HTTP_Authorization': self.access_token1}
		response = client.delete('/question/1', content_type='application/json', **headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'message': 'SUCCESS'})

	def test_question_detail_delete_question_does_not_exist(self):
		headers = {'HTTP_Authorization': self.access_token1}
		response = client.delete('/question/3', content_type='application/json', **headers)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.json(), {'message': 'QUESTION_DOES_NOT_EXIST'})

	def test_question_detail_delete_invalid_user(self):
		headers = {'HTTP_Authorization': self.access_token2}
		response = client.delete('/question/1', content_type='application/json', **headers)
		self.assertEqual(response.status_code, 401)
		self.assertEqual(response.json(), {'message': 'INVALID_USER'})
	
	def test_question_detail_get_success(self):
		response = client.get('/question/1', content_type='application/json')
		self.assertEqual(response.json(), {
			'question': {
				'id'        : 1,
				'title'     : 'test_title01',
				'content'   : 'test_content01',
				'author'    : 'test_name01',
				'created_at': self.question.created_at.strftime('%Y-%m-%d %H:%M:%S')
			}
		})
		self.assertEqual(response.status_code, 200)

	def test_question_detail_get_question_does_not_exist(self):
		headers = {'HTTP_Authorization': self.access_token1}
		response = client.get('/question/3', content_type='application/json', **headers)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.json(), {'message': 'QUESTION_DOES_NOT_EXIST'})
