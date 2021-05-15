from django.urls import path

from user.views      import SingUpView


urlpatterns = [
    path('/signup', SingUpView.as_view()),
]
