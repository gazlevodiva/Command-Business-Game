from django.shortcuts import redirect

from game.models.Moves import Moves
from game.models.PlayersBusiness import PlayersBusiness

from game.decorators import check_user_session_hash

from game.methods.PlayerMethods import sell_personal_business
from game.methods.PlayerMethods import sell_command_business


@check_user_session_hash
def sell_business(request, session, player_business_id):
    players_business = PlayersBusiness.objects.get(pk=player_business_id)
    player = players_business.player

    last_move = Moves.objects.filter(player=player).last()
    move = Moves.objects.create(player=player, position=last_move.position)

    if players_business.is_command:
        sell_command_business(move, players_business)

    if not players_business.is_command:
        sell_personal_business(move, players_business)

    return redirect(f"/player_control_{ player.id }/")
