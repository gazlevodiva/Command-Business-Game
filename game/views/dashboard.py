from django.shortcuts import render

from game.models.Player import Player
from game.models.GameSessions import GameSessions

from game.methods.BusinessMethods import getCommandPlayers
from game.methods.BusinessMethods import getCommandBank

from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import getActions
from game.methods.PlayerMethods import getBusinesses
from game.methods.PlayerMethods import getCommandBusinesses

from game.decorators import check_user_session_hash
from django.contrib.auth.decorators import login_required


@login_required( login_url='/login/' )
@check_user_session_hash
def dashboard( request=None, session=None ):

    players = Player.objects.filter( 
        visible      = True, 
        game_session = session 
    )

    # Info about players business
    players_info = []

    for player in players:

        businesses = getBusinesses( player ) 
        balance    = getBalance( player )
        players_info.append(
            {
                'player':     player,
                'balance':    balance,
                'businesses': businesses,
            }
        )

    # Command player info
    command_players = getCommandPlayers( session )   

    # Info about command businesses
    command_player_info = [] 

    for command_player in command_players:
        
        command_businesses = getCommandBusinesses( command_player['move__player'] )

        command_player_info.append(
            {
                'command_player':     command_player,
                'command_businesses': command_businesses,
            }
        )

    # Game actions
    actions = getActions( session )

    # Total command balance
    bank = getCommandBank( session )

    context = {
        'players':         players_info,
        'command_players': command_player_info,
        'command_bank':    bank,
        'actions':         actions[::-1][:12],
        'session':         session,        
    }

    if request is None:
        return context

    return render( request, 'game/dashboard.html', context)
