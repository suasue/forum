import json
from datetime import datetime

from django.views import View
from django.http  import JsonResponse

from question.models import Comment, Question
from user.utils      import login_decorator


class QuestionView(View):
	@login_decorator
	def post(self, request):
		user    = request.user
		data    = json.loads(request.body)
		title   = data.get('title', None)
		content = data.get('content', None)

		if not (title and content):
			return JsonResponse({'message': 'KEY_ERROR'}, status=400)

		Question.objects.create(
			title   = title,
			content = content,
			author  = user
		)

		return JsonResponse({'message': 'SUCCESS'}, status=201)

	def get(self, request):
		questions = Question.objects.all()

		question_list = [{
			'id'        : question.id,
			'title'     : question.title,
			'content'   : question.content,
			'author'    : question.author.name,
			'created_at': question.created_at.strftime('%Y-%m-%d %H:%M:%S')
			} for question in questions
		]

		return JsonResponse({'questions': question_list}, status=200)


class QuestionDetailView(View):
	@login_decorator
	def put(self, request, question_id):
		user    = request.user
		data    = json.loads(request.body)
		title   = data.get('title', None)
		content = data.get('content', None)

		if not (title and content):
			return JsonResponse({'message': 'KEY_ERROR'}, status=400)
		
		if not Question.objects.filter(id=question_id).exists():
			return JsonResponse({'message': 'QUESTION_DOES_NOT_EXIST'}, status=404)

		question = Question.objects.get(id=question_id)

		if user != question.author:
			return JsonResponse({'message':'INVALID_USER'}, status=401)

		question.title   = title
		question.content = content
		question.save()

		return JsonResponse({'message': 'SUCCESS'}, status=200)

	@login_decorator
	def delete(self, request, question_id):
		user    = request.user

		if not Question.objects.filter(id=question_id).exists():
			return JsonResponse({'message': 'QUESTION_DOES_NOT_EXIST'}, status=404)

		question = Question.objects.get(id=question_id)

		if user != question.author:
			return JsonResponse({'message':'INVALID_USER'}, status=401)
		
		question.delete()

		return JsonResponse({'message': 'SUCCESS'}, status=200)
	
	def get(self, request, question_id):
		if not Question.objects.filter(id=question_id).exists():
			return JsonResponse({'message': 'QUESTION_DOES_NOT_EXIST'}, status=404)
		
		question = Question.objects.get(id=question_id)

		question_detail = {
			'id'        : question.id,
			'title'     : question.title,
			'content'   : question.content,
			'author'    : question.author.name,
			'created_at': question.created_at.strftime('%Y-%m-%d %H:%M:%S')
		}

		return JsonResponse({'question': question_detail}, status=200)


class CommentView(View):
	@login_decorator
	def post(self, request, question_id):
		user    = request.user
		data    = json.loads(request.body)
		content = data.get('content', None)

		if not content:
			return JsonResponse({'message': 'KEY_ERROR'}, status=400)

		if not Question.objects.filter(id=question_id).exists():
			return JsonResponse({'message': 'QUESTION_DOES_NOT_EXIST'}, status=404)

		Comment.objects.create(
			content     = content,
			author      = user,
			question_id = question_id
		)

		return JsonResponse({'message': 'SUCCESS'}, status=201)
