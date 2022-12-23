
from random import choice
from random import randint

from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Surprises import Surprises
from game.models.CommandPayments import CommandPayments
from game.methods.NotificationModal import Modal

from game.views.player_control import player_control

from game.methods.PlayerMethods import getPlayerCategoties
from game.methods.BusinessMethods import getCommandBank

from game.decorators import check_user_session_hash


@check_user_session_hash
def surprise( request, player_id, surprise_type ):

    player = Player.objects.get( pk=player_id )


    # Get categories by surprise type
    all_categories = {
        "surp": getPlayerCategoties( player ),
        "memo": ["MEMO"],
        "cmnd": ["COMMAND"],
    }[ surprise_type ]


    # Get all surprises
    all_surprises  = Surprises.objects.all()
    surprise_list = suprise_list_generator( all_surprises, all_categories )
   

    # Random surprise from surprise_list
    if len( surprise_list ) == 0:
        surprise = choice( all_surprises )
    else:
        surprise = choice( surprise_list )


    action_name = {
        "surp": f'Сюрприз - "{surprise.name}" {surprise.count}.',
        "memo": surprise.name,
        "cmnd": f'{surprise.name} {surprise.count}.',
    }[ surprise_type ]


    modal_name = {
        "surp": "Сюрпрайз!",
        "memo": "Мемори!",
        "cmnd": "Сюрприз для Командного бизнеса!",
    }[ surprise_type ]


    # Create modal
    modal = Modal( modal_name, player )
    modal.surprise = surprise
    modal.type = surprise_type
    
    # If surprise personal
    action_count = surprise.count

    # If suprise Command
    if surprise_type == "cmnd":

        # Becouse action is personal counter
        action_count = 0

        if surprise.count == 0:
            command_bank = getCommandBank()
            count = -int( command_bank / 2 )
        else:
            count = surprise.count
        
        # Make command Payment with no player
        CommandPayments.objects.create(
            count = count
        )
                    

    Actions(
        player   = player,
        name     = action_name,
        count    = action_count,
        category = 'SURP',
    ).save()

    return player_control( 
        request   = request, 
        player_id = player_id, 
        modal     = modal 
    )


def suprise_list_generator( all_surprises, all_categories ):
    surprise_list = []

    for category  in all_categories:
        category_surprises = all_surprises.filter( category=category )

        if len( category_surprises ) > 0:
            for surprise in category_surprises:
                surprise_list.append( surprise )
    
    return surprise_list
