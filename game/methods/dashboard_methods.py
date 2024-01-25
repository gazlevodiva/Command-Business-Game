from game.models.BusinessPayments import BusinessPayments
from game.models.CommandPayments import CommandPayments
from game.models.Actions import Actions
from game.models.Player import Player
from game.models.Moves import Moves

from game.methods.BusinessMethods import getVotion
from game.methods.BusinessMethods import getCommandPlayers

from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import playerTurn
from game.methods.PlayerMethods import getBusinesses

from django.db.models import Sum
import re


def get_dashboard_actions(session):
    game_session_actions = (
        Actions.objects
        .filter(move__player__game_session=session)
        .order_by("-created_date")
        .select_related('move', 'move__player')
    )

    new_level_actions_cache = {}
    business_payments_cache = {}

    game_actions = []
    for action in game_session_actions:
        count = action.count

        if action.category == "NLWL":
            key = (action.move.number, action.move.player.id)
            if key not in new_level_actions_cache:
                total_count = (
                    Actions.objects
                    .filter(
                        move__number=action.move.number,
                        move__player=action.move.player,
                        visible=True,
                        is_public=True,
                        is_personal=True
                    )
                    .aggregate(total_count=Sum('count'))['total_count'] or 0
                )
                new_level_actions_cache[key] = total_count
            count = new_level_actions_cache[key]

        elif action.category == "SURP" and action.is_command:
            command_payment = CommandPayments.objects.get(move=action.move)
            count = command_payment.count

        elif action.category == "BSNS" and action.is_command:
            percent_pattern = r"(-?\d+)%"
            match = re.search(percent_pattern, action.name)

            if match:
                percent = int(match.group(1))
                key = (action.move.number, percent)

                if key not in business_payments_cache:
                    business_payment_query = (
                        BusinessPayments.objects
                        .filter(
                            move__number=action.move.number,
                            rentability=percent
                        )
                    )
                    count = business_payment_query.first().count if business_payment_query.exists() else 0
                    business_payments_cache[key] = count

                count = business_payments_cache[key]

        game_actions.append({
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
        })

    return game_actions


def get_votion_from_last_move(session):
    return getVotion(
        Moves.objects
        .filter(player__game_session=session)
        .latest('created_date')
    )


def get_players_data(session):
    # Get players from session
    players = Player.objects.filter(visible=True, game_session=session)
    player_id_turn = playerTurn(session)

    players_info = []
    for player in players:
        player_info = {}
        player_info["id"] = player.id
        player_info["name"] = player.name
        player_info["icon"] = player.icon
        player_info["level"] = player.level
        player_info["balance"] = getBalance(player)
        player_info["is_turn"] = player_id_turn == player.id

        player_info["businesses"] = []
        for business in getBusinesses(player).filter(is_command=False):
            player_info["businesses"].append(
                {
                    "name": business.business.name,
                    "cost": business.business.cost,
                    "status": business.latest_status
                }
            )

        player_info["current_position"] = (
            Moves.objects
            .filter(player=player)
            .latest('created_date')
            .position
        )

        players_info.append(player_info)

    return players_info


def get_command_players_data(session):
    command_players_info = []
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

        command_players_info.append(
            {
                "name": command_player["move__player"].name,
                "share": command_player["share"],
                "count": command_player["count"],
                "businesses": command_businesses_info,
            }
        )

    return command_players_info


def get_command_business_bank(session):
    return (
        CommandPayments.objects
        .filter(
            move__player__game_session=session
        )
        .aggregate(Sum("count"))
    )["count__sum"]
