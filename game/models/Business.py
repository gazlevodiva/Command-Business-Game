from django.db import models


class Business(models.Model):
    
    BUSINESS_CATEGORY = (
        ('HORECA', 'horeca'),
        ('REALTY', 'realty'),
        ('SCIENCE', 'science'),
        ('IT', 'IT')
    )

    name     = models.CharField( max_length=200 )    
    category = models.CharField( max_length=10, choices=BUSINESS_CATEGORY )
    cost     = models.IntegerField()
    min_rent = models.IntegerField()
    max_rent = models.IntegerField()
    default  = models.IntegerField( default=7 )

    def __str__(self):
        return self.name
