from django.shortcuts import render

from game.models.BusinessPayments import BusinessPayments
from game.models.CommandPayments import CommandPayments
from game.models.Actions import Actions
from game.models.Player import Player
from game.models.Moves import Moves

from game.methods.BusinessMethods import getVotion
from game.methods.BusinessMethods import getCommandPlayers
from game.methods.BusinessMethods import getCommandBank

from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import playerTurn
from game.methods.PlayerMethods import getActionsDashboard
from game.methods.PlayerMethods import getBusinesses
from game.methods.PlayerMethods import getCommandBusinesses

from game.decorators import check_user_session_hash
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.http import JsonResponse
import re

@login_required(login_url="/login/")
@check_user_session_hash
def dashboard_online(request, session):
    context = {
        "players": [],
    }

    # Add session information
    context["session_name"] = session.session_name
    context["session_hash"] = session.session_hash
    context["session_code"] = session.session_code

    # Get actions for History
    context["game_actions"] = []
    for action in getActionsDashboard(session)[:30]:
        count = action.count

        # If new level, count total payments
        if action.category == "NLWL":
            count = (
                Actions.objects
                .filter(move__number=action.move.number)
                .filter(move__player=action.move.player)
                .filter(visible=True)
                .filter(is_personal=True)
                .aggregate(total_count=Sum('count'))
            )['total_count'] or 0

        # If command surpise get count info from CommandPayments
        if action.category == "SURP" and action.is_command:
            command_payment = CommandPayments.objects.get(move=action.move)
            count = command_payment.count

        # If command business payments
        if action.category == "BSNS" and action.is_command:
            percent_pattern = r"(-?\d+)%"
            match = re.search(percent_pattern, action.name)
            if match:
                percent = int(match.group(1))

                players_actions_by_move_number = (
                    Actions.objects
                    .filter(move_player_game_session=session)
                    .filter(move__number=action.move.number)
                )
                players_move_number_new_level = (
                    players_actions_by_move_number
                    .get(category="NLWL")
                    .move
                )
                business_payment = (
                    BusinessPayments.objects
                    .filter(move=players_move_number_new_level)
                )
                try:
                    count = business_payment.get(rentability=percent).count
                except:
                    count = 0

        context["game_actions"].append(
            {
                "move_id": action.move.id,
                "move_number": action.move.number,
                "move_stage": action.move_stage,
                "move_position": action.move.position,
                "player_name": action.move.player.name,
                "action_id": action.id,
                "action_name": action.name,
                "action_count": count,
                "action_visible": action.visible,
                "action_category": action.category,
                "action_is_command": action.is_command,
            }
        )

    # Get active votion
    move = Moves.objects.filter(player__game_session=session).last()
    context["votion"] = getVotion(move)

    # Total command balance
    context["command_bank"] = getCommandBank(session)

    # Take all players from session
    players = (
        Player.objects
        .filter(game_session=session)
        .filter(visible=True)
    )

    player_turn_id = playerTurn(session)
    for player in players:
        player_info = {}  # lets add some info about

        player_info["id"] = player.id
        player_info["name"] = str(player.name)
        player_info["icon"] = str(player.icon)
        player_info["level"] = player.level

        player_info["balance"] = getBalance(player)
        player_info["businesses"] = []
        for business in getBusinesses(player).filter(is_command=False):

            player_info["businesses"].append(
                {
                    "name": str(business.business.name),
                    "cost": business.business.cost,
                }
            )

        player_info["current_position"] = (
            Moves.objects
            .filter(player=player)
            .last()
            .position
        )
        player_info["past_position"] = 0

        if player_turn_id == player.id:
            player_info["is_turn"] = True

        if player_turn_id != player.id:
            player_info["is_turn"] = False

        context["players"].append(player_info)

    # Command player info
    context["command_players"] = []

    for command_player in getCommandPlayers(session):

        command_businesses_info = []
        command_player_businesses = (
            getBusinesses(command_player["move__player"])
            .filter(is_command=True)
        )
        for command_business in command_player_businesses:
            command_businesses_info.append(
                {
                    "name": command_business.business.name,
                    "cost": command_business.business.cost,
                }
            )

        context["command_players"].append(
            {
                "name": command_player["move__player"].name,
                "share": command_player["share"],
                "count": command_player["count"],
                "businesses": command_businesses_info,
            }
        )

    return JsonResponse(context)


@login_required(login_url="/login/")
@check_user_session_hash
def dashboard(request=None, session=None):
    players = Player.objects.filter(visible=True, game_session=session)

    # whos player Turn???
    player_turn = playerTurn(session)

    # Info about players business
    players_info = []
    for player in players:
        businesses = getBusinesses(player)
        balance = getBalance(player)

        if player == player_turn:
            is_turn = True

        if player != player_turn:
            is_turn = False

        # get last field position
        position = Moves.objects.filter(player=player).last().position

        players_info.append(
            {
                "player": player,
                "balance": balance,
                "position": position,
                "businesses": businesses,
                "is_turn": is_turn,
            }
        )

    # Command player info
    command_players = getCommandPlayers(session)

    # Info about command businesses
    command_player_info = []
    for command_player in command_players:
        player = command_player["move__player"]
        command_businesses = getCommandBusinesses(player)
        command_player_info.append(
            {
                "command_player": command_player,
                "command_businesses": command_businesses,
            }
        )

    # Game actions
    actions = getActionsDashboard(session)

    # Total command balance
    bank = getCommandBank(session)

    context = {
        "players": players_info,
        "command_players": command_player_info,
        "command_bank": bank,
        "actions": actions[:15],
        "session": session,
    }

    if request is None:
        return context

    # ONLINE
    if session.online:
        return render(request, "game/dashboard_online.html", context)

    # LOCAL
    if not session.online:
        return render(request, "game/dashboard.html", context)
