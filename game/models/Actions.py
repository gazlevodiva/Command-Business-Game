from django.db import models
from django.utils import timezone

from game.models.Player import Player


class Actions(models.Model):

    ACTIONS_CATEGORY = (
        ('SLR', 'salary'),
        ('CMND', 'command'),
        ('BSNS', 'business'),
        ('SURP', 'surprise'),
        ('INFL', 'inflation'),
        ('OTHER', 'other')
    )
    
    player       = models.ForeignKey( Player, on_delete=models.CASCADE )
    name         = models.CharField( max_length=200 )
    count        = models.IntegerField( default=0 )
    category     = models.CharField( max_length=6, choices=ACTIONS_CATEGORY, default='OTHER' )
    is_command   = models.BooleanField( default=False )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return f'''{self.player.name}: {self.name}'''
