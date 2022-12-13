from django.db import models

from django.utils import timezone

from game.models.PlayersBusiness import PlayersBusiness


class BusinessPayments( models.Model ):

    player_business     = models.ForeignKey( PlayersBusiness, on_delete=models.CASCADE )
    count               = models.IntegerField( default=0 )
    rentability         = models.IntegerField()
    defoult_probability = models.IntegerField()
    player_level        = models.IntegerField()
    created_date        = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return f'''{self.player_business.player}: {self.player_business.business}'''
