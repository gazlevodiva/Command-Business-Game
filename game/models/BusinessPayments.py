from django.db import models

from django.utils import timezone

from game.models.Moves import Moves
from game.models.PlayersBusiness import PlayersBusiness


class BusinessPayments( models.Model ):

    move                = models.ForeignKey( Moves, null=True, on_delete=models.CASCADE )
    player_business     = models.ForeignKey( PlayersBusiness, null=True, on_delete=models.CASCADE )
    count               = models.IntegerField( default=0 )
    rentability         = models.IntegerField()
    defoult_probability = models.IntegerField()
    player_level        = models.IntegerField()    
    created_date        = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return f'''{self.move.player}: {self.player_business}'''
    