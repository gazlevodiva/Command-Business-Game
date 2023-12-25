from django.shortcuts import render
from django.shortcuts import redirect

from django.http import JsonResponse

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Business import Business
from game.models.Surprises import Surprises
from game.models.MemoryAnswers import MemoryAnswers
from game.models.CommandPayments import CommandPayments

from game.methods.MoveMethods import set_end_move
from game.methods.MoveMethods import set_skip_move
from game.methods.MoveMethods import set_start_move
from game.methods.MoveMethods import set_dice_roll

from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import newBusiness
from game.methods.PlayerMethods import getBusinesses
from game.methods.PlayerMethods import playerTurn
from game.methods.PlayerMethods import isOpenCommandBusiness
from game.methods.PlayerMethods import firstInvestToCommandBusiness

from game.methods.BusinessMethods import getVotion
from game.methods.BusinessMethods import setVotion
from game.methods.BusinessMethods import playerIdForVotion
from game.methods.BusinessMethods import getCommandBank
from game.methods.BusinessMethods import getCommandShare
from game.methods.BusinessMethods import getBusinessPayments

from game.decorators import check_user_session_hash

from django.core.serializers import serialize
import json

from .new_level import is_new_level
from .new_level import set_new_level
from .surprise import set_memory
from .surprise import set_surprise
from .surprise import set_command_surprise

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
def move_details(request, session, player_id):
    player = Player.objects.get(pk=player_id)
    player_move = Moves.objects.filter(player=player).last()
    player_last_action = (
        Actions.objects.filter(move__number=player_move.number).last()
    )

    context = {
        "type": "move_details",
        "player_id": player_id,
        "player_name": player.name,
        "move_id": player_move.id,
        "move_stage": player_last_action.move_stage,
        "cell_name": GAME_FIELD[player_move.position],
        "cell_position": player_move.position,
    }

    # Vote for buy command business
    if player.id in playerIdForVotion(player.game_session):
        context["votion"] = getVotion(player_move)
    else:
        context["votion"] = False

    # Does the player have a new_level?
    new_level_details = is_new_level(player)

    first_invest_chance = firstInvestToCommandBusiness(player_move)
    context["first_invest_chance"] = first_invest_chance

    if new_level_details:
        context["is_new_level"] = new_level_details

    if not new_level_details:
        context["action_name"] = str(player_last_action.name)
        context["action_count"] = player_last_action.count
        context["action_category"] = player_last_action.category

    # Memory
    if player_last_action.category == "MEMO":
        memory = Surprises.objects.get(
            name=player_last_action.name, session_id=session.id
        )
        context["memory_id"] = memory.id

    # Command surprise
    if player_last_action.category == "SURP" and player_last_action.is_command:
        command_payment = CommandPayments.objects.get(move=player_move)
        context["action_count"] = command_payment.count

    return JsonResponse(context)


@check_user_session_hash
def player_move(request, session, player_id, dice_value):
    # string param to int - '2-5' -> 7
    is_rolled = False
    if len(dice_value.split('-')) == 2:
        is_rolled = True

    move_value = sum([int(x) for x in dice_value.split('-')])

    # Get players positiones and math new position
    player = Player.objects.get(pk=player_id)
    current_player_move = Moves.objects.filter(player=player).last()
    new_player_position = current_player_move.position + move_value

    # For new level
    is_newlevel = False
    next_cell = False
    next_cell_name = False
    next_move_value = False

    # The player went around the circle and stood further from the start
    if new_player_position > 25:
        is_newlevel = True
        next_cell = True
        next_move_value = new_player_position - 25
        next_cell_name = GAME_FIELD[next_move_value + 1]
        new_player_position = 1

    # If player go on start
    if new_player_position == 25:
        is_newlevel = True
        new_player_position = 1

    # Create new move for player and action position
    move = Moves.objects.create(player=player, position=new_player_position)
    if is_rolled:
        set_dice_roll(move, dice_value)
    set_start_move(move)

    context = {
        "type": "player_move",
        "player_id": player_id,
        "player_name": player.name,
        "move_id": move.id,
        "move_stage": "START",
        "cell_name": GAME_FIELD[new_player_position],
        "cell_position": new_player_position,
        "next_cell": next_cell,
        "next_cell_name": next_cell_name,
        "next_cell_move": next_move_value,
    }

    # For create a new level action with new move, not old
    if is_newlevel:
        set_new_level(move)
        context["is_new_level"] = is_new_level(player)

    if not is_newlevel:
        context["is_new_level"] = []

    # SURPRISE
    if GAME_FIELD[new_player_position] == "surprise-cell":
        surprise = set_surprise(move)
        context["surprise_id"] = surprise.id
        context["action_name"] = surprise.name
        context["action_count"] = surprise.count

    # MEMORY
    if GAME_FIELD[new_player_position] == "memory-cell":
        memory = set_memory(move)
        context["memory_id"] = memory.id
        context["action_name"] = memory.name
        context["action_count"] = memory.count

    # COMMAND SURPRISE
    if GAME_FIELD[new_player_position] == "command-surprise-cell":
        first_invest_chance = firstInvestToCommandBusiness(move)
        context["first_invest_chance"] = first_invest_chance

        # If first time and open command investments
        if not first_invest_chance:
            command_surprise = set_command_surprise(move)
            context["surprise_id"] = command_surprise.id
            context["action_name"] = command_surprise.name

            command_payment = CommandPayments.objects.get(move=move)
            context["action_count"] = command_payment.count

    # SKIP MOVE
    if GAME_FIELD[new_player_position] == "skip-move-cell":
        set_skip_move(move)

    response = JsonResponse(context)
    return response


