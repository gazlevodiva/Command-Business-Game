from django.shortcuts import render
from django.shortcuts import redirect

from game.models.Player import Player
from game.models.Actions import Actions

from game.decorators import check_user_session_hash


@check_user_session_hash
def new_player( request ):

    if request.method == 'POST':

        # Get player name from POST form
        player_name = request.POST['new_player_name'] 

        # Create new player
        new_player = Player.objects.create( name=player_name )        

        # Add default balance 60 000
        count = 60000
        name = f'''Начал игру - {count}'''
        Actions(
            player   = new_player,
            category = 'OTHER',
            name     = name,
            count    = count
        ).save()

        request_template = redirect( f"/player_control_{new_player.id}/" )
        request_template.set_cookie( 'game_session_controller', new_player.id )

        return request_template

    return render( request, 'game/new_player.html' )
