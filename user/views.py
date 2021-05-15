import json

from django.views import View
from django.http  import JsonResponse

from user.models   import User


class SingUpView(View):
	def post(self, request):
		data     = json.loads(request.body)
		email    = data.get('email', None)
		name     = data.get('name', None)
		password = data.get('password', None)

		if not (email and name and password):
			return JsonResponse({'message': 'KEY_ERROR'}, status=400)

		if User.objects.filter(email=email).exists():
			return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status=409)

		User.objects.create_user(email, name, password)

		return JsonResponse({'message': 'SUCCESS'}, status=201)
