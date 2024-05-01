from django.db import models
from game.models.Business import Business
from django.utils import timezone


class QuizQuestions(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class QuizAnswers(models.Model):
    question = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, default='')
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
