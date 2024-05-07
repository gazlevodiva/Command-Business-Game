from game.models.BusinessPayments import BusinessPayments
from game.models.CommandPayments import CommandPayments
from game.models.GameSessions import GameSessions
from game.models.Actions import Actions
from game.models.Player import Player
from game.models.Moves import Moves

from game.methods.BusinessMethods import getVotion
from game.methods.BusinessMethods import getCommandPlayers
from game.methods.BusinessMethods import get_business_payment_by_action

from game.methods.PlayerMethods import getBalance
from game.methods.PlayerMethods import playerTurn
from game.methods.PlayerMethods import getBusinesses

from collections import defaultdict
from django.db.models import Sum


def get_dashboard_actions(session: GameSessions) -> list:
    game_session_actions = (
        Actions.objects
        .filter(move__player__game_session=session)
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

        # for vis_ac in visible_actions:
        #     print(move_number, vis_ac)

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

            quiz_action = next(
                (ac for ac in actions if ac.category == "QUIZ"),
                None
            )
            if quiz_action:
                game_actions.append({
                    "move_id": quiz_action.move.id,
                    "move_number": quiz_action.move.number,
                    "move_stage": quiz_action.move_stage,
                    "move_position": quiz_action.move.position,
                    "player_name": quiz_action.move.player.name,
                    "action_id": quiz_action.id,
                    "action_name": quiz_action.name,
                    "action_count": quiz_action.count,
                    "action_visible": quiz_action.visible,
                    "action_category": quiz_action.category,
                    "action_is_command": quiz_action.is_command,
                })

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
                count = get_business_payment_by_action(command_business_action)

                game_actions.append({
                    "move_id": command_business_action.move.id,
                    "move_number": command_business_action.move.number,
                    "move_stage": command_business_action.move_stage,
                    "move_position": command_business_action.move.position,
                    "player_name": command_business_action.move.player.name,
                    "action_id": command_business_action.id,
                    "action_name": command_business_action.name,
                    "action_count": count,
                    "action_visible": command_business_action.visible,
                    "action_category": command_business_action.category,
                    "action_is_command": command_business_action.is_command,
                })

        # Try to fing and get Command Surprise action
        command_surprise_action = next(
            (ac for ac in actions if ac.category == "SURP" and ac.is_command),
            None
        )
        if command_surprise_action:
            count = CommandPayments.objects.get(
                move=command_surprise_action.move
            ).count

            game_actions.append({
                "move_id": command_surprise_action.move.id,
                "move_number": command_surprise_action.move.number,
                "move_stage": command_surprise_action.move_stage,
                "move_position": command_surprise_action.move.position,
                "player_name": command_surprise_action.move.player.name,
                "action_id": command_surprise_action.id,
                "action_name": command_surprise_action.name,
                "action_count": count,
                "action_visible": command_surprise_action.visible,
                "action_category": command_surprise_action.category,
                "action_is_command": command_surprise_action.is_command,
            })

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
        print(
            x['move_number'],
            x['player_name'],
            x['action_name'],
            x['action_count']
        )


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
