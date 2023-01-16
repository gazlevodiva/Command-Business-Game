from django.shortcuts import redirect

from game.models.Actions import Actions
from game.models.PlayersBusiness import PlayersBusiness
from game.models.CommandPayments import CommandPayments

from game.decorators import check_user_session_hash


@check_user_session_hash
def sell_business(request, player_business_id):
    
    player_business = PlayersBusiness.objects.get( pk=player_business_id )

    if player_business.is_command:
        name = f'''
            Коммандный бизнес {player_business.business.name} продан.
        '''  
        Actions(
            count    = 0,
            player   = player_business.player,
            name     = name,
            category = 'CMND',
            is_command = True
        ).save()

        CommandPayments(
            count  = player_business.business.cost
        ).save()

    if not player_business.is_command:
        name = f'''
            Личный бизнес {player_business.business.name} продан.
        '''
        Actions(
            count    = player_business.business.cost,
            player   = player_business.player,
            name     = name,
            category = 'BSNS',
        ).save()

    player_business.status = 'SOLD'
    player_business.save()

    return redirect(f"/player_control_{player_business.player.id}/")
