from django.db import models
from game.models.GameSessions import GameSessions

class Player(models.Model):
    
    name    = models.CharField( max_length=8 )
    level   = models.IntegerField( default=1 )
    visible = models.BooleanField( default=True )
    game_session = models.ForeignKey( GameSessions, default=3, on_delete=models.CASCADE )

    def __str__(self):
        return self.name
