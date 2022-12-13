
from django.shortcuts import render

from game.models.Business import Business

def rules( request ):
    businesses = Business.objects.all()
    context = {
        'businesses': businesses
    }
    return render( request, 'game/rules.html', context)
