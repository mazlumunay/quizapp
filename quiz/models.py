from django.db import models
from django.contrib.auth.models import User

# Models for quiz questions and user results

class Question(models.Model):
    """
    Model representing a quiz question.

    Fields:
    - question: CharField representing the question itself.
    - answer: CharField representing the correct answer.
    - option_one: CharField representing the first option.
    - option_two: CharField representing the second option.
    - option_three: CharField representing the third option (optional).
    - option_four: CharField representing the fourth option (optional).
    - created_at: DateTimeField representing the creation date of the question.
    - updated_at: DateTimeField representing the last update date of the question.
    """
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=100)
    option_one = models.CharField(max_length=100)
    option_two = models.CharField(max_length=100)
    option_three = models.CharField(max_length=100, blank=True)
    option_four = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class Result(models.Model):
    """
    Model representing a user's quiz result.

    Fields:
    - user: ForeignKey to User model representing the user who took the quiz.
    - total: IntegerField representing the total number of questions attempted.
    - got: IntegerField representing the number of questions answered correctly.
    - created_at: DateTimeField representing the creation date of the result.
    - updated_at: DateTimeField representing the last update date of the result.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    total = models.IntegerField(blank=False)
    got = models.IntegerField(blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
