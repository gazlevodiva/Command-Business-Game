from django.shortcuts import redirect


from game.models.Moves import Moves
from game.models.Actions import Actions
from game.models.CommandPayments import CommandPayments
from game.models.PlayersBusiness import PlayersBusiness
from game.models.PlayersBusinessStatus import PlayersBusinessStatus

from game.decorators import check_user_session_hash


@check_user_session_hash
def sell_business(request, session, player_business_id):
    
    players_business = PlayersBusiness.objects.get( pk=player_business_id )
    player = players_business.player

    move = Moves.objects.create( player=player )

    if players_business.is_command:
        name = f'''
            Коммандный бизнес {players_business.business.name} продан.
        '''  
        Actions.objects.create(
            move     = move,
            count    = 0,
            name     = name,
            category = 'SELL_BIS',
            is_command = True
        )

        CommandPayments.objects.create(
            count    = players_business.business.cost,
            category = "SELL_BIS",
            move     = move
        )

    if not players_business.is_command:
        name = f'''
            Личный бизнес {players_business.business.name} продан.
        '''
        Actions.objects.create(
            move     = move,
            count    = players_business.business.cost,
            name     = name,
            category = 'SELL_BIS',
        )

    PlayersBusinessStatus.objects.create(
        move = move,
        players_business = players_business,
        status = "SOLD"
    )    


    return redirect(f"/player_control_{ player.id }/")
