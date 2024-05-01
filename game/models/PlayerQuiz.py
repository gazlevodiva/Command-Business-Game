from django.db import models
from game.models.Actions import Actions
from game.models.Quiz import QuizQuestions
from game.models.Quiz import QuizAnswers
from django.utils import timezone


class PlayerQuiz(models.Model):
    action = models.ForeignKey(Actions, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.action.name


class PlayerQuizQuestions(models.Model):
    quiz = models.ForeignKey(PlayerQuiz, on_delete=models.CASCADE)
    answer = models.ForeignKey(QuizAnswers, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.ForeignKey(QuizQuestions, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question.name
