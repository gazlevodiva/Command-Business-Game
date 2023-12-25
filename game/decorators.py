from django.shortcuts import redirect
from django.http import Http404

from game.models.GameSessions import GameSessions
from game.views.error import error_404


def check_user_session_hash(view):
    def wrapped(request, *args, **kwargs):
        try:
            session_hash = request.COOKIES["game_session_hash"]
            session = GameSessions.objects.get(session_hash=session_hash)

            if not session:
                print("check_user_session_hash: No session_hash in DB. Return 404")
                return error_404(request)

        except:
            print("check_user_session_hash: No session_hash. Return 404")
            return error_404(request)

        return view(request, session, *args, **kwargs)

    return wrapped
