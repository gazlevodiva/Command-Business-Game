
from random import choice

from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Surprises import Surprises
from game.methods.NotificationModal import Modal

from game.views.player_control import player_control

from game.methods.PlayerMethods import getPlayerCategoties

from itertools import chain


def surprise( request, player_id, surprise_type ):
    player = Player.objects.get( pk=player_id )


    if surprise_type == 'surp':
        all_categories = getPlayerCategoties( player )

    if surprise_type == 'memo':
        all_categories = ['MEMO']

    if surprise_type == 'cmnd':
        all_categories = ['COMMAND']


    surprise_list = []
    all_surprises  = Surprises.objects.all()
    for surp_category  in all_categories:
        surprises = all_surprises.filter( category=surp_category )

        if len( surprises ) > 0:
            for surp in surprises:
                surprise_list.append( surp )

    # Random surprise from surprise_list
    if len( surprise_list ) == 0:
        surprise = choice( all_surprises )

    if len( surprise_list ) > 0:
        surprise = choice( surprise_list )




    if surprise_type == 'surp':
        action_name    = f'Сюрприз - "{surprise.name}" {surprise.count}.'
        modal_name     = "Сюрпрайз!"
        modal          = Modal( modal_name, player )
        modal.surprise = surprise
        modal.type     = "surprise"

    if surprise_type == 'cmnd':
        action_name    = f'Сюрприз - "{surprise.name}" {surprise.count}.'
        modal_name     = "Сюрпрайз!"
        modal          = Modal( modal_name, player )
        modal.surprise = surprise
        modal.type     = "command"

    if surprise_type == 'memo':
        action_name    = surprise.name
        modal_name     = "Мемори!"
        modal          = Modal( modal_name, player )
        modal.surprise = surprise
        modal.type     = "memory"

    
    Actions(
        player   = player,
        name     = action_name,
        count    = surprise.count,
        category = 'SURP',
    ).save()

    return player_control( 
        request   = request, 
        player_id = player_id, 
        modal     = modal 
    )
