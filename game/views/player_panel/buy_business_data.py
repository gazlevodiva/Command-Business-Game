from django.http import JsonResponse

from game.models.Player import Player
from game.models.Business import Business

from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import getBusinesses

from game.methods.BusinessMethods import getCommandBank
from game.methods.BusinessMethods import getCommandShare

from game.decorators import check_user_session_hash

from django.core.serializers import serialize
import json


@check_user_session_hash
def player_control_business_data(
    request,
    session,
    player_id,
    business_category
):
    player = Player.objects.get(pk=player_id)
    player_balance = getBalance(player)
    share, count = getCommandShare(player)
    bank = getCommandBank(session)

    businesses = (
        Business.objects
        .filter(game_mode=session.game_mode)
        .order_by("cost")
    )

    if business_category != "ALL":
        businesses = businesses.filter(category=business_category)

    businesses = json.loads(serialize("json", businesses))

    # get businesses count
    businesses_count = getBusinesses(player)
    can_buy_more = True
    if len(businesses_count) >= 10:
        can_buy_more = False

    context = {
        "player_id": player.id,
        "businesses": businesses,
        "player_balance": player_balance,
        "command_share": share,
        "command_count": count,
        "command_bank": bank,
        "can_buy_more": can_buy_more,
    }
    response = JsonResponse(context)
    return response
