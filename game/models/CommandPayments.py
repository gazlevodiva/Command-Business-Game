from django.db import models
from django.utils import timezone
from game.models.Moves import Moves


class CommandPayments(models.Model):

    COMMAND_PAYMENTS_CATEGORY = (
        ('SURP', 'command_surprise'),
        ('SELL_BIS', 'sell_business'),
        ('DEPOSITE', 'new_deposite'),
        ('WITHDRAW', 'withdraw_deposite'),
        ('BUY_BIS', 'buy_business'),
        ('OTHER', 'other'),
    )

    move = models.ForeignKey(Moves, null=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=8, choices=COMMAND_PAYMENTS_CATEGORY, default='OTHER' )
    count = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'''{self.count}'''
