from django.shortcuts import render, redirect
from game.decorators import check_user_session_hash

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.models.PlayersBusiness import PlayersBusiness
from game.models.PlayersBusinessStatus import PlayersBusinessStatus

import io
import base64
import qrcode
from django.http import JsonResponse

@check_user_session_hash
def session_panel( request=None, session=None ):
    
    players = Player.objects.filter( visible=True, game_session=session )

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
    qr_code_image.save(buffer, 'PNG')
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    context = {
        "players": players,
        "session": session,
        'qr_code_base64': qr_code_base64,
    }

    if request is None:
        return { "players": players }
    
    return render(request, 'game/session_control/session_admin_panel.html', context) 


@check_user_session_hash
def reset_last_move( request, session ):

    # Get last move in game session
    last_move = Moves.objects.filter(player__game_session=session).last()

    last_actions = Actions.objects.filter(move=last_move)

    for action in last_actions:

        if action.category == 'NLWL':
            action.move.player.level -= 1
            action.move.player.save()

        # Check all changes player_business status in move
        related_statuses = PlayersBusinessStatus.objects.filter(move=action.move)

        for players_business_status in related_statuses:
            if players_business_status == "ACTIVE":
                players_business_status.players_business.delete()


    if last_move.number != 0 :
        last_move.delete()

    response = JsonResponse( {"res":'Try to delete...'} )
    return response

@check_user_session_hash
def delete_player( request, session, player_id ):
    player = Player.objects.get(id=player_id)
    player.delete()
    return redirect(request.META.get('HTTP_REFERER', ''))
