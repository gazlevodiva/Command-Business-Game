from django.shortcuts import redirect

from game.models.Player import Player

from game.methods.BusinessMethods import sellCommandShare

from game.decorators import check_user_session_hash


@check_user_session_hash
def sell_share(request, player_id):

    player = Player.objects.get( pk=player_id )

    sellCommandShare( player, 50000 )

    return redirect(f"/player_control_{player_id}/")
