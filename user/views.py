import json
import jwt 

from django.views import View
from django.http  import JsonResponse

from user.models import User
from forum.settings import SECRET_KEY, ALGORITHM


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


class SignInView(View):
	def post(self, request):
		data     = json.loads(request.body)
		email    = data.get('email', None)
		password = data.get('password', None)

		if not (email and password):
			return JsonResponse({'message': 'KEY_ERROR'}, status=400)

		if not User.objects.filter(email=email).exists():
			return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=404)

		user = User.objects.get(email=email)
		
		if not user.check_password(password):
			return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
		
		access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
				
		return JsonResponse({'message': 'SUCCESS', 'Authorization': access_token}, status=200)
