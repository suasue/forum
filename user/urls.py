from django.urls import path

from user.views import SingUpView, SignInView


urlpatterns = [
    path('/signup', SingUpView.as_view()),
	path('/signin', SignInView.as_view()),
]
