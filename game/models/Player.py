from django.db import models


class Player(models.Model):
    
    name    = models.CharField( max_length=200 )
    level   = models.IntegerField( default=1 )
    visible = models.BooleanField( default=True )

    def __str__(self):
        return self.name
