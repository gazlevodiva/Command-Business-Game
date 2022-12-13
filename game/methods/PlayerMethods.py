from random import randint

from django.db.models import Sum

from game.models.Player import Player
from game.models.Actions import Actions

from game.models.PlayersBusiness import PlayersBusiness
from game.models.CommandPayments import CommandPayments


SALARY = {
    1: 5000,
    2: 6000,
    3: 7200,
    4: 8500,
    5: 10100,
    6: 12000,
    7: 14200,
    8: 16800,
    9: 19800,
    10: 23300,
    11: 14900,
    12: 7800,
    13: 1600,
    14: -3700,
    15: -8500,
    16: -12900,
    17: -17100,
    18: -21100,
    19: -25100,
    20: -29200,
}


def getPlayer( player_id ):
    return Player.objects.get( pk=player_id )


def getBalance( player ):
    return (
        Actions.objects
        .filter( player=player )
        .aggregate( Sum('count') )['count__sum']
    )


def getInflation( player ):
    inflation = randint( 1,10 )
    if inflation == 1:

        player_balance = getBalance(player)

        if player_balance <= 0:
            count = 0

        if player_balance > 0:
            count = -int( player_balance / 2 )

        name = f'Инфляция! Потеря средств {count}.'

        return Actions.objects.create(
            player = player,
            name   = name,
            count  = count
        )

    
    name = 'Инфляции нет.'

    return Actions.objects.create(
        player = player,
        name   = name,
        count  = 0
    )
    

def getSalary( player ):
    try:
        salary = SALARY[ player.level ]
    except:
        salary = 0

    name = f'Зарплата {salary}, круг {player.level+1}.'

    return Actions.objects.create(
        player = player,
        name   = name,
        count  = salary
    )


def getBusinesses( player ):
    return (
        PlayersBusiness.objects
        .filter( 
            player=player, 
            status='active' 
        )
    )


def getCommandBusinesses( player=None ):
    if player:
        return PlayersBusiness.objects.filter( 
            player=player, 
            status='active',
            is_command=True
        )

    if not player:
        return PlayersBusiness.objects.filter( 
            status='active',
            is_command=True
        )


def setNewLevel( player ):
    player.level += 1 
    return player.save()


def newBusiness( player, business, is_command ):

    if is_command:
        name = f'''
            Стал администратором {business.name} в коммандном бизнесе.
        '''
        Actions(
            player=player,
            name=name,
            count= 0
        ).save()

        CommandPayments(
            count= -business.cost
        ).save()

        PlayersBusiness(
            player=player, 
            business=business,
            is_command=is_command,
        ).save()

    if not is_command:
        name = f'''
            Купил личный бизнес {business.name}.
        '''
        Actions(
            player=player,
            name=name,
            count= -business.cost
        ).save()

        PlayersBusiness(
            player=player, 
            business=business,
            is_command=is_command,
        ).save()


def PlayerXReinvest():
    player_X = Player.objects.get( name='X' )
    player_x_balance = getBalance( player_X )

    name = f'''Вложил в командный бизнес {player_x_balance}.'''
    Actions(
        player=player_X,
        name=name,
        count= -player_x_balance
    ).save()

    CommandPayments(
        player=player_X, 
        count=player_x_balance
    ).save()


def getActions():
    return Actions.objects.all()
