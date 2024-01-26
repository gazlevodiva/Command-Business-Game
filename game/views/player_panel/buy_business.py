from django.http import JsonResponse

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Business import Business

from game.methods.PlayerMethods import newBusiness
from game.methods.BusinessMethods import getVotion
from game.methods.BusinessMethods import setVotion
from game.methods.BusinessMethods import playerIdForVotion

from game.decorators import check_user_session_hash


@check_user_session_hash
def player_control_buy_business(
    request,
    session,
    player_id,
    business_id,
    is_command
):
    player = Player.objects.get(pk=player_id)
    move = Moves.objects.filter(player=player).last()
    business = Business.objects.get(pk=business_id)

    context = {}

    if is_command == "command":
        if len(playerIdForVotion(session)) == 1:
            newBusiness(move, business, is_command=True)
            context["result"] = True
            return JsonResponse(context)

        setVotion(move, business)
        context["votion"] = getVotion(move)

    if is_command == "personal":
        newBusiness(move, business, is_command=False)
        context["result"] = True

    return JsonResponse(context)
