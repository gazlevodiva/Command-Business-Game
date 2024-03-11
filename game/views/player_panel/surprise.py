from random import choice

from game.models.Moves import Moves
from game.models.Actions import Actions
from game.models.Surprises import Surprises
from game.models.MemoryAnswers import MemoryAnswers
from game.models.CommandPayments import CommandPayments

from game.methods.PlayerMethods import get_player_categoties
from game.methods.BusinessMethods import getCommandBank

from django.db.models.query import QuerySet
from typing import Optional, List


def set_surprise(move: Moves) -> Optional[Surprises]:
    """
    Assigns a surprise to a given move based on player categories.

    Retrieves all surprises and player categories. Generates a surprise list
    relevant to the player's categories. If the list is not empty, a random
    surprise is chosen from it. If the list is empty, a random surprise is
    chosen from all available surprises. An action is then created with the
    selected surprise and linked to the move.

    Args:
    move (Moves): The move object to which the surprise will be assigned.

    Returns:
    Optional[Surprises]: The surprise object that was assigned to the move,
    or None if an error occurs.
    """
    try:
        surprises: QuerySet = Surprises.objects.all()
        categories: QuerySet = get_player_categoties(move.player)
        surprise_list: list = surprise_list_generator(surprises, categories)

        if surprise_list:
            surprise: Surprises = choice(surprise_list)
        else:
            surprise: Surprises = choice(surprises)

        # Creating an Action with the selected surprise
        Actions.objects.create(
            move=move,
            move_stage="CONTINUE",
            name=surprise.name,
            count=surprise.count,
            is_personal=True,
            is_public=True,
            is_command=False,
            category="SURP",
        )
        return surprise

    except (Surprises.DoesNotExist, Actions.DoesNotExist, Exception) as error:
        print("Error in  set_surprise:", error)
        return None


def get_memory(move: Moves) -> Optional[Surprises]:
    """
    Retrieves a memory based on the player's current game session
    or a default memory if none are available.

    Args:
    move (Moves): The move instance to retrieve a memory for.

    Returns:
    Optional[Surprises]: A Surprises instance or None if an error occurs.
    """
    try:
        # Attempt to retrieve memories for the current game session
        memories: QuerySet = Surprises.objects.filter(
            category="MEMO",
            session_id=move.player.game_session.id
        )

        # If there are no memories for the current game session,
        # retrieve default memories with session_id 0
        if not memories.exists():
            memories: QuerySet = Surprises.objects.filter(
                category="MEMO", session_id=0
            )

        # Exclude memories that have already been answered by the player
        answered_memories_ids: QuerySet = MemoryAnswers.objects.filter(
            action__move__player=move.player
        ).values_list("question__id", flat=True)

        available_memories: List = memories.exclude(
            id__in=answered_memories_ids
        )

        # Ensure that we can't choose from an empty QuerySet
        if available_memories.exists():
            return choice(list(available_memories))
        else:
            return choice(list(memories))

    except Exception as error:
        print("Error in  get_memory:", error)
        return None


def set_memory(move: Moves) -> Optional[Surprises]:
    """
    Sets a memory for the given move. It first tries to get memories
    related to the current game session. If none are found, it defaults to
    memories with session_id 0. It then excludes any memories already
    associated with the player and selects one at random to create an Action.

    Args:
    move (Moves): The move instance for which to set a memory.

    Returns:
    Optional[Surprises]: The selected memory instance, or None.
    """
    try:
        memory = get_memory(move)

        if memory:
            # Create an action with the selected memory
            Actions.objects.create(
                move=move,
                move_stage="CONTINUE",
                name=memory.name,
                count=memory.count,
                is_personal=True,
                is_public=True,
                is_command=False,
                category="MEMO",
            )
            return memory
        else:
            # No valid memory could be found or created
            return None

    except Exception as error:
        print("Error in set_memory:", error)
        return None


def set_command_surprise(move: Moves) -> Optional[Surprises]:
    """
    Sets a command surprise for the given move. Selects a random
    command surprise, calculates the count based on specific logic
    (inflation), and creates related command payment and action
    entries in the database.

    Args:
    move (Moves): The move instance for which to set a command surprise.

    Returns:
    Optional[Surprises]: The Surprises instance selected or None.
    """
    try:
        #  Retrieving all command surprises
        all_command_surprises: QuerySet = Surprises.objects.filter(
            category="COMMAND"
        )

        # Ensure there is at least one command surprise available
        if not all_command_surprises.exists():
            print("No command surprises available.")
            return None

        command_surprise: Surprises = choice(list(all_command_surprises))

        # Inflation logic
        if command_surprise.count == 0:
            command_bank: int = getCommandBank(move.player.game_session)
            count = -int(command_bank / 2)
        else:
            count = command_surprise.count

        # Creating a CommandPayments entry
        CommandPayments.objects.create(
            move=move,
            category="SURP",
            count=count,
        )

        # Creating an Actions entry
        Actions.objects.create(
            move=move,
            move_stage="CONTINUE",
            name=command_surprise.name,
            count=0, 
            is_personal=True,
            is_public=True,
            is_command=True,
            category="SURP",
        )

        return command_surprise

    except Exception as error:
        print(f"Error in set_command_surprise: {error}")
        return None


def surprise_list_generator(
    surprises: QuerySet,
    categories: QuerySet
) -> List[Surprises]:
    """
    Generates a list of surprises based on the given categories.

    This function takes a queryset of all surprises and a queryset
    of categories, filters surprises by each category provided,
    and aggregates them into a list. It assumes that both the surprises
    and categories are querysets containing Surprises model instances
    and their related category model instances, respectively.

    Args:
    surprises (QuerySet): A queryset containing Surprises instances.
    categories (QuerySet): A queryset containing category instances.

    Returns:
    List[Surprises]: A list of Surprises instances
    filtered by the given categories.
    """
    result: List[Surprises] = []

    # Iterate through the categories to filter surprises
    for category in categories:
        try:
            # Here we assume 'category=category' is the correct way to filter
            # If the actual field is different, replace 'category'
            # with the correct field name
            category_surprises: QuerySet = surprises.filter(category=category)

            # Extend the result list with the filtered surprises
            result.extend(list(category_surprises))

        except Surprises.DoesNotExist:
            # Handle the case where the filter does
            # not find any surprises for a category
            continue  # Skip to the next category

    return result
