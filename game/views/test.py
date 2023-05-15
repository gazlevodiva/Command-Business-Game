from django.shortcuts import HttpResponse, render
from django.http import HttpResponseBadRequest, JsonResponse 

from game.models.Player import Player
from game.models.Actions import Actions
from game.models.GameSessions import GameSessions
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



from django.db.models import Min
from django.db.models.functions import TruncSecond


def test( request ):

    session = GameSessions.objects.get( pk=19 )

    actions = Actions.objects.filter(game_session=session).exclude(player__name="X")
    grouped_actions = actions.annotate(truncated_time=TruncSecond('created_date')).values('truncated_time', 'player_id')


    for x in grouped_actions:
        print(x)

    return HttpResponse( actions )
