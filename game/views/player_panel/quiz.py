from django.http import JsonResponse
from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.decorators import check_user_session_hash
from game.methods.quiz_methods import get_or_set_quiz
from django.shortcuts import get_object_or_404


@check_user_session_hash
def get_quiz(request, session, player_id):

    # Get player
    player = get_object_or_404(Player, pk=player_id)
    player_last_move = Moves.objects.filter(player=player).last()

    context = {
        "quiz": get_or_set_quiz(player_last_move),
    }
    return JsonResponse(context)
