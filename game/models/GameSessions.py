from django.db import models
from django.utils import timezone
from datetime import datetime
import random
import hashlib


class GameSessions(models.Model):
    
    session_name = models.CharField( max_length=100 )
    session_hash = models.CharField( default="generated", max_length=10, unique=True )
    session_code = models.IntegerField( default=1234 )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.session_name
    
    def save(self, *args, **kwargs):
        input_string = self.session_name + str(datetime.timestamp(self.created_date))
        hash_object = hashlib.sha256(input_string.encode('utf-8'))
        hash_hex = hash_object.hexdigest()

        self.session_hash = hash_hex[:10]
        self.session_code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        super(GameSessions, self).save(*args, **kwargs)

        from game.models.Moves import Moves
        from game.models.Player import Player
        from game.models.Actions import Actions
        from game.models.CommandPayments import CommandPayments

        playerX_name = 'X'
        playerX_balance = 200000

        new_player = Player.objects.create(
            name         = playerX_name, 
            visible      = False, 
            game_session = self
        )

        move = Moves.objects.create(
            player = new_player,
            number = 0
        )

        CommandPayments.objects.create(
            move     = move,
            category = "DEPOSITE",
            count    = playerX_balance,
        )

        Actions.objects.create(
            move     = move,
            name     = f"Начал игру - {playerX_balance}",
            count    = playerX_balance,
            category = 'OTHER',
        )

        Actions.objects.create(
            move     = move,
            name     = f"Вложил в командный бизнес - {playerX_balance}",
            count    = -playerX_balance,
            category = 'CMND',
            is_command = True,
        )
