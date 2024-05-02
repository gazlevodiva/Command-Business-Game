from game.models.BusinessPayments import BusinessPayments
from game.models.CommandPayments import CommandPayments
from game.models.GameSessions import GameSessions
from game.models.Actions import Actions
from game.models.Player import Player
from game.models.Moves import Moves

from game.methods.BusinessMethods import getVotion
from game.methods.BusinessMethods import getCommandPlayers

from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import playerTurn
from game.methods.PlayerMethods import getBusinesses

from collections import defaultdict
from django.db.models import Sum
import re


def get_dashboard_actions(session: GameSessions) -> list:
    game_session_actions = (
        Actions.objects
        .filter(move__player__game_session=session)
        .filter(is_public=True)
        .select_related('move', 'move__player')
        .order_by("-move__number", "-created_date")
    )

    # Create sorted dict like {move : [actions...], ...}
    moves_actions = defaultdict(list)
    for action in game_session_actions:
        moves_actions[action.move.number].append(action)

    # Generate total list of dashboard actions
    game_actions = []
    for move_number, actions in moves_actions.items():
        visible_actions = [ac for ac in actions if ac.visible]

        print(move_number, actions)

        # Try to fing and get New Level action
        new_level_action = next(
            (ac for ac in actions if ac.category == "NLWL"),
            None
        )
        if new_level_action:
            total_count = sum([ac.count for ac in actions])
            action_name = new_level_action.name

            # Try to fing and get Inflation action in new level
            inflation_action = next(
                (ac for ac in actions if ac.category == "INFL"),
                None
            )
            if inflation_action:
                action_name = f"{new_level_action.name}. {inflation_action.name}"

            game_actions.append({
                "move_id": new_level_action.move.id,
                "move_number": new_level_action.move.number,
                "move_stage": new_level_action.move_stage,
                "move_position": new_level_action.move.position,
                "player_name": new_level_action.move.player.name,
                "action_id": new_level_action.id,
                "action_name": action_name,
                "action_count": total_count,
                "action_visible": new_level_action.visible,
                "action_category": new_level_action.category,
                "action_is_command": new_level_action.is_command,
            })

            # Try to fing and get Command Business action in new level
            command_business_action = next(
                (ac for ac in actions if ac.category == "BSNS" and ac.is_command),
                None
            )
            if command_business_action:
                print('-----', move_number, '-----', command_business_action)

                payment_actions = (
                    [ac for ac in actions if ac.is_command and ac.move.player.name != 'X']
                )

                print(payment_actions)

                print('-------------------------------')

        # Try to fing and get Command Surprise action
        command_surprise_action = next(
            (ac for ac in actions if ac.category == "SURP" and ac.is_command),
            None
        )
        if command_surprise_action:
            count = CommandPayments.objects.get(
                move=command_surprise_action.move
            ).count

        if not new_level_action and not command_surprise_action:
            for action in visible_actions:
                game_actions.append({
                    "move_id": action.move.id,
                    "move_number": action.move.number,
                    "move_stage": action.move_stage,
                    "move_position": action.move.position,
                    "player_name": action.move.player.name,
                    "action_id": action.id,
                    "action_name": action.name,
                    "action_count": action.count,
                    "action_visible": action.visible,
                    "action_category": action.category,
                    "action_is_command": action.is_command,
                })

    # Check results
    for x in game_actions:
        print(x['move_number'], x['player_name'], x['action_name'], x['action_count'])

    # ////////////////////////////////////

    new_level_actions_cache = {}
    business_payments_cache = {}

    game_actions = []
    for action in game_session_actions:
        count = action.count

        # New level - just total count
        if action.category == "NLWL":
            key = (action.move.number, action.move.player.id)

            if key not in new_level_actions_cache:
                total_count = (
                    Actions.objects.filter(
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

        # Command Surprise
        if action.category == "SURP" and action.is_command:
            command_payment = CommandPayments.objects.get(move=action.move)
            count = command_payment.count

        # Command Business income
        if action.category == "BSNS" and action.is_command:
            percent_pattern = r"(-?\d+)%"
            match = re.search(percent_pattern, action.name)

            if match:
                percent = int(match.group(1))
                key = (action.move.number, percent)

                if key not in business_payments_cache:
                    business_payment_query = (
                        BusinessPayments.objects
                        .filter(move__player=action.move.player)
                        .filter(
                            move__number=action.move.number,
                            rentability=percent
                        )
                    )
                    count = (
                        business_payment_query.first().count
                        if business_payment_query.exists() else 0
                    )
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
                    "id": business.id,
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
                    "id": command_business.id,
                    "name": command_business.business.name,
                    "cost": command_business.business.cost,
                    "status": command_business.latest_status
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
