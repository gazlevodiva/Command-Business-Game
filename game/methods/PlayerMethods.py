from random import randint

from django.db.models import Q, Sum, Subquery, OuterRef

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Surprises import Surprises
from game.models.Actions import Actions
from game.models.MemoryAnswers import MemoryAnswers
from game.models.PlayersBusiness import PlayersBusiness
from game.models.CommandPayments import CommandPayments
from game.models.PlayersBusinessStatus import PlayersBusinessStatus
from game.methods.BusinessMethods import getBusinessPayments
from game.methods.MoveMethods import set_end_move

from typing import Optional
from django.db import transaction


SALARY = {
    1: 5000,
    2: 6000,
    3: 7200,
    4: 8500,
    5: 10100,
    6: 12000,
    7: 14200,
    8: 16800,
    9: 19800,
    10: 23300,
    11: 14900,
    12: 7800,
    13: 1600,
    14: -3700,
    15: -8500,
    16: -12900,
    17: -17100,
    18: -21100,
    19: -25100,
    20: -29200,
}


def getPlayer(player_id) -> any:
    return Player.objects.get(pk=player_id)


def getBalance(player) -> any:
    return Actions.objects.filter(
        move__player=player,
    ).aggregate(
        Sum("count")
    )["count__sum"]


def getMemoryAnswers(player):
    return MemoryAnswers.objects.filter(action__move__player=player)


def getInflation(move):
    inflation = randint(1, 10)
    if inflation == 1:
        player_balance = getBalance(move.player)

        if player_balance <= 0:
            count = 0

        if player_balance > 0:
            count = -int(player_balance / 2)

        return Actions.objects.create(
            move=move,
            name="📉Инфляция",
            count=count,
            category="INFL",
            is_personal=True,
            is_public=True,
        )

    return None


def getSalary(move):
    try:
        salary = SALARY[move.player.level]
    except Exception as e:
        print("Salary end", e)
        salary = 0

    return Actions.objects.create(
        move=move,
        name="Получил зарплату",
        count=salary,
        category="SLR",
        is_personal=True,
        is_public=False,
    )


def getBusinesses(player):
    return (
        PlayersBusiness.objects
        .annotate(
            latest_status=Subquery(
                PlayersBusinessStatus.objects
                .filter(players_business=OuterRef("pk"))
                .order_by("-move")
                .values("status")[:1]
            )
        )
        .filter(
            Q(player=player) &
            (Q(latest_status="ACTIVE") | Q(latest_status="DEFOULT"))
        )
    )


def get_business_card_info(player):
    business_card_info = []
    for player_business in getBusinesses(player):
        business_payments_model = getBusinessPayments(player_business)
        business_payments = []

        for payment in business_payments_model:
            business_payments.append(
                {
                    "move_id": payment.move.id,
                    "count": payment.count,
                    "rentability": payment.rentability,
                    "defoult_probability": payment.defoult_probability,
                    "player_level": payment.player_level,
                }
            )

        business_card_info.append(
            {
                "business": {
                    "id": player_business.id,
                    "name": player_business.business.name,
                    "status": player_business.latest_status,
                    "is_command": player_business.is_command,
                    "business_cost": player_business.business.cost,
                    "min_rent": player_business.business.min_rent,
                    "max_rent": player_business.business.max_rent,
                },
                "business_payments": business_payments,
            }
        )

    business_card_info.sort(key=lambda x: x['business']['status'] == 'DEFOULT')
    return business_card_info


def getCommandBusinesses(player=None):
    return getBusinesses(player).filter(is_command=True)


