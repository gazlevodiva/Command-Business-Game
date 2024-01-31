from django.http import JsonResponse
from game.models.Moves import Moves
from game.models.Player import Player
from game.methods.BusinessMethods import sellCommandShare
from game.decorators import check_user_session_hash


@check_user_session_hash
def sell_share(request, session, player_id, count):
    player = Player.objects.get(pk=player_id)
    moves = Moves.objects.filter(player=player)
    last_move = moves.last()
    new_move = Moves.objects.create(player=player, position=last_move.position)
    sellCommandShare(new_move, count)
    return JsonResponse({"result": True})
