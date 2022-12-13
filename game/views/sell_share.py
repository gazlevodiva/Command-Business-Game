from django.shortcuts import redirect

from game.models.Player import Player

from game.methods.BusinessMethods import sellCommandShare


def sell_share(request, player_id):

    player = Player.objects.get( pk=player_id )

    sellCommandShare( player )

    return redirect(f"/player_control_{player_id}/")