def newBusiness(move, business, is_command):
    if is_command:
        name = f"Стал администратором в КБ {business.name}"

        Actions.objects.create(
            move=move,
            move_stage="END",
            name=name,
            count=0,
            category="BUY_BIS",
            is_command=is_command,
            is_personal=True,
            is_public=True,
        )

        CommandPayments.objects.create(
            move=move, category="BUY_BIS", count=-business.cost
        )

        players_business = PlayersBusiness.objects.create(
            player=move.player,
            business=business,
            is_command=is_command,
        )

    if not is_command:
        name = f"Купил ЛБ {business.name}"

        Actions.objects.create(
            move=move,
            move_stage="END",
            name=name,
            count=-business.cost,
            category="BUY_BIS",
            is_personal=True,
            is_public=True,
        )

        players_business = PlayersBusiness.objects.create(
            player=move.player,
            business=business,
            is_command=is_command,
        )

    PlayersBusinessStatus.objects.create(
        players_business=players_business,
        move=move,
        status="ACTIVE"
    )


def sell_command_business(move: Moves, players_business: PlayersBusiness):
    """
    Executes a sell action for a player's business in the game.

    This function is called when a player decides to sell their business.
    It calculates the sell price of the business, logs the sale as an action,
    and records the payment. This action and its details are logged
    with the specified attributes, marking the business as sold.

    Args:
        move (Moves): The move instance associated with the selling action.
        players_business (PlayersBusiness): The business that is being sold.
    """
    try:
        with transaction.atomic():
            sell_price = players_business.business.cost*0.95
            name = f"Продал КБ {players_business.business.name}"

            Actions.objects.create(
                move=move,
                move_stage="START",
                count=0,
                name=name,
                category="SELL_BIS",
                is_command=True,
                is_personal=True,
                is_public=True,
            )

            CommandPayments.objects.create(
                count=sell_price,
                category="SELL_BIS",
                move=move
            )

            PlayersBusinessStatus.objects.create(
                move=move,
                players_business=players_business,
                status="SOLD"
            )

    except Exception as e:
        print(f"Error in sell_command_business: {e}")


def sell_personal_business(move: Moves, players_business: PlayersBusiness):
    """
    Executes a sell action for a player's business in the game.

    This function is called when a player decides to sell their business.
    It calculates the sell price of the business, logs the sale as an action,
    and records the payment. This action and its details are logged
    with the specified attributes, marking the business as sold.

    Args:
        move (Moves): The move instance associated with the selling action.
        players_business (PlayersBusiness): The business that is being sold.
    """
    try:
        with transaction.atomic():
            sell_price = players_business.business.cost*0.95
            name = f"Продал ЛБ {players_business.business.name}"

            Actions.objects.create(
                move=move,
                move_stage="START",
                count=sell_price,
                name=name,
                category="SELL_BIS",
                is_personal=True,
                is_public=False,
            )

            PlayersBusinessStatus.objects.create(
                move=move,
                players_business=players_business,
                status="SOLD"
            )

    except Exception as e:
        print(f"Error in sell_personal_business: {e}")


def PlayerXReinvest(move):
    player_x = Player.objects.get(name="X", game_session=move.player.game_session)
    player_x_balance = getBalance(player_x)

    if player_x_balance == 0:
        return

    name = f"Вложил в КБ {player_x_balance}"

    new_move = Moves.objects.create(player=player_x, number=move.number)

    Actions.objects.create(
        move=new_move,
        name=name,
        count=-player_x_balance,
        category="CMND",
        is_command=True,
        visible=False,
        is_personal=False,
    )

    CommandPayments.objects.create(
        move=new_move, category="DEPOSITE", count=player_x_balance
    )


def getActions(session):
    return Actions.objects.filter(move__player__game_session=session).order_by(
        "-created_date"
    )


def getActionsDashboard(session):
    game_session_actions = (
        Actions.objects
        .filter(move__player__game_session=session)
        .filter(is_public=True)
        .order_by("-created_date")
    )
    return game_session_actions


def getPlayerCategoties(player):
    player_businesses = getBusinesses(player)

    categories = ["PERSONAL"]
    for player_business in player_businesses:
        if player_business.business.category not in categories:
            categories.append(player_business.business.category)

    return categories


