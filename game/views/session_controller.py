from django.shortcuts import render
from game.decorators import check_user_session_hash

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Surprises import Surprises
from game.models.PlayersBusinessStatus import PlayersBusinessStatus

import io
import base64
import qrcode
from django.http import JsonResponse
import pandas as pd
from django.shortcuts import get_object_or_404


@check_user_session_hash
def session_players(request, session):
    players = Player.objects.filter(game_session=session, visible=True)
    players_json = [
        {
            "id": player.id,
            "name": player.name,
            "icon": player.icon,
            "deletable": (
                Actions.objects
                .filter(move__player=player)
                .filter(is_command=True)
                .exists()
            )
        }
        for player in players
    ]
    response = JsonResponse({"players": players_json})
    return response


@check_user_session_hash
def session_panel(request=None, session=None):
    players = Player.objects.filter(visible=True, game_session=session)

    qr_text = f"http://{request.get_host()}/s/{session.session_hash}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_text)
    qr.make(fit=True)

    qr_code_image = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    qr_code_image.save(buffer, "PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    context = {
        "players": players,
        "session": session,
        "qr_code_base64": qr_code_base64,
    }

    if request is None:
        return {"players": players}

    return render(
        request,
        "game/session_control/session_admin_panel.html",
        context
    )


@check_user_session_hash
def reset_game(request, session):
    players = Player.objects.filter(game_session=session, visible=True)

    try:
        # need to delete all Xplayer Movex except first
        player_X = Player.objects.get(game_session=session, name="X")
        player_X_moves = (
            Moves.objects
            .filter(player=player_X)
            .exclude(number=0)
        )

        # Delete information
        player_X_moves.delete()
        players.delete()
        describe = "Все игроки, а также их ходы и действия удалены."

    except Exception as e:
        return JsonResponse(
            {
                "result": False,
                "describe": "Ошибка при удалении",
                "error": str(e)
            }
        )

    response = JsonResponse({"result": True, "describe": describe})
    return response


@check_user_session_hash
def delete_player(request, session, player_id):
    try:
        player = get_object_or_404(Player, id=player_id)
        player.delete()
        describe = "Игрок успешно удален."
    except Exception as e:
        describe = "error"
        return JsonResponse(
            {"result": False, "describe": describe, "error": str(e)}
        )

    return JsonResponse({"result": True, "describe": describe})


@check_user_session_hash
def memory_setup(request, session):
    if request.method == "POST":
        # Delete old memories
        Surprises.objects.filter(category="MEMO", session_id=session.id).delete()

        for key, value in request.POST.items():
            if "memory" in key:
                new_memory = Surprises.objects.create(
                    name=value, category="MEMO", session_id=session.id
                )

    memories = Surprises.objects.filter(category="MEMO", session_id=session.id)
    if not memories:
        memories = Surprises.objects.filter(category="MEMO", session_id=0)

    context = {"memories": memories}
    return render(request, "game/session_control/session_admin_memory.html", context)


@check_user_session_hash
def upload_memory_file(request, session):
    if request.method == "POST" and request.FILES:
        file = request.FILES.get("file")
        if file:
            try:
                df = pd.read_excel(file)

                if len(df.columns) == 1:
                    memories_list = df.values.tolist()
                    return JsonResponse({"memories": memories_list})
                else:
                    return JsonResponse(
                        {"error": "Неверная структура файла"}, status=400
                    )
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Ошибка при загрузке файла"}, status=400)
