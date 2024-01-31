from django.shortcuts import render

from game.decorators import check_user_session_hash

from game.models.Player import Player

from game.methods.Achievements import getAchievements
from game.methods.BusinessMethods import getCommandShare
from game.methods.PlayerMethods import getBusinessesCost
from game.methods.PlayerMethods import getMemoryAnswers
from game.methods.PlayerMethods import getBalance


@check_user_session_hash
def finish(request, session):

    # Player x info
    # playerX = Player.objects.filter(game_session=session).get(name="X")
    # playerX_total = (
    #     CommandPayments.objects
    #     .filter(move__player=playerX)
    #     .aggregate(
    #         total=Sum('count')
    #     )
    # )['total']

    # if playerX_total is None:
    #     playerX_total = 0

    # PLayers list
    players = Player.objects.filter(game_session=session)

    # Get achievements for all players
    achievements = getAchievements(players)

    players_info = []
    for player in players:
        # Get total actives cost
        balance = getBalance(player)
        command_cost = getCommandShare(player)[1]
        business_cost = getBusinessesCost(player)
        memory_answers = getMemoryAnswers(player)

        if not business_cost:
            business_cost = 0

        if not command_cost:
            command_cost = 0

        profit = int(balance + command_cost + business_cost)
        profit_multiplier = round(profit/session.player_balance, 1)
        profit_level_avarage = round(profit/player.level)

        players_info.append(
            {
                "player": player,
                "profit": profit,
                "profit_multiplier": profit_multiplier,
                "profit_level_avarage": profit_level_avarage,
                "achievements": achievements[player][:5],
                "memory_answers": memory_answers,
            }
        )

    return render(request, "game/finish.html", {"players_info": players_info})
