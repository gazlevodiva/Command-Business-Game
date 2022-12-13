
import os

import json

from random import choice

from game.models.Player import Player
from game.models.Actions import Actions
from game.methods.NotificationModal import Modal

from game.views.player_control import player_control


def surprise( request, player_id ):
    player = Player.objects.get( pk=player_id )

    # Get surprise_list.json
    module_dir    = os.path.dirname(__file__)  # get current directory
    file_path     = os.path.join(module_dir, 'surprise_list.json')
    surprise_file = open ( file_path, "rb" ) 
    surprise_list = json.loads( surprise_file.read() )

    # Random surprise from surprise_list
    surprise = choice( surprise_list['surprises'] )
    
    name  = f'''Сюрприз - "{surprise['name']}" {surprise['count']}.'''

    Actions(
        player = player,
        name   = name,
        count  = surprise['count']
    ).save()

    # Close surprise_list.json
    surprise_file.close()

    # Create Bootstrap Modal window
    modal = Modal("Сюрприз!", player)
    modal.surprise = surprise
    modal.type = "surprise"

    return player_control( 
        request   = request, 
        player_id = player_id, 
        modal     = modal 
    )
