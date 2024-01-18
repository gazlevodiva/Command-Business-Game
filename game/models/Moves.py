from django.db import models
from django.utils import timezone
from django.db.models import Max

from game.models.Player import Player


class Moves(models.Model):
    
    number = models.IntegerField(blank=True)
    player = models.ForeignKey(Player, default=None, on_delete=models.CASCADE)
    position = models.IntegerField(default=None)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"""{ self.player.name } делает { self.number } ход. """

    def save(self, *args, **kwargs):
        if self.number is None and self.number != 0:
            self.number = self.get_next_move_number()

        if not self.position:
            current_position = Moves.objects.filter(player=self.player).last()

            if not current_position:
                self.position = 1

            if current_position:
                self.position = current_position.position

        super(Moves, self).save(*args, **kwargs)

    def get_next_move_number(self):
        max_move_number = Moves.objects.filter(
            player__game_session=self.player.game_session
        ).aggregate(Max("number"))["number__max"]

        if max_move_number is None:
            return 1

        return max_move_number + 1
