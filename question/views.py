import json

from django.views import View
from django.http  import JsonResponse

from question.models import Question
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
