from django.shortcuts import redirect

from game.methods.BusinessMethods import setDefoult

from game.models.PlayersBusiness import PlayersBusiness


def set_defoult(request, player_business_id):

    business = PlayersBusiness.objects.get( pk=player_business_id )
    
    setDefoult( business )

    return redirect("/")
