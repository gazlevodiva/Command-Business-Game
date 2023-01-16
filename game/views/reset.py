from django.shortcuts import redirect

from game.models.Player import Player
from game.models.Actions import Actions
from game.models.PlayersBusiness import PlayersBusiness
from game.models.CommandPayments import CommandPayments
from game.models.BusinessPayments import BusinessPayments


def reset(request):

    if request.user.is_authenticated:
    
        # Delete all about last game
        Player.objects.all().delete()
        Actions.objects.all().delete()
        PlayersBusiness.objects.all().delete()
        CommandPayments.objects.all().delete()
        BusinessPayments.objects.all().delete()

        player_X_balance = 200000

        player_X = Player( name="X", visible=False )
        player_X.save()
        
        commandBusinessPayments = CommandPayments(
            player = player_X, 
            count  = player_X_balance,
        )
        commandBusinessPayments.save()

        name = f'''Начал игру - {player_X_balance}'''
        Actions(
            player   = player_X,
            name     = name,
            count    = player_X_balance,
            category = 'OTHER',
        ).save()

        name = f'''Вложил в командный бизнес - {player_X_balance}'''
        
        Actions(
            player   = player_X,
            name     = name,
            count    = -player_X_balance,
            category = 'CMND',
            is_command = True
        ).save()

    return redirect("/")
