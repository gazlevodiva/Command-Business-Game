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

from game.methods.NotificationModal import Modal

from django.core import serializers

from game.views.player_control import player_control


def test( request ):
    player = Player.objects.get( pk=59 )

    # Create Bootstrap Modal window
    modal = Modal("Удачно прошел круг!", player)
    modal.type = "new_level"

    inflation_action = getInflation( player )
    salary_action    = getSalary( player )

    modal.add_action( inflation_action )
    modal.add_action( salary_action )
    

    return player_control( 
        request   = request, 
        player_id = player.id, 
        modal     = modal 
    )
