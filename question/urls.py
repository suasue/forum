from django.urls import path

from question.views import (
	QuestionView, 
	QuestionDetailView, 
	CommentView,
	QuestionLikeView,
	BestQuestionView
)


urlpatterns = [
    path('', QuestionView.as_view()),
    path('/<int:question_id>', QuestionDetailView.as_view()),
    path('/<int:question_id>/comment', CommentView.as_view()),
    path('/<int:question_id>/like', QuestionLikeView.as_view()),
    path('/<int:question_id>/best', BestQuestionView.as_view()),
]
