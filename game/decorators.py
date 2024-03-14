from game.models.Player import Player
from game.models.GameSessions import GameSessions
from game.views.error import error_404
from django.shortcuts import get_object_or_404
import re


def check_user_session_hash(view):
    def wrapped(request, *args, **kwargs):
        try:

            # Check is this player_control_ url
            # player_control_pattern = r'^/player_control_(\d+)/$'
            # match = re.match(player_control_pattern, request.path)
            # if match:
            #     player_id = int(match.group(1))
            #     player = get_object_or_404(Player, pk=player_id)
            #     if player:
            #         print(f"check_user_session_hash: {player.name} - {player.id}")

            session_hash = request.COOKIES["game_session_hash"]
            if not session_hash:
                print("check_user_session_hash: No session_hash. Return 404")
                return error_404(request)

            session = GameSessions.objects.get(session_hash=session_hash)
            if not session:
                print("check_user_session_hash: No session in DB. Return 404")
                return error_404(request)

        except Exception as e:
            print("check_user_session_hash: No session_hash. Return 404", e)
            return error_404(request)

        return view(request, session, *args, **kwargs)

    return wrapped
