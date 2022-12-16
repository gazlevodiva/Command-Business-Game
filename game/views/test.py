from django.shortcuts import HttpResponse, render
from django.http import HttpResponseBadRequest, JsonResponse 

from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Business import Business
from game.models.PlayersBusiness import PlayersBusiness
from game.models.CommandPayments import CommandPayments
from game.models.BusinessPayments import BusinessPayments

from game.methods.BusinessMethods import getCommandBank
from game.methods.BusinessMethods import getCommandPlayers
from game.methods.BusinessMethods import getBusinessPayments

from game.methods.PlayerMethods import getSalary
from game.methods.PlayerMethods import getInflation
from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import getBusinesses
from game.methods.PlayerMethods import getCommandBusinesses
from game.methods.PlayerMethods import getPlayerCategoties


from game.methods.NotificationModal import Modal

from django.core import serializers

from game.views.player_control import player_control


def test( request ):
    player = Player.objects.get( pk=80 )

    # Create Bootstrap Modal window
    print( getPlayerCategoties( player ) )
    

    return HttpResponse( getPlayerCategoties( player ) )
