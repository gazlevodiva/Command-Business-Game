from argparse import Action
from distutils.cmd import Command
from random import randint

from django.db.models import Sum

from game.models.Player import Player
from game.models.Actions import Actions
from game.models.CommandPayments import CommandPayments
from game.models.BusinessPayments import BusinessPayments


def setDefoult( player_business ):
    player = player_business.player
    business = player_business.business

    # Defoult business will sale by 30% of cost
    business_sale_price = int( business.cost * 0.33 )
    
    if player_business.is_command:

        CommandPayments(
            count = business_sale_price
        ).save()

        name = f'''
            {business.name} - Дефолт! 
            Возврат стоимости {business_sale_price}. Коммандный бизнес.
        '''

        defoult_action = Actions.objects.create(
            player = player,
            name   = name,
            count  = 0
        )

    if not player_business.is_command:

        name = f'''
            {business.name} - Дефолт! 
            Возврат стоимости {business_sale_price}.
        '''

        defoult_action = Actions.objects.create(
            player = player,
            name   = name,
            count  = business_sale_price
        )
                
    # Set business defoult
    player_business.status = 'defoult'
    player_business.save()

    return defoult_action


def getBusinessProfit( player_business ):

    # 1 STEP - Defoult Probability 
    defoult_probability = randint( 1, 16 )
    # defoult_probability = 1
    if defoult_probability == 1:
        defoult_action = setDefoult( player_business )
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
        player_business     = player_business,
        count               = profit,
        rentability         = rentability,
        defoult_probability = defoult_probability,
        player_level        = player_business.player.level + 1,
    )

    return ( defoult_probability, rentability, profit, False )


def setPersonalBusinessIncome( player_business ):

    # Business profit
    defoult, rentability, profit, defoult_action = getBusinessProfit( player_business )

    name = f''' 
        {player_business.business.name} доход {profit}, 
        рентабельность {rentability}%;
    '''
    payment_action = Actions.objects.create(
        player = player_business.player,
        name   = name,
        count  = profit
    )

    actions = [ payment_action ]
    if defoult_action:
        actions.append( defoult_action )

    return ( defoult, rentability, profit, actions ) 


def setCommandBusinessIncome( player_business ):

    defoult, rentability, profit, defoult_action = getBusinessProfit( player_business )
    command_business_players     = getCommandPlayers()

    # 20% after add to admin
    players_bank = int( profit * 0.8 )
    admin_share  = profit - players_bank
    admin_player = player_business.player
    
    payment_actions = [ ]
    if defoult_action:
        payment_actions.append( defoult_action )


    if profit >= 0:
        for command_player in command_business_players:
            count = int( players_bank * command_player['share'] / 100 )

            # Count new shares. Admin +20%
            if command_player['player'] == admin_player:
                count += admin_share
            
            name = f'''
                {player_business.business.name} доход {count}, 
                рентабельность {rentability}%. Коммандный бизнес.
            '''
            payment_action = Actions.objects.create(
                player = command_player['player'],
                name   = name,
                count  = count
            )
            payment_actions.append( payment_action )

    if profit < 0:
        name = f''' 
                {player_business.business.name} доход {profit}, 
                рентабельность {rentability}%. Коммандный бизнес.
        '''
        payment_action = Actions.objects.create(
            player = player_business.player,
            name   = name,
            count  = profit
        )
        payment_actions.append( payment_action )

    return ( defoult, rentability, profit, payment_actions )


def getCommandBank():
    return (
        CommandPayments.objects
        .aggregate( Sum('count') )
    )['count__sum']


def getCommandPlayers():
    bank = (
        CommandPayments.objects
        .filter( player__isnull=False )
        .aggregate( Sum( 'count' ) )
    )['count__sum']

    player_payments = (
        CommandPayments.objects
        .filter( player__isnull=False )
        .values( 'player' )
        .annotate( 
            share = Sum( 'count' ) * 100 / bank,
            count = Sum( 'count' )
        )
        .order_by()
    )
    
    for player_payment in player_payments:
        player_payment['player'] = Player.objects.get( 
            pk=player_payment['player'] 
        )

    return player_payments


def getBusinessPayments( player_business ):
    return BusinessPayments.objects.filter( player_business=player_business )


def getCommandShare( player ):
    command_players = getCommandPlayers()
    for command_player in command_players:

        if command_player['player'] == player:
            return ( 
                command_player['share'], 
                command_player['count'] 
            )

    return ( 0, 0 )


def sellCommandShare( player ):
    share, count = getCommandShare( player )

    name = f'''
        Продал свою долю {share}% коммандного бизнеса за
        {count}.
    '''

    Actions(
        player = player,
        name   = name,
        count  = count
    ).save()

    CommandPayments(
            player = player,
            count  = -count
        ).save()