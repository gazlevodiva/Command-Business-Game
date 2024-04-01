from django.shortcuts import render
from django.shortcuts import redirect

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions

from game.decorators import check_user_session_hash

import random
from game.views.error import error_404


def generate_unique_icon(game_session) -> str:
    used_emoji = (
        Player.objects
        .filter(game_session=game_session)
        .values_list("icon", flat=True)
    )
    emoji = ['⭐️', '🌚', '🌝', '🎃', '👾', '💎', '👽']
    available_icons = list(set(emoji) - set(used_emoji))

    if not available_icons:
        return ""

    return random.choice(available_icons)


@check_user_session_hash
def new_player(request, session):
    context = {}
    context['session_name'] = session.session_name
    context['session_description'] = session.description
    players_count = Player.objects.filter(game_session=session).count()

    # If more then 6 players - 404
    if players_count == 7:
        return error_404(request)

    if request.method == "POST":
        player_name = request.POST["new_player_name"]
        player_icon = generate_unique_icon(game_session=session)

        # Create new player
        new_player = Player.objects.create(
            name=player_name,
            icon=player_icon,
            game_session=session
        )

        # player start balance
        player_balance = session.player_balance

        # Make default connetion move
        move = Moves.objects.create(player=new_player, number=0)

        # Create connect action
        Actions.objects.create(
            move=move,
            move_stage="END",
            name="Начал игру",
            count=player_balance,
            category="GAMESTART",
            visible=True,
            is_public=True,
        )

        request_template = redirect(f"/player_control_{new_player.id}/")
        request_template.set_cookie(
            "game_session_controller", new_player.id, max_age=604800
        )

        return request_template

    return render(request, "game/new_player.html", context)
