from django.db import models
from django.utils import timezone
from game.models.Moves import Moves
from game.models.PlayersBusiness import PlayersBusiness


class PlayersBusinessStatus( models.Model ):
    BUSINESS_STATUS = (
        ('ACTIVE', 'Active'),
        ('VOTING', 'Voting'),
        ('UNVOTE', 'Voting failed'),
        ('SOLD', 'Sold'),
        ('DEFOULT', 'Defoult'),
    )

    players_business = models.ForeignKey(PlayersBusiness, on_delete=models.CASCADE)
    move = models.ForeignKey(Moves, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=BUSINESS_STATUS, default='ACTIVE')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.status
