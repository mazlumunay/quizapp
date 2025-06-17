from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Question(models.Model):
    """Model for quiz questions with multiple choice options."""
    
    question = models.CharField(max_length=500, help_text="The question text")
    option_one = models.CharField(max_length=200, help_text="First option")
    option_two = models.CharField(max_length=200, help_text="Second option")
    option_three = models.CharField(max_length=200, help_text="Third option")
    option_four = models.CharField(max_length=200, help_text="Fourth option")
    answer = models.CharField(max_length=200, help_text="Correct answer")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"Q: {self.question[:50]}..."

    def get_options(self):
        """Return all options as a list."""
        return [self.option_one, self.option_two, self.option_three, self.option_four]


class Result(models.Model):
    """Model to store quiz results for users."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    score_percentage = models.FloatField(default=0.0)
    date_taken = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_taken']
        verbose_name = "Result"
        verbose_name_plural = "Results"

    def __str__(self):
        return f"{self.user.username} - {self.correct_answers}/{self.total_questions}"

    @property
    def total(self):
        """Alias for total_questions for template compatibility."""
        return self.total_questions
    
    @property
    def got(self):
        """Alias for correct_answers for template compatibility."""
        return self.correct_answers

    def calculate_percentage(self):
        """Calculate and update score percentage."""
        if self.total_questions > 0:
            self.score_percentage = (self.correct_answers / self.total_questions) * 100
        else:
            self.score_percentage = 0.0
        return self.score_percentage