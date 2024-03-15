from game.models.Player import Player
from game.models.GameSessions import GameSessions
from game.views.error import error_404
from game.views.player_panel.authorise import authorise
from django.shortcuts import get_object_or_404
import re


def check_user_session_hash(view):
    def wrapped(request, *args, **kwargs):
        try:
            session_hash = request.COOKIES["game_session_hash"]
            session = GameSessions.objects.get(session_hash=session_hash)
            if not session:
                print("check_user_session_hash: No session in DB. Return 404")
                return error_404(request)

        except Exception as e:
            print("check_user_session_hash: No session_hash. Check url", e)

            player_control_pattern = r'^/player_control_(\d+)/$'
            match = re.match(player_control_pattern, request.path)

            if not match:
                print("check_user_session_hash: No session_hash and no player. Return 404")
                return error_404(request)

            if match:
                print("check_user_session_hash: MATCH")
                player_id = int(match.group(1))
                player = get_object_or_404(Player, pk=player_id)
                session_hash = player.game_session.session_hash

                # Need to ask session code here!!!
                return authorise(request, *args, **kwargs)

            return error_404(request)

        return view(request, session, *args, **kwargs)

    return wrapped
