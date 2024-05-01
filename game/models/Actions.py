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
        ('MEMO', 'memory'),
        ('INFL', 'inflation'),
        ('NLWL', 'new_level'),
        ('OTHER', 'other'),
        ('POSITION', 'position'),
        ('GAMESTART', 'gamestart'),
        ('DICE_VALUE', 'dice value'),
        ('START_VOTE', 'start vote'),
        ('VOTE_FOR', 'vote for'),
        ('VOTE_AGN', 'vote against'),
        ('QUIZ', 'quiz'),
    )

    MOVE_STAGE = (
        ('START', 'start'),
        ('CONTINUE', 'continue'),
        ('END', 'end'),
        ('-', 'none'),
    )

    move = models.ForeignKey(Moves, null=True, on_delete=models.CASCADE) 
    move_stage = models.CharField(max_length=9, choices=MOVE_STAGE, default='CONTINUE', null=True)
    name = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
    category = models.CharField(max_length=10, choices=ACTIONS_CATEGORY, default='OTHER')
    is_personal = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    is_command = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if not self.move:
            return f'''{self.name}'''
        return f'''{self.move.player.name}: {self.name}'''
