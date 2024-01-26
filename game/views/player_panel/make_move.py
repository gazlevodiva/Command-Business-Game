from django.http import JsonResponse

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.CommandPayments import CommandPayments

from game.methods.MoveMethods import set_skip_move
from game.methods.MoveMethods import set_start_move
from game.methods.MoveMethods import set_dice_roll
from game.methods.PlayerMethods import firstInvestToCommandBusiness

from game.decorators import check_user_session_hash

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

    # if is_rolled:
    #     set_end_move(current_player_move)

    # For new level
    is_newlevel = False
    next_cell = False
    # next_cell_name = False
    next_move_value = False

    # The player went around the circle and stood further from the start
    if new_player_position > 25:

        next_cell = True
        next_move_value = new_player_position - 25

        is_newlevel = True
        new_player_position = 1
        # next_cell_name = GAME_FIELD[next_move_value + 1]

    # If player go on start
    if new_player_position == 25:
        is_newlevel = True
        new_player_position = 1

    if is_rolled:
        # Set up dice move
        dice_move = (
            Moves.objects
            .create(
                player=player,
                position=current_player_move.position
            )
        )
        set_dice_roll(dice_move, dice_value)

        # New move
        move = (
            Moves.objects
            .create(
                player=player,
                number=dice_move.number,
                position=new_player_position
            )
        )

    # Create new move for player and action position
    if not is_rolled:
        move = (
            Moves.objects
            .create(
                player=player,
                position=new_player_position
            )
        )

    set_start_move(move)

    context = {}

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

    context['type'] = "player_move"
    context['player_id'] = player.id
    context['player_name'] = player.name
    context['move_id'] = move.id
    context['move_stage'] = "START"
    context['move_number'] = move.number
    context['cell_name'] = GAME_FIELD[new_player_position]
    context['cell_position'] = new_player_position
    context['next_cell'] = next_cell
    # context['next_cell_name'] = next_cell_name
    context['next_cell_move'] = next_move_value

    response = JsonResponse(context)
    return response
