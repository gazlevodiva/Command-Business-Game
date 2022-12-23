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

@check_user_session_hash
def dashboard( request ):

    players = Player.objects.filter( visible=True )

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
    command_players = getCommandPlayers()   

    # Info about command businesses
    command_player_info = [] 

    for command_player in command_players:
        
        command_businesses = getCommandBusinesses( command_player['player'] )

        command_player_info.append(
            {
                'command_player':     command_player,
                'command_businesses': command_businesses,
            }
        )

    # Game actions
    actions = getActions()

    # Total command balance
    bank = getCommandBank()

    session_info = GameSessions.objects.latest( 'created_date' )
    session_link = f'{request.get_host()}/s/{session_info.session_hash}'
    session_code = session_info.session_code

    context = {
        'players':         players_info,
        'command_players': command_player_info,
        'command_bank':    bank,
        'actions':         actions[::-1][:9],
        'session_code':    session_code,
        'session_link':    session_link,
        
    }
    return render( request, 'game/dashboard.html', context)
