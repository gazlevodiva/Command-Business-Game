from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.http import JsonResponse

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Surprises import Surprises
from game.models.MemoryAnswers import MemoryAnswers
from game.models.CommandPayments import CommandPayments

from game.methods.MoveMethods import set_go_to_start
from game.methods.MoveMethods import set_back_to_start
from game.methods.MoveMethods import set_end_move

from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import getBusinesses
from game.methods.PlayerMethods import playerTurn
from game.methods.PlayerMethods import isOpenCommandBusiness
from game.methods.PlayerMethods import firstInvestToCommandBusiness
from game.methods.PlayerMethods import get_business_card_info

from game.methods.BusinessMethods import getVotion
from game.methods.BusinessMethods import playerIdForVotion
from game.methods.BusinessMethods import getCommandBank
from game.methods.BusinessMethods import getCommandShare
from game.methods.BusinessMethods import getBusinessPayments

from game.decorators import check_user_session_hash

from .new_level import is_new_level

GAME_FIELD = {
    1: "start-cell",
    2: "horeca-business-cell",
    3: "surprise-cell",
    4: "random-move-cell",
    5: "memory-cell",
    6: "realty-business-cell",
    7: "random-move-cell",
    8: "command-surprise-cell",
    9: "surprise-cell",
    10: "all-business-cell",
    11: "memory-cell",
    12: "skip-move-cell",
    13: "back-to-start-cell",
    14: "go-to-start-cell",
    15: "surprise-cell",
    16: "science-business-cell",
    17: "random-move-cell",
    18: "memory-cell",
    19: "all-business-cell",
    20: "command-surprise-cell",
    21: "random-move-cell",
    22: "surprise-cell",
    23: "it-business-cell",
    24: "memory-cell",
}


@check_user_session_hash
def player_finish_move(request, session, move_id):
    set_end_move(Moves.objects.get(pk=move_id))
    return JsonResponse({"result": True})


@check_user_session_hash
def player_back_to_start(request, session, move_id):
    set_back_to_start(Moves.objects.get(pk=move_id))
    return JsonResponse({"result": True, "move_id": move_id})


@check_user_session_hash
def player_go_to_start(request, session, move_id):
    set_go_to_start(Moves.objects.get(pk=move_id))
    return JsonResponse({"result": True, "move_id": move_id})


@check_user_session_hash
def player_control_data(request, session, player_id):
    context = {}
    player = Player.objects.get(pk=player_id)
    player_balance = getBalance(player)
    share, count = getCommandShare(player)
    bank = getCommandBank(session)

    # Get moves info
    player_moves = Moves.objects.filter(player=player)
    player_move = player_moves.last()

    # Get actions info
    player_actions = (
        Actions.objects
        .filter(move__player=player)
        .filter(move__number=player_move.number)
    )
    player_last_action = player_actions.last()

    # Whos player turn
    player_turn = playerTurn(session)
    if player == player_turn:
        is_player_turn = True

    if player != player_turn:
        is_player_turn = False

    context["player_id"] = player.id
    context["player_name"] = player.name
    context["player_level"] = player.level
    context["player_balance"] = player_balance
    context["command_share"] = share
    context["command_count"] = count
    context["command_bank"] = bank
    context["is_player_turn"] = is_player_turn
    context["is_open_command_business"] = isOpenCommandBusiness(player)
    context["move_id"] = player_move.id
    context["move_stage"] = player_last_action.move_stage
    context["cell_name"] = GAME_FIELD[player_move.position]
    context["cell_position"] = player_move.position

    # Vote for buy command business
    if player.id in playerIdForVotion(player.game_session):
        context["votion"] = getVotion(player_move)
    else:
        context["votion"] = False

    # Fisrt action with command business
    context["first_invest_chance"] = firstInvestToCommandBusiness(player_move)

    # Does the player have a new_level?
    new_level_details = is_new_level(player)

    if new_level_details:
        context["is_new_level"] = new_level_details

    if not new_level_details:
        context["action_name"] = player_last_action.name
        context["action_count"] = player_last_action.count
        context["action_category"] = player_last_action.category

    # Memory
    if player_last_action.category == "MEMO":
        memories = Surprises.objects.filter(name=player_last_action.name)
        memory_exist = memories.filter(session_id=session.id).exists()

        if memory_exist:
            memory = memories.get(session_id=session.id)

        if not memory_exist:
            memory = memories.get(session_id=0)

        context["memory_id"] = memory.id

    # Command surprise
    if player_last_action.category == "SURP" and player_last_action.is_command:
        context["action_count"] = CommandPayments.objects.get(move=player_move).count

    # If player drop the dice
    if player_actions.filter(category="DICE_VALUE").exists():
        # Get dice value from last move
        last_action_dice = (
            player_actions
            .filter(category="DICE_VALUE")
            .get(move_stage="END")
        )
        action_dive_value = (
            sum([int(x) for x in last_action_dice.name.split('-')])
        )
        context['dice_value'] = action_dive_value

        if len(player_moves) > 1:
            previous_move = player_moves.order_by('-id')[1]
            context['previous_cell_position'] = previous_move.position
            end_cell_position = previous_move.position + action_dive_value

            context["next_cell"] = False
            if end_cell_position > 25:
                context['next_cell'] = True
                context['next_cell_move'] = end_cell_position - 25

        else:
            previous_move = None

    # Get information for business cards
    context["player_businesses"] = get_business_card_info(player)

    return JsonResponse(context)