def getPlayerSurprises(move):
    return Actions.objects.filter(
        move=move,
        category="SURP",
    )


def getBusinessesCost(player):
    return PlayersBusiness.objects.filter(player=player).aggregate(
        Sum("business__cost")
    )["business__cost__sum"]


def playerTurn(session):
    # Get all actions
    players_list_query = (
        Player.objects.filter(visible=True)
        .filter(game_session=session)
        .order_by("created_at")
        .all()
    )

    if len(players_list_query) == 0:
        return False

    # Get list of players
    players_list = [player.id for player in players_list_query]

    # Get last action ftom game session
    player_actions = (
        Actions.objects
        .filter(move__player__game_session=session)
        .filter(move__player__visible=True)
        .exclude(category__in=["VOTE_FOR", "VOTE_AGN", "BSNS"])
    )

    # Get the last action
    last_action = player_actions.last()

    # If player drop the dice in last move, we check start and end position
    player_move_actions = (
        player_actions
        .filter(move__number=last_action.move.number)
    )
    if player_move_actions.filter(category="DICE_VALUE").exists():

        # Get dice action
        dice_action = (
            player_move_actions
            .filter(category="DICE_VALUE")
            .get(move_stage="END")
        )

        # get dice value from action
        dice_action_value = sum([int(x) for x in dice_action.name.split('-')])

        # Check finish position to current position
        finish_position = dice_action.move.position + dice_action_value
        if finish_position > 25:
            finish_position = finish_position - 24

        if finish_position == 25:
            finish_position = 1

        current_position = last_action.move.position

        # return player_id to finish moves
        if current_position != finish_position:
            return dice_action.move.player.id

    if last_action.move.position == 14:
        return last_action.move.player.id

    if last_action.move_stage == "START":
        return last_action.move.player.id

    if last_action.move_stage == "CONTINUE":
        return last_action.move.player.id

    player_last_move = (
        Actions.objects.filter(move__player__game_session=session)
        .filter(move__player__visible=True)
        .filter(move_stage="END")
        .last()
    )
    player = player_last_move.move.player

    if not player_last_move:
        return players_list[0]

    try:
        last_move_player_index = players_list.index(player.id)
    except Exception as e:
        print("Не удалось определить последнего игрока.", e)
        return False

    next_player_index = (last_move_player_index + 1) % len(players_list)
    next_player_id = players_list[next_player_index]
    return next_player_id


def isOpenCommandBusiness(player) -> bool:
    return Actions.objects.filter(
        category="POSITION",
        is_command=True,
        move__player=player,
    ).exists()


def firstInvestToCommandBusiness(move) -> bool:
    # Command positions count
    command_position = Actions.objects.filter(
        category="POSITION",
        is_command=True,
        move__player=move.player,
    ).count()

    # Command payment
    command_payment = CommandPayments.objects.filter(
        move__player=move.player,
    ).exists()

    result = False

    if not command_payment:
        result = True

    if command_position == 1:
        result = True

    return result


def first_invest_to_cb(move: Moves, payment: int):
    """
    Executes a sell action for a player's business in the game.

    This function is called when a player decides to sell their business.
    It calculates the sell price of the business, logs the sale as an action,
    and records the payment. This action and its details are logged
    with the specified attributes, marking the business as sold.

    Args:
        move (Moves): The move instance associated with the selling action.
        players_business (PlayersBusiness): The business that is being sold.
    """
    try:
        with transaction.atomic():
            CommandPayments.objects.create(
                move=move,
                category="DEPOSITE",
                count=payment,
            )

            Actions.objects.create(
                move=move,
                category="CMND",
                name="Вложил средства в КБ",
                count=-payment,
                is_command=True,
                is_personal=True,
                is_public=True,
            )

            set_end_move(move)

    except Exception as e:
        print(f"Error in first_invest_to_cb: {e}")


