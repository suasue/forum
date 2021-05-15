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

		if not title:
			return JsonResponse({'message': 'KEY_ERROR'}, status=400)

		Question.objects.create(
			title   = title,
			content = content,
			author  = user
		)

		return JsonResponse({'message': 'SUCCESS'}, status=201)
