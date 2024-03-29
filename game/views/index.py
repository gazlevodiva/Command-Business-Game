from django.shortcuts import redirect

from django.http import HttpResponseRedirect

from game.models.Player import Player
from game.models.GameSessions import GameSessions


def index(request, session_hash=False):
    try:
        session = GameSessions.objects.get(session_hash=session_hash)
    except GameSessions.DoesNotExist:
        session = None

    if session:
        try:
            session_controller = request.COOKIES["game_session_controller"]
            player = Player.objects.get(pk=session_controller)
        except Exception as e:
            print(e)
            player = None

        if player is not None:
            return redirect(f"/player_control_{session_controller}/")

        render_template = HttpResponseRedirect("/new_player/")
        render_template.set_cookie(
            "game_session_hash",
            session_hash,
            max_age=604800
        )
        return render_template

    return HttpResponseRedirect("/login/")
