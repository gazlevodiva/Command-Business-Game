from random import randint

from django.db.models import Sum, Subquery, OuterRef

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions

from game.models.PlayersBusiness import PlayersBusiness
from game.models.CommandPayments import CommandPayments
from game.models.PlayersBusinessStatus import PlayersBusinessStatus


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
        Actions.objects.filter( 
            move__player = player, 
        )
        .aggregate( Sum('count') )['count__sum']
    )


def getInflation( move ):
    inflation = randint( 1,10 )
    if inflation == 1:

        player_balance = getBalance( move.player )

        if player_balance <= 0:
            count = 0

        if player_balance > 0:
            count = -int( player_balance / 2 )

        name = f"📉 Инфляция! Потеря средств {count}."

        return Actions.objects.create(
            move     = move,
            name     = name,
            count    = count,
            category = 'INFL',
        )

    
    name = 'Инфляции нет.'

    return Actions.objects.create(
        move     = move,
        name     = name,
        count    = 0,
        category = 'OTHER',
    )
    

def getSalary( move ):
    try:
        salary = SALARY[ move.player.level ]
    except:
        salary = 0

    name = f'Зарплата {salary}, круг { move.player.level+1 }.'

    return Actions.objects.create(
        move     = move,
        name     = name,
        count    = salary,
        category = 'SLR',
    )


def getBusinesses( player ):
    res = PlayersBusiness.objects.annotate(
        latest_status=Subquery(
            PlayersBusinessStatus.objects.filter(players_business=OuterRef("pk")).order_by("-move").values("status")[:1]
        )
    ).filter(player=player, latest_status="ACTIVE")

    return res


def getCommandBusinesses( player=None ):
    return getBusinesses( player ).filter( is_command=True )


def setNewLevel( player ):
    player.level += 1 
    return player.save()


def newBusiness( move, business, is_command ):

    if is_command:
        name = f'''
            Стал администратором {business.name} в коммандном бизнесе.
        '''
        Actions.objects.create(
            move     = move,
            name     = name,
            count    = 0,
            category = 'BUY_BIS',
            is_command = is_command
        )

        CommandPayments.objects.create(
            move     = move,
            category = "BUY_BIS",
            count    = -business.cost
        )

        players_business = PlayersBusiness.objects.create(
            player     = move.player, 
            business   = business,
            is_command = is_command,
        )

    if not is_command:
        name = f'''
            Купил личный бизнес {business.name}.
        '''
        Actions.objects.create(
            move     = move,
            name     = name,
            count    = -business.cost,
            category = 'BUY_BIS',
        )

        players_business = PlayersBusiness.objects.create(
            player     = move.player, 
            business   = business,
            is_command = is_command,
        )

    PlayersBusinessStatus.objects.create(
        players_business = players_business,
        move   = move,
        status = "ACTIVE"
    )

    


def PlayerXReinvest( move ):
    player_x = Player.objects.get( name='X', game_session=move.player.game_session )
    player_x_balance = getBalance( player_x )

    if player_x_balance == 0:
        return

    name = f'Вложил в командный бизнес {player_x_balance}.'

    new_move = Moves.objects.create( player=player_x, number=move.number )
    
    Actions.objects.create(
        move     = new_move,
        name     = name,
        count    = -player_x_balance,
        category = 'CMND',
        is_command = True
    )

    CommandPayments.objects.create(
        move     = new_move, 
        category = "DEPOSITE",
        count    = player_x_balance
    )


def getActions( session ):
    return Actions.objects.filter( move__player__game_session=session ).order_by( 'created_date' )


def getPlayerCategoties( player ):
    player_businesses = getBusinesses( player ) 

    categories = ['PERSONAL']
    for player_business in player_businesses:
        if player_business.business.category not in categories:
            categories.append( player_business.business.category )

    return categories


def getPlayerSurprises( move ):
    return Actions.objects.filter( 
            move     = move, 
            category = 'SURP',
        )


def getBusinessesCost( player):
    return (
        PlayersBusiness.objects
        .filter(
            player       = player, 
            status       = 'ACTIVE',
            game_session = player.game_session
        )
        .aggregate(Sum('business__cost'))['business__cost__sum']
    )
    