from django.urls import path

from question.views import QuestionView, QuestionDetailView


urlpatterns = [
    path('', QuestionView.as_view()),
    path('/<int:question_id>', QuestionDetailView.as_view()),
]
