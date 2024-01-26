from game.models.Actions import Actions
from game.models.Moves import Moves

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


def set_skip_move(move):
    return Actions.objects.create(
        move=move,
        name="Пропускает ход",
        category="OTHER",
        is_command=False,
        is_personal=True,
        is_public=True,
    )


def set_end_move(move):
    return Actions.objects.create(
        move=move,
        move_stage="END",
        name="Закончил ход",
        category="POSITION",
        visible=False,
        is_command=False,
        is_personal=True,
        is_public=False,
    )


def set_start_move(move):
    is_command = False
    if GAME_FIELD[move.position] == "command-surprise-cell":
        is_command = True

    return Actions.objects.create(
        move=move,
        move_stage="START",
        name=f"Переходит на {GAME_FIELD[move.position]}",
        category="POSITION",
        visible=False,
        is_command=is_command,
        is_personal=True,
        is_public=False,
    )


def set_dice_roll(move, value):
    Actions.objects.create(
        move=move,
        move_stage="START",
        name="Бросает кубик",
        category="DICE_VALUE",
        visible=False,
        is_command=False,
        is_personal=True,
        is_public=True,
    )

    Actions.objects.create(
        move=move,
        move_stage="END",
        name=value,
        category="DICE_VALUE",
        visible=False,
        is_command=False,
        is_personal=True,
        is_public=True,
    )


def set_go_to_start(move):
    return Actions.objects.create(
        move=move,
        move_stage="CONTINUE",
        name="Переходит сразу на старт",
        category="OTHER",
        visible=True,
        is_command=False,
        is_personal=True,
        is_public=True,
    )


def set_back_to_start(move):
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
