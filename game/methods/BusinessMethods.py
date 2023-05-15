from random import randint

from django.db.models import Sum

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.models.CommandPayments import CommandPayments
from game.models.BusinessPayments import BusinessPayments
from game.models.PlayersBusinessStatus import PlayersBusinessStatus



def setDefoult( player_business, move ):  

    player = player_business.player
    session = player.game_session
    business = player_business.business

    # Defoult business will sale by 30% of cost
    business_sale_price = int( business.cost * 0.33 )
    
    if player_business.is_command:

        CommandPayments.objects.create(
            count = business_sale_price,
            move  = move,
        )

        name = f'''
            🔥 {business.name} - Дефолт!
            Возврат стоимости {business_sale_price}. Коммандный бизнес.
        '''

        defoult_action = Actions.objects.create(
            move       = move,
            name       = name,
            count      = 0,
            category   = 'BSNS',
            is_command = True
        )

    if not player_business.is_command:

        name = f'''
            🔥 {business.name} - Дефолт! 
            Возврат стоимости {business_sale_price}.
        '''

        defoult_action = Actions.objects.create(
            move     = move,
            name     = name,
            count    = business_sale_price,
            category = 'CMND',
        )
                
    # Set business defoult
    player_business_status = PlayersBusinessStatus.objects.get( player_business=player_business )
    player_business_status.status = 'DEFOULT'
    player_business_status.save()

    return defoult_action


def getBusinessProfit( player_business, move ):

    print( player_business )

    # 1 STEP - Defoult Probability 
    defoult_probability = randint( 1, 16 )
    # defoult_probability = 1
    if defoult_probability == 1:
        defoult_action = setDefoult( player_business, move )
        return ( 0, 0, 0, defoult_action )

    # 2 STEP - Rentability
    rentability = randint( 
        player_business.business.min_rent,
        player_business.business.max_rent
    ) 
        
    # 3 STEP - Business Income
    profit = int( 
        player_business.business.cost * rentability / 100 
    )

    business_action = BusinessPayments.objects.create(
        move                = move,
        player_business     = player_business,
        count               = profit,
        rentability         = rentability,
        defoult_probability = defoult_probability,
        player_level        = player_business.player.level + 1,
    )

    return ( defoult_probability, rentability, profit, False )


def setPersonalBusinessIncome( player_business, move ):

    # Business profit
    defoult, rentability, profit, defoult_action = getBusinessProfit( player_business, move )

    name = f''' 
        {player_business.business.name} доход {profit}, 
        рентабельность {rentability}%;
    '''
    payment_action = Actions.objects.create(
        move     = move,
        name     = name,
        count    = profit,
        category = 'BSNS',
    )

    actions = [ payment_action ]
    if defoult_action:
        actions.append( defoult_action )

    return ( defoult, rentability, profit, actions ) 


def setCommandBusinessIncome( player_business, move ):

    defoult, rentability, profit, defoult_action = getBusinessProfit( player_business, move )
    command_business_players = getCommandPlayers( player_business.player.game_session )

    # 20% after add to admin
    players_bank = int( profit * 0.8 )
    admin_share  = profit - players_bank
    admin_player = player_business.player
    
    payment_actions = []
    if defoult_action:
        payment_actions.append( defoult_action )

    if profit > 0:
        for command_player in command_business_players:

            # Players profit
            count = int( players_bank * command_player['share'] / 100 )

            # Create move for every command player
            new_move = Moves.objects.create( player=command_player['move__player'], number=move.number )

            # Count new shares. Admin +20%
            if command_player['move__player'] == admin_player:
                count += admin_share
                name = f'''
                    Командный бизнес. {player_business.business.name} доход {profit}, 
                    рентабельность {rentability}%. 
                '''

            else:
                name = f'''Доход от командного бизнеса {count}.'''

            
            
            payment_action = Actions.objects.create(
                move     = new_move,
                name     = name,
                count    = count,
                category = 'CMND',
                is_command = True
            )
            payment_actions.append( payment_action )

    if profit <= 0:
        name = f''' 
            Командный бизнес. {player_business.business.name} рентабельность {rentability}%. 
        '''
        payment_action = Actions.objects.create(
            move     = move,
            name     = name,
            count    = profit,
            category = 'CMND',
            is_command = True
        )
        payment_actions.append( payment_action )

    return ( defoult, rentability, profit, payment_actions )


def getCommandBank( game_session ):
    return (
        CommandPayments.objects
        .filter( move__player__game_session=game_session )
        .aggregate( Sum('count') )
    )['count__sum']


def getBusinessPayments( player_business ):
    return BusinessPayments.objects.filter( 
        player_business = player_business, 
    )


def getCommandPlayers( game_session ):
    bank = (
        CommandPayments.objects.filter( 
            move__player__game_session = game_session
        )
        .filter( category__in=["DEPOSITE", "WITHDRAW"] )
        .aggregate( Sum( 'count' ) )
    )['count__sum']

    player_payments = (
        CommandPayments.objects.filter( 
            move__player__game_session = game_session
        )
        .filter( category__in=["DEPOSITE", "WITHDRAW"] )
        .values( 'move__player' )
        .annotate( 
            share = Sum( 'count' ) * 100 / bank,
            count = Sum( 'count' )
        )
        .order_by()
    )
    
    for player_payment in player_payments:
        player_payment['move__player'] = Player.objects.get( 
            pk = player_payment['move__player'],
        )

    return player_payments


def getCommandShare( player ):

    game_session = player.game_session

    command_players = getCommandPlayers( game_session=game_session )

    for command_player in command_players:
        if command_player['move__player'] == player:
            return ( command_player['share'], command_player['count'] )

    return ( 0, 0 )


def sellCommandShare( move, sell_count=None):
    share, count = getCommandShare( move.player )

    name = f'''
        Продал свою долю {share}% коммандного бизнеса за {count}.
    '''

    if sell_count:        
        count = sell_count
        name = f''' Продал {count} из своей командной доли. '''

    Actions.objects.create(
        move     = move,
        name     = name,
        count    = count,
        category = 'CMND',
        is_command = True
    ).save()

    CommandPayments.objects.create(
        move     = move,
        category = "WITHDRAW",
        count    = -count
    )
    