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

def getAchievements( players ):

    # Нажал на кнопку “Сюрприз” больше других игроков
    SurpriseMan = (
        Player.objects
        .filter(
            visible = True
        )
        .annotate(
            num_surprise_actions = Count( 
                'actions__category', 
                filter = Q( actions__category='SURP' ) )
        )
        .order_by( '-num_surprise_actions' )
        .first()
    )

    # Нажал на кнопку “Сюрприз для КБ” больше других игроков
    CommandSurpriseMan = (
        Player.objects
        .filter(
            visible = True
        )
        .annotate(
            num_surprise_actions = Count( 
                'actions__category', 
                filter = Q( 
                    actions__category   = 'SURP', 
                    actions__is_command = True 
                ) 
            )
        )
        .order_by( '-num_surprise_actions' )
        .first()
    )

    # Принес больше всего денег КБ
    CommandLeader = (
        Player.objects
        .filter( 
            visible = True
        )
        .annotate(
            total_commandpayments = Sum('commandpayments__count'),
        )
        .order_by('-total_commandpayments')
        .first()
    )

    # Нанес самый больший ущерб КБ
    EternalIntern = (
        Player.objects
        .filter( 
            visible = True 
        )
        .annotate(
            total_commandpayments = Sum(
                'commandpayments__count', 
                filter = Q( commandpayments__lt=0 ) 
            ),            
        )
        .order_by('-total_commandpayments')
        .first()
    )

    # Вложил больше всего денег в КБ
    CommandSource = (
        Player.objects
        .filter( 
            visible = True
        )
        .annotate(
            max_command_payments = Max('commandpayments__count')
        )
        .order_by('-max_command_payments')
        .first()
    )

    # Больше всего раз выводил деньги из КБ
    ShipRunner = (
        Player.objects
        .filter(
            visible = True,
            commandpayments__count__lt = 0
        )
        .annotate(
            sum_count = Max( F('commandpayments__count') )
        )
        .order_by('-sum_count')
        .first()
    )

    # Больше всего раз получил дефолт
    DefoultMan = (
        Player.objects
        .filter( 
            visible = True 
        )
        .annotate(
            defoult_count = Count(
                'playersbusiness', 
                filter = Q(playersbusiness__status='DEFOULT')
            )
        )
        .filter(
            defoult_count__gt = 0
        )
        .order_by('-defoult_count')
        .first()
    )

    # Заработал больше всего денег на бизнесе
    BornBusinessman = (
        Player.objects
        .filter(
            visible = True            
        )
        .annotate(
            earnings = Sum('playersbusiness__businesspayments__count')
        )
        .first()
    )

    # Самый убыточные бизнесы
    BadLuckBusinessman = (
        Player.objects
        .filter(
            visible = True,
            playersbusiness__businesspayments__count__lt = 0
        )
        .annotate(
            earnings = Sum('playersbusiness__businesspayments__count')
        )
        .first()
    )

    # Больше всего инфляций
    InflationCaller = (
        Player.objects
        .filter( 
            visible = True 
        )
        .annotate(
            inflation_count = Count(
                'actions', 
                filter = Q(actions__category='INFL')
            )
        )
        .filter(
            inflation_count__gt = 0
        )
        .order_by('-inflation_count')
        .first()
    )

    # Больше всего проданных и купленных бизнесов
    MarketTrader = (
        Player.objects
        .filter(
            visible = True
        )
        .annotate(
            sold_count = Count(
                'playersbusiness', 
                filter = Q(playersbusiness__status='SOLD')
            )
        )
        .order_by('-sold_count')
        .first()

    )

    # Больше всего заработал на сюрпризах
    LuckyMan = (
        Player.objects
        .filter( 
            visible = True 
        )
        .annotate( 
            surprise_count = Sum(
                'actions__count', 
                filter = Q(actions__category='SURP')
            )
        )
        .filter(
            surprise_count__gt = 0
        )
        .order_by('-surprise_count')
        .first()
    )

    # Потерял на сюрпризах больше всех 
    UnLuckyMan = (
        Player.objects
        .filter( 
            visible = True 
        )
        .annotate( 
            surprise_count = Sum(
                'actions__count', 
                filter = Q( actions__category = 'SURP' )
            )
        )
        .filter(
            surprise_count__lt = 0
        )
        .order_by('-surprise_count')
        .first()
    )

    # Заработал больше всего денег
    WarrenBaffet = (
        Player.objects
        .filter( 
            visible = True 
        )
        .annotate( 
            count_sum = Sum('actions__count') + Sum('playersbusiness__businesspayments__count')
        )
        .filter(
            count_sum__gt = 0
        )
        .order_by('-count_sum')
        .first()
    )

    # Самое большое кол-во Action
    ActiveBro = (
        Player.objects
        .filter( 
            visible = True
        )
        .annotate( 
            actions_count = Count('actions')
        )
        .filter(
            actions_count__gt = 0
        )
        .order_by('-actions_count')
        .first()
    )


    

    # Empty achievements list
    Achievements = {}
    for player in players:

        achievements_list = []

        if player == SurpriseMan:
            achievements_list.append(
                Achievement( 
                    title = "Человек Сюрприз 🎁",
                    text  = "Больше всех нажал на кнопку Сюрприз"
                )
            )   

        if player == CommandSurpriseMan:
            achievements_list.append(
                Achievement( 
                    title = "Командный сюрприз 🎁",
                    text  = "Получил больше всего сюрпризов для КБ"
                )
            )
            
        if player == CommandLeader:
            achievements_list.append(
                Achievement( 
                    title = "Командный лидер 🦾",
                    text  = "Принес больше всего денег КБ"
                )
            )

        if player == EternalIntern:
            achievements_list.append(
                Achievement( 
                    title = "Вечный стажер 👨🏼‍🎓",
                    text  = "Нанес больше всего убытков для КБ"
                )
            )

        if player == CommandSource:
            achievements_list.append(
                Achievement( 
                    title = "Командный источник 🤴🏻",
                    text  = "Вложил больше всех в КБ"
                )
            )

        if player == ShipRunner:
            achievements_list.append(
                Achievement( 
                    title = "Бегущий с корабля 🏃🏽‍♂️",
                    text  = "Вывел из командного бизнеса больше всего денег"
                )
            )
        
        if player == DefoultMan:
            achievements_list.append(
                Achievement( 
                    title = "ДефолтМэн 🙈",
                    text  = "Найбольшее кол-во дефолтов"
                )
            )

        if player == BornBusinessman:
            achievements_list.append(
                Achievement( 
                    title = "Прирожденный бизнесмен 💵",
                    text  = "Заработал на бизнесе больше всех"
                )
            )

        if player == BadLuckBusinessman:
            achievements_list.append(
                Achievement( 
                    title = "НеБизнесмен 🪫",
                    text  = "Потерял на бизнесе больше всех"
                )
            )

        if player == InflationCaller:
            achievements_list.append(
                Achievement( 
                    title = "Призыватель инфляций 📈📉",
                    text  = "Инфляция настигает вас постоянно"
                )
            )

        if player == MarketTrader:
            achievements_list.append(
                Achievement( 
                    title = "Как на рынке 🛒",
                    text  = "Продал больше всех бизнесов"
                )
            )

        if player == LuckyMan:
            achievements_list.append(
                Achievement( 
                    title = "Человек удачи 🪬",
                    text  = "Больше всего заработал на сюрпризах"
                )
            )

        if player == UnLuckyMan:
            achievements_list.append(
                Achievement( 
                    title = "Человек НЕудачи 🪆",
                    text  = "Потерял на сюрпризах больше всех "
                )
            )

        if player == WarrenBaffet:
            achievements_list.append(
                Achievement( 
                    title = "Warren Baffet ⭐️",
                    text  = "Заработал больше всех денег"
                )
            )

        if player == ActiveBro:
            achievements_list.append(
                Achievement( 
                    title = "Актив Бро 🧗🏼‍♂️",
                    text  = "Сделал больше всех действий"
                )
            )


        Achievements[player] = achievements_list

    return Achievements
