from random import choice

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Surprises import Surprises
from game.models.MemoryAnswers import MemoryAnswers
from game.models.CommandPayments import CommandPayments
from game.methods.NotificationModal import Modal

from game.views.player_panel import player_controller

from game.methods.PlayerMethods import getPlayerCategoties
from game.methods.BusinessMethods import getCommandBank

from game.decorators import check_user_session_hash
from django.db.models import Subquery, OuterRef


def set_surprise(move):
    all_surprises = Surprises.objects.all()
    all_categories = getPlayerCategoties(move.player)
    surprise_list = suprise_list_generator(all_surprises, all_categories)

    if len(surprise_list) > 0:
        surprise = choice(surprise_list)
    else:
        # Everything above is used only to determine the surprise,
        # taking into account the business categories that the user has.
        surprise = choice(all_surprises)

    # Make an Action
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


def set_memory(move):
    memories = Surprises.objects.filter(
        category="MEMO", session_id=move.player.game_session.id
    )
    if not memories:
        memories = Surprises.objects.filter(category="MEMO", session_id=0)

    # Get all answered players memories
    answered_questions_subquery = MemoryAnswers.objects.filter(
        action__move__player=OuterRef("pk")
    ).values("question")
    all_memories = (
        memories.exclude(pk__in=Subquery(answered_questions_subquery))
    )

    # Get memory
    memory = choice(all_memories)

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


def set_command_surprise(move):
    all_command_surprises = Surprises.objects.filter(category="COMMAND")
    command_surprise = choice(all_command_surprises)

    # Inflation
    if command_surprise.count == 0:
        command_bank = getCommandBank(move.player.game_session)
        count = -int(command_bank / 2)

    else:
        count = command_surprise.count

    # Make command Payment
    CommandPayments.objects.create(
        move=move,
        category="SURP",
        count=count,
    )

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


@check_user_session_hash
def surprise(request, session, player_id, surprise_type):
    player = Player.objects.get(pk=player_id)

    # Get categories by surprise type
    all_categories = {
        "surp": getPlayerCategoties(player),
        "memo": ["MEMO"],
        "cmnd": ["COMMAND"],
    }[surprise_type]

    # Get all surprises
    all_surprises = Surprises.objects.all()
    if surprise_type == "memo":
        answered_questions_subquery = (
            MemoryAnswers.objects
            .filter(
                action__move__player=OuterRef("pk")
            )
            .values("question")
        )
        all_surprises = (
            all_surprises
            .exclude(
                pk__in=Subquery(answered_questions_subquery)
            )
        )

    surprise_list = suprise_list_generator(all_surprises, all_categories)

    # Random surprise from surprise_list
    if len(surprise_list) == 0:
        surprise = choice(all_surprises)
    else:
        surprise = choice(surprise_list)

    action_name = {
        "surp": f'Сюрприз - "{surprise.name}" {surprise.count}.',
        "memo": surprise.name,
        "cmnd": f"{surprise.name} {surprise.count}.",
    }[surprise_type]

    modal_name = {
        "surp": "Сюрпрайз!",
        "memo": "Мемори!",
        "cmnd": "Сюрприз для Командного бизнеса!",
    }[surprise_type]

    # Create modal
    modal = Modal(modal_name, player, surprise.pk)
    modal.surprise = surprise
    modal.type = surprise_type

    # If surprise personal
    action_count = int(surprise.count)
    is_command = False

    if surprise_type == "memo":
        return player_controller.player_control(
            request=request, player_id=player_id, modal=modal
        )

    # Get new position from cookie
    controller_position = request.COOKIES.get("controller_position")

    # Make new move
    move = Moves.objects.create(player=player, position=controller_position)

    # If suprise Command
    if surprise_type == "cmnd":
        # Becouse action is personal counter
        action_count = 0
        is_command = True

        if surprise.count == 0:
            command_bank = getCommandBank(player.game_session)
            count = -int(command_bank / 2)
            action_name = f"{surprise.name} {count}"
        else:
            count = surprise.count

        # Make command Payment with no player
        CommandPayments.objects.create(move=move, category="SURP", count=count)

    Actions.objects.create(
        move=move,
        name=action_name,
        count=action_count,
        is_personal=True,
        category="SURP",
        is_command=is_command,
    )

    return player_controller.player_control(
        request=request, player_id=player_id, modal=modal
    )


def suprise_list_generator(surprises, categories) -> list:
    result = []

    for category in categories:
        category_surprises = surprises.filter(category=category)

        if len(category_surprises) > 0:
            for surprise in category_surprises:
                result.append(surprise)

    return result
