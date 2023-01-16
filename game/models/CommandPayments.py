from django.db import models

from django.utils import timezone

from game.models.Player import Player


class CommandPayments( models.Model ):
    
    player       = models.ForeignKey( Player, null=True, on_delete=models.CASCADE )
    count        = models.IntegerField()
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return f'{self.player}: {self.count}'
