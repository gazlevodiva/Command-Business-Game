from django.http import JsonResponse

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.GameSessions import GameSessions

from game.methods.PlayerMethods import who_is_turn
from game.methods.BusinessMethods import get_votion
from game.methods.BusinessMethods import player_id_for_votion

from game.decorators import check_user_session_hash
from django.shortcuts import get_object_or_404
from typing import Any, Dict


@check_user_session_hash
def whois_turn_data(
    request,
    session: GameSessions,
    player_id: int
) -> JsonResponse:
    """
    Provides data about whose turn it is in the current game session.

    Args:
    request: HttpRequest object.
    session: Current game session object.
    player_id: ID of the player making the request.

    Returns:
    JsonResponse: Data about the current player's turn.
    """
    player_turn_id: int = who_is_turn(session)

    player_turn: Player = get_object_or_404(Player, pk=player_turn_id)
    player_turn_last_move: Moves = Moves.objects.filter(
        player=player_turn
    ).last()

    if not player_turn_last_move:
        return JsonResponse(
            {"error": "No moves found for the current player."},
            status=404
        )

    context: Dict[str, Any] = {
        "move_id": player_turn_last_move.id,
        "move_number": player_turn_last_move.number,
        "player_id": player_turn.id,
        "player_name": player_turn.name,
        "votion": False
    }

    if player_id in player_id_for_votion(player_turn.game_session):
        context["votion"] = get_votion(player_turn_last_move)

    return JsonResponse(context)
