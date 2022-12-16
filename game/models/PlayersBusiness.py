from django.db import models

from django.utils import timezone


from game.models.Player import Player
from game.models.Business import Business


class PlayersBusiness( models.Model ):

    BUSINESS_STATUS = (
        ('ACTIVE', 'Active'),
        ('SOLD', 'Sold'),
        ('DEFOULT', 'Defoult')
    )

    player       = models.ForeignKey( Player, null=True, on_delete=models.CASCADE )
    business     = models.ForeignKey( Business, on_delete=models.CASCADE )
    status       = models.CharField( max_length=10, choices=BUSINESS_STATUS, default='ACTIVE' )
    is_command   = models.BooleanField( default=False )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return f'''{self.player}: {self.business} - {self.status}'''
