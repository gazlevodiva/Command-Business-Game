from django.db import models

from game.models.Player import Player
from game.models.Business import Business


class Surprises( models.Model ):

    SURPRISE_CATEGORY = (
        ('PERSONAL', 'personal'),
        ('COMMAND', 'command'),
        ('HORECA', 'horeca'),
        ('REALTY', 'realty'),
        ('SCIENCE', 'science'),
        ('IT', 'IT'),
        ('MEMO', 'memory')
    )

    category   = models.CharField( max_length=10, choices=SURPRISE_CATEGORY, default='PERSONAL' )
    name       = models.CharField( max_length=200 )
    count      = models.IntegerField( default=0 )
    is_command = models.BooleanField( default=False )

    def __str__(self):
        return f'{self.name} {self.count}'
