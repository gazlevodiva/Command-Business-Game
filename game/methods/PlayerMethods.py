from random import randint

from django.db.models import Sum, Subquery, OuterRef

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.models.MemoryAnswers import MemoryAnswers
from game.models.PlayersBusiness import PlayersBusiness
from game.models.CommandPayments import CommandPayments
from game.models.PlayersBusinessStatus import PlayersBusinessStatus


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

        name = f"📉 Инфляция"

        return Actions.objects.create(
            move=move,
            name=name,
            count=count,
            category="INFL",
            is_personal=True,
            is_public=True,
        )

    name = "Инфляции нет"

    return Actions.objects.create(
        move=move,
        name=name,
        count=0,
        category="OTHER",
        is_personal=True,
        is_public=False,
        visible=False,
    )


def getSalary(move):
    try:
        salary = SALARY[move.player.level]
    except:
        salary = 0

    return Actions.objects.create(
        move=move,
        name="Зарплата",
        count=salary,
        category="SLR",
        is_personal=True,
        is_public=False,
    )


def getBusinesses(player):
    res = PlayersBusiness.objects.annotate(
        latest_status=Subquery(
            PlayersBusinessStatus.objects.filter(players_business=OuterRef("pk"))
            .order_by("-move")
            .values("status")[:1]
        )
    ).filter(player=player, latest_status="ACTIVE")
    return res


def getCommandBusinesses(player=None):
    return getBusinesses(player).filter(is_command=True)


def newBusiness(move, business, is_command):
    if is_command:
        name = f"Командный бизнес. Стал администратором в {business.name}"

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
        name = f"Купил личный бизнес {business.name}"

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


def PlayerXReinvest(move):
    player_x = Player.objects.get(name="X", game_session=move.player.game_session)
    player_x_balance = getBalance(player_x)

    if player_x_balance == 0:
        return

    name = f"Вложил в командный бизнес {player_x_balance}"

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
    return (
        Actions.objects.filter(move__player__game_session=session)
        .filter(is_public=True)
        .order_by("-created_date")
    )


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
    players_list_query = (
        Player.objects.filter(visible=True)
        .filter(game_session=session)
        .order_by("created_at")
        .all()
    )

    if len(players_list_query) == 0:
        return False

    players_list = [player.id for player in players_list_query]

    last_action = (
        Actions.objects.filter(move__player__game_session=session)
        .filter(move__player__visible=True)
        .exclude(category__in=["VOTE_FOR", "VOTE_AGN"])
        .last()
    )

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
