from django.db import models
from django.utils import timezone


class GameSessions(models.Model):
    
    session_hash = models.CharField( max_length=10 )
    session_code = models.IntegerField( default=1234 )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.session_hash
