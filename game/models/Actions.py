from django.db import models
from django.utils import timezone

from game.models.Moves import Moves

class Actions(models.Model):

    ACTIONS_CATEGORY = (
        ('SLR', 'salary'),
        ('CMND', 'command'),
        ('BSNS', 'business'),
        ('BUY_BIS', 'buy_business'),
        ('SELL_BIS', 'sell_business'),
        ('DEF_BIS', 'defoult_business'),
        ('SURP', 'surprise'),
        ('INFL', 'inflation'),
        ('NLWL', 'new_level'),
        ('OTHER', 'other'),
    )
    
    move         = models.ForeignKey( Moves, null=True, on_delete=models.CASCADE )
    name         = models.CharField( max_length=200 )
    count        = models.IntegerField( default=0 )
    category     = models.CharField( max_length=9, choices=ACTIONS_CATEGORY, default='OTHER' )
    is_command   = models.BooleanField( default=False )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        if not self.move:
            return f'''{self.name}'''
        return f'''{self.move.player.name}: {self.name}'''

