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
    # PLayers list
    players = Player.objects.filter(visible=True, game_session=session)

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

        profit = int((balance + command_cost + business_cost) * 100 / 60000)

        players_info.append(
            {
                "player": player,
                "profit": profit,
                "achievements": achievements[player][:5],
                "memory_answers": memory_answers,
            }
        )

    context = {"players_info": players_info}
    return render(request, "game/finish.html", context)