# Main player controller
@check_user_session_hash
def player_control(request=None, session=None, player_id=None, modal=False):
    # Set context
    context = {}
    context["game_session"] = session

    # Get players businesses
    # player = Player.objects.get(pk=player_id)
    player = get_object_or_404(Player, pk=player_id)
    context["player"] = player

    last_move = Moves.objects.filter(player=player).last()
    context["move"] = last_move
    context["current_player_position"] = last_move.position

    # whos player Turn???
    player_turn = Player.objects.get(pk=playerTurn(session))

    context["player_turn"] = player_turn

    if player == player_turn:
        context["is_player_turn"] = True

    if player != player_turn:
        context["is_player_turn"] = False

    # Business Payments for player businesses in card
    business_payments_info = []
    for player_business in getBusinesses(player):
        business_payments = getBusinessPayments(player_business)
        business_payments_info.append(
            {
                "business": player_business,
                "business_payments": business_payments[::-1][:7],
            }
        )

    context["player_businesses"] = business_payments_info

    # Balance by Actions
    player_balance = getBalance(player)
    share, count = getCommandShare(player)
    bank = getCommandBank(session)

    context["player_balance"] = player_balance
    context["command_share"] = share
    context["command_count"] = count
    context["command_bank"] = bank

    # Player Controller
    if request.method == "POST":
        if "player_command_payment" in request.POST:
            # Count of command payment from POST form
            payment = int(request.POST["player_command_payment"])
            form_type = request.POST["form_type"]

            if form_type == "first_invest":
                first_invest = True
                new_move = last_move

            if form_type == "other_invest":
                first_invest = False
                new_move = Moves.objects.create(
                    player=player, position=last_move.position
                )

            # Invest Money
            CommandPayments.objects.create(
                move=new_move,
                category="DEPOSITE",
                count=payment,
            )
            Actions.objects.create(
                move=new_move,
                category="CMND",
                name="Вложил средства в КБ",
                count=-payment,
                is_command=True,
                is_personal=True,
                is_public=True,
            )

            if first_invest:
                set_end_move(new_move)

        if "memory_answer" in request.POST:
            move_id = request.POST["move_id"]
            memory_id = request.POST["memory_id"]
            memory_answer = request.POST["memory_answer"]

            move = Moves.objects.get(pk=move_id)
            surprise = Surprises.objects.get(pk=memory_id)

            action = Actions.objects.create(
                move=move,
                move_stage="END",
                name=surprise.name,
                count=0,
                category="MEMO",
                visible=False,
                is_command=False,
                is_personal=True,
                is_public=False,
            )

            MemoryAnswers.objects.create(
                action=action,
                question=surprise,
                answer=memory_answer,
            )

        return redirect(f"/player_control_{player_id}/")

    context["is_open_command_business"] = isOpenCommandBusiness(player)

    context["modal"] = modal

    if request is None:
        return context

    # ONLINE
    if session.online:
        return render(
            request, "game/player_control/player_control_online.html", context
        )

    # LOCAL
    if not session.online:
        return render(
            request, "game/player_control/player_control.html", context
        )