def invest_to_cb(move: Moves, payment: int):
    """
    Executes a sell action for a player's business in the game.

    This function is called when a player decides to sell their business.
    It calculates the sell price of the business, logs the sale as an action,
    and records the payment. This action and its details are logged
    with the specified attributes, marking the business as sold.

    Args:
        move (Moves): The move instance associated with the selling action.
        players_business (PlayersBusiness): The business that is being sold.
    """
    try:
        with transaction.atomic():
            new_move = Moves.objects.create(
                player=move.player, position=move.position
            )

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

    except Exception as e:
        print(f"Error in invest_to_cb: {e}")


def set_memory_answer(move: Moves, memory: Surprises, answer: str):
    """
    Executes a sell action for a player's business in the game.

    This function is called when a player decides to sell their business.
    It calculates the sell price of the business, logs the sale as an action,
    and records the payment. This action and its details are logged
    with the specified attributes, marking the business as sold.

    Args:
        move (Moves): The move instance associated with the selling action.
        players_business (PlayersBusiness): The business that is being sold.
    """
    try:
        with transaction.atomic():
            action = Actions.objects.create(
                move=move,
                move_stage="END",
                name=memory.name,
                count=0,
                category="MEMO",
                visible=False,
                is_command=False,
                is_personal=True,
                is_public=False,
            )

            MemoryAnswers.objects.create(
                action=action,
                question=memory,
                answer=answer,
            )

    except Exception as e:
        print(f"Error in set_memory_answer: {e}")


def get_player_categoties(player):
    player_businesses = getBusinesses(player)

    categories = ["PERSONAL"]
    for player_business in player_businesses:
        if player_business.business.category not in categories:
            categories.append(player_business.business.category)

    return categories


def who_is_turn(session):
    # Get all actions
    players_list_query = (
        Player.objects.filter(visible=True)
        .filter(game_session=session)
        .order_by("created_at")
        .all()
    )

    if len(players_list_query) == 0:
        return False

    # Get list of players
    players_list = [player.id for player in players_list_query]

    # Get last action ftom game session
    player_actions = (
        Actions.objects
        .filter(move__player__game_session=session)
        .filter(move__player__visible=True)
        .exclude(category__in=["VOTE_FOR", "VOTE_AGN", "BSNS"])
    )

    # Get the last action
    last_action = player_actions.last()

    # If player drop the dice in last move, we check start and end position
    player_move_actions = (
        player_actions
        .filter(move__number=last_action.move.number)
    )
    if player_move_actions.filter(category="DICE_VALUE").exists():

        # Get dice action
        dice_action = (
            player_move_actions
            .filter(category="DICE_VALUE")
            .get(move_stage="END")
        )

        # get dice value from action
        dice_action_value = sum([int(x) for x in dice_action.name.split('-')])

        # Check finish position to current position
        finish_position = dice_action.move.position + dice_action_value
        if finish_position > 25:
            finish_position = finish_position - 24

        if finish_position == 25:
            finish_position = 1

        current_position = last_action.move.position

        # return player_id to finish moves
        if current_position != finish_position:
            return dice_action.move.player.id

    if last_action.move.position == 14:
        return last_action.move.player.id

    if last_action.move_stage == "START":
        return last_action.move.player.id

    if last_action.move_stage == "CONTINUE":
        return last_action.move.player.id

    player_last_move = (
        Actions.objects.filter(move__player__game_session=session)
        .filter(move__player__visible=True)
        .filter(move_stage="END")
        .last()
    )
    player = player_last_move.move.player

    if not player_last_move:
        return players_list[0]

    try:
        last_move_player_index = players_list.index(player.id)
    except Exception as e:
        print("Не удалось определить последнего игрока.", e)
        return False

    next_player_index = (last_move_player_index + 1) % len(players_list)
    next_player_id = players_list[next_player_index]
    return next_player_id
