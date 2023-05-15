from django.shortcuts import redirect

from game.models.Moves import Moves
from game.models.Player import Player

from game.methods.BusinessMethods import sellCommandShare

from game.decorators import check_user_session_hash


@check_user_session_hash
def sell_share(request, session, player_id, count):

    player = Player.objects.get( pk=player_id )
    move = Moves.objects.create( player=player )

    sellCommandShare( move, count )

    return redirect(f"/player_control_{ player.id }/")