@check_user_session_hash
def whois_turn_data(request, session, player_id):
    # Who is turn
    player_turn_id = playerTurn(session)
    player_turn = Player.objects.get(pk=player_turn_id)
    player_turn_last_move = Moves.objects.filter(player=player_turn).last()

    context = {}
    context["move_id"] = player_turn_last_move.id
    context["move_number"] = player_turn_last_move.number
    context["player_id"] = player_turn.id
    context["player_name"] = player_turn.name

    if player_id in playerIdForVotion(player_turn.game_session):
        context["votion"] = getVotion(player_turn_last_move)
    else:
        context["votion"] = False

    return JsonResponse(context)


@check_user_session_hash
def player_finish_move(request, session, move_id):
    move = Moves.objects.get(pk=move_id)
    set_end_move(move)
    context = {"result": True}
    return JsonResponse(context)


@check_user_session_hash
def player_back_to_start(request, session, move_id):
    move = Moves.objects.get(pk=move_id)

    Actions.objects.create(
        move=move,
        move_stage="CONTINUE",
        name="Вернулся на старт",
        category="OTHER",
        visible=True,
        is_command=False,
        is_personal=True,
        is_public=True,
    )

    set_end_move(move)  # end back to start position

    # change position to start cell
    new_move = Moves.objects.create(player=move.player, position=1)

    # Set start position action
    set_start_move(new_move)

    # Set end move position action
    set_end_move(new_move)

    context = {"result": True}
    return JsonResponse(context)


@check_user_session_hash
def player_go_to_start(request, session, move_id):
    move = Moves.objects.get(pk=move_id)

    Actions.objects.create(
        move=move,
        move_stage="CONTINUE",
        name="Переходит сразу на старт",
        category="OTHER",
        visible=True,
        is_command=False,
        is_personal=True,
        is_public=True,
    )

    context = {"result": True, "move_id": move_id}
    return JsonResponse(context)


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

    context = {
        "player_id": player.id,
        "businesses": businesses,
        "player_balance": player_balance,
        "command_share": share,
        "command_count": count,
        "command_bank": bank,
    }
    response = JsonResponse(context)
    return response


@check_user_session_hash
def player_control_data(request, session, player_id):
    player = Player.objects.get(pk=player_id)
    player_balance = getBalance(player)
    share, count = getCommandShare(player)
    bank = getCommandBank(session)

    # whos player Turn???
    player_turn = playerTurn(session)
    if player == player_turn:
        is_player_turn = True

    if player != player_turn:
        is_player_turn = False

    is_open_command_business = isOpenCommandBusiness(player)

    context = {
        "player_id": player.id,
        "player_name": player.name,
        "player_level": player.level,
        "player_balance": player_balance,
        "command_share": share,
        "command_count": count,
        "command_bank": bank,
        "is_player_turn": is_player_turn,
        "is_open_command_business": is_open_command_business,
    }
    response = JsonResponse(context)
    return response


# Main player controller
@check_user_session_hash
def player_control(request=None, session=None, player_id=None, modal=False):
    # Set context
    context = {}
    context["game_session"] = session

    # Get players businesses
    player = Player.objects.get(pk=player_id)
    context["player"] = player

    last_move = Moves.objects.filter(player=player).last()
    context["move"] = last_move
    context["current_player_position"] = last_move.position

    # whos player Turn???
    player_turn_id = playerTurn(session)
    player_turn = Player.objects.get(pk=player_turn_id)

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
                is_command=False,
                is_personal=True,
                is_public=True,
            )

            MemoryAnswers.objects.create(
                action=action,
                question=surprise,
                answer=memory_answer,
            )

        return redirect(f"/player_control_{player_id}/")

    is_open_command_business = isOpenCommandBusiness(player)
    context["is_open_command_business"] = is_open_command_business

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
