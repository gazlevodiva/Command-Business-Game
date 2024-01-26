from django.http import JsonResponse

from game.models.Moves import Moves
from game.models.Player import Player

from game.methods.PlayerMethods import playerTurn
from game.methods.BusinessMethods import getVotion
from game.methods.BusinessMethods import playerIdForVotion

from game.decorators import check_user_session_hash


@check_user_session_hash
def whois_turn_data(request, session, player_id):
    player_turn_id = playerTurn(session)
    player_turn = Player.objects.get(pk=player_turn_id)
    player_turn_last_move = Moves.objects.filter(player=player_turn).last()

    context = {}
    context["move_id"] = player_turn_last_move.id
    context["move_number"] = player_turn_last_move.number
    context["player_id"] = player_turn.id
    context["player_name"] = player_turn.name

    if player_id in playerIdForVotion(player_turn.game_session):
        context["votion"] = getVotion(player_turn_last_move)
    else:
        context["votion"] = False

    return JsonResponse(context)
