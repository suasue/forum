from django.db import models

from user.models import User


class Question(models.Model):
    title      = models.CharField(max_length=255)
    content    = models.TextField(null=True)
    author     = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'questions'


class Comment(models.Model):
    content    = models.TextField()
    author     = models.ForeignKey('user.User', on_delete=models.CASCADE)
    question   = models.ForeignKey('Question', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'comments'


class QuestionLike(models.Model):
    user     = models.ForeignKey('user.User', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    class Meta:
        db_table = 'question_likes'
