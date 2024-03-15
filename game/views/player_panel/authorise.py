from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from game.models.Player import Player


def authorise(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    session = player.game_session

    if request.method == "POST":
        if "session_game_code" in request.POST:

            form_code = request.POST["session_game_code"]
            print(form_code, session.session_code)

            if int(form_code) == int(session.session_code):
                request_template = redirect(f"/player_control_{player.id}/")
                request_template.set_cookie(
                    "game_session_controller",
                    player.id,
                    max_age=604800
                )
                request_template.set_cookie(
                    "game_session_hash",
                    session.session_hash,
                    max_age=604800
                )

                print('Куки вписаны!!!!')

                return request_template

    context = {
        "session": session,
        "player": player,
    }
    return render(request, "game/player_authorise.html", context)
