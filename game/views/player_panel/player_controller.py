from django.shortcuts import render
from django.shortcuts import redirect

from django.http import JsonResponse

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Business import Business
from game.models.CommandPayments import CommandPayments

from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import newBusiness
from game.methods.PlayerMethods import getBusinesses

from game.methods.BusinessMethods import getCommandBank
from game.methods.BusinessMethods import getCommandShare
from game.methods.BusinessMethods import getBusinessPayments

from game.decorators import check_user_session_hash

from django.core.serializers import serialize
import json

 
@check_user_session_hash
def player_control_buy_business( request, session, player_id, business_id, is_command ):
    
    player = Player.objects.get( pk=player_id )
    business = Business.objects.get( pk=business_id )
    move = Moves.objects.create( player=player )

    if is_command == "command":
        is_command = True

    if is_command == "personal":
        is_command = False

    newBusiness(move, business, is_command)


@check_user_session_hash
def player_control_business_data( request, session, player_id, business_category ):
    
    player = Player.objects.get( pk=player_id )
    player_balance = getBalance( player )
    share, count = getCommandShare( player )
    bank = getCommandBank( session )

    if business_category == "ALL":
        businesses = Business.objects.all().order_by('cost')

    else:
        businesses = Business.objects.filter( category=business_category ).order_by('cost')
        
    businesses = json.loads(serialize("json", businesses))

    context = {
        "player_id":  player.id,
        "businesses": businesses,
        "player_balance": player_balance,
        "command_share":  share,
        "command_count":  count,
        "command_bank":   bank,
    }
    response = JsonResponse( context )
    return response 


@check_user_session_hash
def player_control_data( request, session, player_id ):
    
    player = Player.objects.get( pk=player_id )
    player_balance = getBalance( player )
    share, count = getCommandShare( player )
    bank = getCommandBank( session )

    context = {
        "player_level":   player.level,
        "player_balance": player_balance,
        "command_share":  share,
        "command_count":  count,
        "command_bank":   bank,
    }
    response = JsonResponse( context )
    return response 


# Main player controller
@check_user_session_hash
def player_control( request=None, session=None, player_id=None, modal=False ):

    # Get players businesses 
    player = Player.objects.get( pk=player_id )

    # Personal Businesses
    player_businesses = getBusinesses( player )

    # Business Payments for player businesses in card
    business_payments_info = []

    for player_business in player_businesses:

        business_payments = getBusinessPayments( player_business )
        business_payments_info.append(
            {
                "business":          player_business,                
                "business_payments": business_payments[::-1][:7]
            }
        )

    # Balance by Actions
    player_balance = getBalance( player )


    # Try to get command business
    share, count = getCommandShare( player )

    # Command Bank
    bank = getCommandBank( session )


    # Player Controller
    if request.method == 'POST':            
        if 'player_command_payment' in request.POST:

            # Count of command payment from POST form
            command_payment = int( request.POST['player_command_payment'] ) 

            move = Moves.objects.create( player=player )

            CommandPayments.objects.create(
                move     = move, 
                category = 'DEPOSITE',
                count    = command_payment,
            )

            name = f'''Вложил в командный бизнес - {command_payment}.'''

            Actions.objects.create(
                move     = move,
                category = 'CMND',
                name     = name,
                count    = -command_payment,
                is_command = True
            )

        return redirect( f"/player_control_{player_id}/" )

    

    context = {
        "player":            player, 
        "player_businesses": business_payments_info,
        "player_balance":    player_balance,
        "command_share":     share,
        "command_count":     count,
        "command_bank":      bank,
        "modal":             modal,
        "game_session":      session,
    }

    if request is None:
        return context

    return render(request, 'game/player_control/player_control.html', context)
