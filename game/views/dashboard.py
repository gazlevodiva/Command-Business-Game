from django.shortcuts import render

from game.models.Player import Player

from game.methods.BusinessMethods import getCommandPlayers
from game.methods.BusinessMethods import getCommandBank

from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import getActions
from game.methods.PlayerMethods import getBusinesses
from game.methods.PlayerMethods import getCommandBusinesses


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
                'command_businesses': command_businesses
            }
        )

    # Game actions
    actions = getActions()

    # Total command balance
    bank = getCommandBank()

    context = {
        'players':         players_info,
        'command_players': command_player_info,
        'command_bank':    bank,
        'actions':         actions[::-1][:10]
    }
    return render( request, 'game/dashboard.html', context)
