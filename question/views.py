import json
from datetime import datetime

from django.views               import View
from django.http                import JsonResponse
from django.db.models           import Q, Count

from question.models import Comment, Question, QuestionLike
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
		keyword = request.GET.get('keyword', None)

		questions = Question.objects.prefetch_related('author')

		if keyword:
			questions = questions.filter(
				Q(title__icontains=keyword) | Q(content__icontains=keyword)
			)

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
		user = request.user

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

	def get(self, request, question_id):
		if not Question.objects.filter(id=question_id).exists():
			return JsonResponse({'message': 'QUESTION_DOES_NOT_EXIST'}, status=404)

		comments = Comment.objects.filter(question_id=question_id)

		comment_list = [{
			'id'        : comment.id,
			'content'   : comment.content,
			'author'    : comment.author.name,
			'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
			} for comment in comments 
		]

		return JsonResponse({'comments': comment_list}, status=200)


class QuestionLikeView(View):
	@login_decorator
	def post(self, request, question_id):
		user = request.user
		if not Question.objects.filter(id=question_id).exists():
			return JsonResponse({'message': 'QUESTION_DOES_NOT_EXIST'}, status=404)

		if QuestionLike.objects.filter(user=user, question_id=question_id).exists():
			QuestionLike.objects.filter(user=user, question_id=question_id).delete()
			like_count = QuestionLike.objects.filter(question_id=question_id).count()

			return JsonResponse({'message': 'SUCCESS', 'like_count': like_count}, status=200)
			
		QuestionLike.objects.create(user=user, question_id=question_id)
		like_count = QuestionLike.objects.filter(question_id=question_id).count()

		return JsonResponse({'message': 'SUCCESS', 'like_count': like_count}, status=201)


class BestQuestionView(View):
	def get(self, request, question_id):
		if not Question.objects.filter(id=question_id).exists():
			return JsonResponse({'message': 'QUESTION_DOES_NOT_EXIST'}, status=404)

		question      = Question.objects.get(id=question_id)
		questions     = Question.objects.filter(created_at__month=question.created_at.month)
		best_question = questions.annotate(like_count=Count('questionlike')).order_by('-like_count')[0]
		
		best_question_detail = {
			'id'        : best_question.id,
			'title'     : best_question.title,
			'content'   : best_question.content,
			'author'    : best_question.author.name,
			'created_at': best_question.created_at.strftime('%Y-%m-%d %H:%M:%S'),
			'like_count': best_question.like_count
		}

		return JsonResponse({'best_question': best_question_detail}, status=200)
