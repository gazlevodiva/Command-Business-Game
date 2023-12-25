from django.db import models
from django.utils import timezone

from game.models.Actions import Actions
from game.models.Surprises import Surprises

class MemoryAnswers(models.Model):
    
    action       = models.ForeignKey( Actions, null=True, on_delete=models.CASCADE )
    question     = models.ForeignKey( Surprises, null=True, on_delete=models.CASCADE )
    answer       = models.CharField( max_length=512, default='' )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return f'''{self.action}: {self.question}'''
