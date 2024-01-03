from django.http import JsonResponse

from game.models.Moves import Moves
from game.models.Player import Player

from game.methods.BusinessMethods import getVotion
from game.methods.BusinessMethods import setNewVote

from game.decorators import check_user_session_hash


@check_user_session_hash
def set_vote(request, session, move_id, player_id, vote_category):
    move = Moves.objects.get(pk=move_id)
    player = Player.objects.get(pk=player_id)
    vote_res = setNewVote(move, player, vote_category)
    context = {"vote_move_id": move_id, "vote_res": vote_res}
    return JsonResponse(context)


@check_user_session_hash
def get_votion_data(request, session, move_id):
    move = Moves.objects.get(pk=move_id)
    votion = getVotion(move)
    context = {"votion": votion}
    return JsonResponse(context)
