from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import getBusinesses
from game.methods.PlayerMethods import getPlayerSurprises

from game.models.CommandPayments import CommandPayments
from game.models.PlayersBusiness import PlayersBusiness
from game.models.Actions import Actions
from game.models.Player import Player

from django.db.models import Sum
from django.db.models import Max
from django.db.models import Min
from django.db.models import Count
from django.db.models import Q
from django.db.models import F


class Achievement:
    def __init__(self, title, text):
        self._title = title
        self._text = text

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value


def getAchievements(players):
    # Нажал на кнопку “Сюрприз” больше других игроков
    SurpriseMan = (
        Player.objects.annotate(
            num_surp_actions=Count(
                "moves__actions", filter=Q(moves__actions__category="SURP")
            )
        )
        .order_by("-num_surp_actions")
        .first()
    )

    # Нажал на кнопку “Сюрприз для КБ” больше других игроков
    CommandSurpriseMan = (
        Player.objects.annotate(
            num_command_surp_actions=Count(
                "moves__actions",
                filter=Q(
                    moves__actions__category="SURP", moves__actions__is_command=True
                ),
            )
        )
        .order_by("-num_command_surp_actions")
        .first()
    )

    MemoryMan = (
        Player.objects.annotate(
            num_memo_actions=Count(
                "moves__actions", filter=Q(moves__actions__category="MEMO")
            )
        )
        .order_by("-num_memo_actions")
        .first()
    )

    # Принес больше всего денег КБ
    CommandLeader = (
        CommandPayments.objects.filter(category="DEPOSITE", move__player__visible=True)
        .values("move__player")
        .annotate(total_investments=Sum("count"))
        .order_by("-total_investments")
        .first()
    )
    if CommandLeader:
        player_id = CommandLeader["move__player"]
        CommandLeader = Player.objects.get(pk=player_id)
    else:
        CommandLeader = None

    # Нанес самый больший ущерб КБ
    EternalIntern = (
        CommandPayments.objects.filter(
            category="SURP", move__player__visible=True, count__lt=0
        )
        .values("move__player")
        .annotate(total_withdrawals=Sum(F("count") * -1))
        .order_by("-total_withdrawals")
        .first()
    )
    if EternalIntern:
        player_id = EternalIntern["move__player"]
        EternalIntern = Player.objects.get(pk=player_id)
    else:
        EternalIntern = None

    # Больше всего раз выводил деньги из КБ
    ShipRunner = (
        CommandPayments.objects.filter(
            category="WITHDRAW", move__player__visible=True, count__lt=0
        )
        .values("move__player")
        .annotate(total_withdrawals=Sum(F("count") * -1))
        .order_by("-total_withdrawals")
        .first()
    )
    if ShipRunner:
        player_id = ShipRunner["move__player"]
        ShipRunner = Player.objects.get(pk=player_id)
    else:
        ShipRunner = None

    # Больше всего раз получил дефолт
    DefoultMan = (
        Player.objects.annotate(
            num_defoult_actions=Count(
                "moves__actions", filter=Q(moves__actions__category="DEF_BIS")
            )
        )
        .order_by("-num_defoult_actions")
        .first()
    )

    # Заработал больше всего денег на бизнесе
    BornBusinessman = (
        Player.objects.filter(visible=True)
        .annotate(
            total_bsns_in_surp=Sum(
                "moves__actions__count",
                filter=Q(moves__actions__count__gt=0, moves__actions__category="BSNS"),
            )
        )
        .order_by("-total_bsns_in_surp")
        .first()
    )

    # Самый убыточные бизнесы
    BadLuckBusinessman = (
        Player.objects.filter(visible=True)
        .annotate(
            total_bsns_in_surp=Sum(
                "moves__actions__count",
                filter=Q(moves__actions__count__lt=0, moves__actions__category="BSNS"),
            )
        )
        .order_by("-total_bsns_in_surp")
        .last()
    )

    # Больше всего инфляций
    InflationCaller = (
        Player.objects.filter(visible=True)
        .annotate(
            num_infl_actions=Count(
                "moves__actions", filter=Q(moves__actions__category="INFL")
            )
        )
        .order_by("-num_infl_actions")
        .first()
    )

    # Больше всего проданных и купленных бизнесов
    MarketTrader = (
        Player.objects.filter(visible=True)
        .annotate(
            num_buy_actions=Count(
                "moves__actions", filter=Q(moves__actions__category="BUY_BIS")
            ),
            num_sell_actions=Count(
                "moves__actions", filter=Q(moves__actions__category="SELL_BIS")
            ),
        )
        .order_by("-num_buy_actions", "-num_sell_actions")
        .first()
    )

    # Больше всего заработал на сюрпризах
    LuckyMan = (
        Player.objects.filter(visible=True)
        .annotate(
            total_earnings_in_surp=Sum(
                "moves__actions__count",
                filter=Q(moves__actions__count__gt=0, moves__actions__category="SURP"),
            )
        )
        .order_by("-total_earnings_in_surp")
        .first()
    )

    # Потерял на сюрпризах больше всех
    UnLuckyMan = (
        Player.objects.filter(visible=True)
        .annotate(
            total_losses_in_surp=Sum(
                "moves__actions__count",
                filter=Q(moves__actions__count__lt=0, moves__actions__category="SURP"),
            )
        )
        .order_by("-total_losses_in_surp")
        .last()
    )

    # Заработал больше всего денег
    WarrenBaffet = (
        Player.objects.filter(visible=True)
        .annotate(
            total_earnings=Sum(
                "moves__actions__count", filter=Q(moves__actions__count__gt=0)
            )
        )
        .order_by("-total_earnings")
        .first()
    )

    # Самое большое кол-во Action
    ActiveBro = (
        Player.objects.filter(visible=True)
        .annotate(num_actions=Count("moves__actions"))
        .order_by("-num_actions")
        .first()
    )

    # Empty achievements list
    Achievements = {}
    for player in players:
        achievements_list = []

        if player == SurpriseMan:
            achievements_list.append(
                Achievement(
                    title="Человек Сюрприз 🎁",
                    text="Больше всех нажал на кнопку Сюрприз",
                )
            )

        if player == CommandSurpriseMan:
            achievements_list.append(
                Achievement(
                    title="Командный сюрприз 🎁",
                    text="Получил больше всего сюрпризов для КБ",
                )
            )

        if player == MemoryMan:
            achievements_list.append(
                Achievement(
                    title="Сверхмозг 🧠", 
                    text="Получил больше всего карточек мемори"
                )
            )

        if player == CommandLeader:
            achievements_list.append(
                Achievement(
                    title="Командный лидер 🦾", 
                    text="Принес больше всего денег КБ"
                )
            )

        if player == EternalIntern:
            achievements_list.append(
                Achievement(
                    title="Вечный стажер 👨🏼",
                    text="Самые убыточные сюрпризы для КБ"
                )
            )

        if player == ShipRunner:
            achievements_list.append(
                Achievement(
                    title="Бегущий с корабля 🏃🏽‍♂️",
                    text="Вывел из КБ больше всего денег",
                )
            )

        if player == DefoultMan:
            achievements_list.append(
                Achievement(
                    title="ДефолтМэн 🙈",
                    text="Найбольшее кол-во дефолтов"
                )
            )

        if player == BornBusinessman:
            achievements_list.append(
                Achievement(
                    title="Прирожденный бизнесмен 💵",
                    text="Заработал на бизнесе больше всех",
                )
            )

        if player == BadLuckBusinessman:
            achievements_list.append(
                Achievement(
                    title="НеБизнесмен 🪫",
                    text="Потерял на бизнесе больше всех"
                )
            )

        if player == InflationCaller:
            achievements_list.append(
                Achievement(
                    title="Призыватель инфляций 📈📉",
                    text="Инфляция настигает вас постоянно",
                )
            )

        if player == MarketTrader:
            achievements_list.append(
                Achievement(
                    title="Как на рынке 🛒",
                    text="Продал больше всех бизнесов"
                )
            )

        if player == LuckyMan:
            achievements_list.append(
                Achievement(
                    title="Человек удачи 🪬",
                    text="Больше всего заработал на сюрпризах"
                )
            )

        if player == UnLuckyMan:
            achievements_list.append(
                Achievement(
                    title="Человек НЕудачи 🪆",
                    text="Потерял на сюрпризах больше всех "
                )
            )

        if player == WarrenBaffet:
            achievements_list.append(
                Achievement(
                    title="Warren Baffet ⭐️", 
                    text="Заработал больше всех денег"
                )
            )

        if player == ActiveBro:
            achievements_list.append(
                Achievement(
                    title="Актив Бро 🧗🏼‍♂️",
                    text="Сделал больше всех действий"
                )
            )

        # Achieve for everyone who havent
        if len(achievements_list) == 0:
            achievements_list.append(
                Achievement(title="Играл ✅", text="За хорошую игру!")
            )

        Achievements[player] = achievements_list

    return Achievements
