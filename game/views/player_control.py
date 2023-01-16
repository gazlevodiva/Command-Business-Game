from django.shortcuts import render
from django.shortcuts import redirect

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

# Player controller
@check_user_session_hash
def player_control( request, player_id, modal=False ):

    # Get all businesses to use in form
    businesses = Business.objects.all()

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
    bank = getCommandBank()


    # Player Controller
    if request.method == 'POST':


        if 'player_business' in request.POST:

            print( request.POST )

            # get Business
            business_id = request.POST['player_business']
            business = Business.objects.get( pk=business_id )

            # Check command or not
            if 'is_command' in request.POST:
                is_command = True
            
            if 'is_command' not in request.POST:
                is_command = False

            # Set new business for player
            newBusiness(player, business, is_command)
            

        if 'player_command_payment' in request.POST:

            # Count of command payment from POST form
            command_payment = int( request.POST['player_command_payment'] ) 

            CommandPayments(
                player = player, 
                count  = command_payment,
            ).save()

            name = f'''Вложил в командный бизнес - {command_payment}.'''

            Actions(
                player   = player,
                category = 'CMND',
                name     = name,
                count    = -command_payment,
                is_command = True
            ).save()


        return redirect( f"/player_control_{player_id}/" )


    context = {
        "player":            player, 
        "businesses":        businesses, 
        "player_businesses": business_payments_info,
        "player_balance":    player_balance,
        "command_share":     share,
        "command_count":     count,
        "command_bank":      bank,
        "modal":             modal
    }
    return render(request, 'game/player_control.html', context)