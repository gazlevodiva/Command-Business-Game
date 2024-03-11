from game.models.Actions import Actions
from game.models.Moves import Moves

from typing import Optional

from django.db import transaction


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


def set_skip_move(move: Moves) -> Optional[Actions]:
    """
    Creates an action indicating that the player 
    has decided to skip their turn.

    This function is used when a player chooses 
    not to make a move. It logs this decision
    as an action with the specified attributes, 
    marking the move as skipped.

    Args:
    move (Moves): The move instance that is being skipped.

    Returns:
    Optional[Actions]: The action instance created for the skipped move. 
    Returns None if the action creation fails due to an error.
    """
    try:
        action = Actions.objects.create(
            move=move,
            name="Пропускает ход",
            category="OTHER",
            is_command=False,
            is_personal=True,
            is_public=True,
        )
        return action
    except Exception as e:
        print(f"Error in set_skip_move: {e}")
        return None


def set_end_move(move: Moves) -> Optional[Actions]:
    """
    Creates an 'end move' action for a given move.

    This function is responsible for marking the end of a player's move
    by creating a corresponding action in the database. It sets the move
    stage to 'END', indicating that the player has completed their turn.

    Args:
    move (Moves): The move instance for which the end action is being set.

    Returns:
    Optional[Actions]: The action instance created for marking
                       the end of the move. Returns None if the action
                       creation fails for any reason.
    """
    try:
        action = Actions.objects.create(
            move=move,
            move_stage="END",
            name="Закончил ход",
            category="POSITION",
            visible=False,
            is_command=False,
            is_personal=True,
            is_public=False,
        )
        return action
    except Exception as e:
        print(f"Error in set_end_move: {e}")
        return None


def set_start_move(move: Moves) -> Optional[Actions]:
    """
    Creates an action at the start of a move, indicating 
    the player's position and whether it involves a 
    command based on the game field.

    Args:
    move (Moves): The current move instance.

    Returns:
    Optional[Actions]: The created action instance or None.
    """
    try:
        # Determine if the current move's position involves a command
        is_command = GAME_FIELD.get(move.position, "") == "command-surprise-cell"

        action = Actions.objects.create(
            move=move,
            move_stage="START",
            name=f"Переходит на {GAME_FIELD.get(move.position, 'undefined-cell')}",
            category="POSITION",
            visible=False,
            is_command=is_command,
            is_personal=True,
            is_public=False,
        )
        return action
    except Exception as e:
        print(f"Error in set_start_move: {e}")
        return None


def set_dice_roll(move: Moves, value: str) -> Optional[Actions]:
    """
    Records two actions for a move: the action of rolling
    a dice and the result of the roll.

    Args:
    move (Moves): The move instance to which the dice
    roll actions are related.
    value (str): The result of the dice roll to record
    as the second action's name.

    Returns:
    Optional[bool]: True if actions were successfully created, or None.
    """
    try:
        with transaction.atomic():
            # Recording the action of rolling a dice
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

            # Recording the result of the dice roll
            value_action = Actions.objects.create(
                move=move,
                move_stage="END",
                name=str(value),
                category="DICE_VALUE",
                visible=False,
                is_command=False,
                is_personal=True,
                is_public=True,
            )
            return value_action
        
    except Exception as e:
        print(f"Error in set_dice_roll: {e}")
        return None


def set_go_to_start(move: Moves) -> Optional[Actions]:
    """
    Creates an action indicating that the player moves
    directly to the start.

    This function records a specific game action where a player
    is instructed to move directly to the start position.
    The action is made visible to everyone and is not considered
    a command action but rather a personal action that affects
    the player's position within the game.

    Args:
    move (Moves): The move instance for which the action is being set.

    Returns:
    Optional[Actions]: The created Actions instance if successful, or None.
    """
    try:
        action = Actions.objects.create(
            move=move,
            move_stage="CONTINUE",
            name="Переходит сразу на старт",
            category="OTHER",
            visible=True,
            is_command=False,
            is_personal=True,
            is_public=True,
        )
        return action
    except Exception as e:
        print(f"Error in set_go_to_start: {e}")
        return None


def set_back_to_start(move: Moves) -> Optional[Actions]:
    """
    Handles a game action where a player returns to the
    start position and a new move is initiated.

    This function performs several actions in sequence:
    - Marks the current move with a special action indicating
      a return to start.
    - Registers the end of the current move.
    - Creates a new move at the start position for the player.
    - Registers the start and end actions for the new move.

    Args:
    move (Moves): The current move instance to be ended and followed
    by a new start move.

    Returns:
    Optional[Moves]: The new move instance created at the start position,
    or None if an error occurs.
    """
    try:
        with transaction.atomic():
            # Marking the current move with a return-to-start action
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

            # Ending the current move
            set_end_move(move)

            # Creating a new move at the start position
            new_move = Moves.objects.create(player=move.player, position=1)

            # Registering start and end actions for the new move
            set_start_move(new_move)
            set_end_move(new_move)

            return new_move
        
    except Exception as e:
        print(f"Error in set_back_to_start: {e}")
        return None
