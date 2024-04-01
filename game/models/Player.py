from django.db import models
from game.models.GameSessions import GameSessions
from django.utils import timezone


class Player(models.Model):
    name = models.CharField(max_length=16)
    icon = models.CharField(max_length=8, default='')
    level = models.IntegerField(default=1)
    visible = models.BooleanField(default=True)
    game_session = models.ForeignKey(GameSessions, default=3, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
