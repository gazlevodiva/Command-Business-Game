from django.shortcuts import render
from django.shortcuts import redirect

from game.models.Player import Player
from game.models.Actions import Actions


def new_player( request ):

    if request.method == 'POST':

        # Get player name from POST form
        player_name = request.POST['new_player_name'] 

        # Create new player
        new_player = Player( name=player_name )        
        new_player.save()

        # Add default balance 60 000
        count = 60000
        name = f'''Начал игру - {count}'''
        Actions(
            player = new_player,
            name   = name,
            count  = count
        ).save()

        return redirect( f"/player_control_{new_player.id}/" )

    return render( request, 'game/new_player.html' )
