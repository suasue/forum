from django.urls import path

from question.views import QuestionView


urlpatterns = [
    path('', QuestionView.as_view()),
]
