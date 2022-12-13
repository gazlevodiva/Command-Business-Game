from django.db import models


class Business(models.Model):
    
    name     = models.CharField( max_length=200 )
    cost     = models.IntegerField()
    min_rent = models.IntegerField()
    max_rent = models.IntegerField()
    default  = models.IntegerField( default=7 )

    def __str__(self):
        return self.name
