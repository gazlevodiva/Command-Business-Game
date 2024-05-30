from game.methods.dashboard_methods import get_players_data
from game.methods.dashboard_methods import get_dashboard_actions
from game.methods.dashboard_methods import get_command_players_data
from game.methods.dashboard_methods import get_command_business_bank
from game.methods.dashboard_methods import get_votion_from_last_move

from game.decorators import check_user_session_hash
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.shortcuts import render


@login_required(login_url="/login/")
@check_user_session_hash
def dashboard_online(request, session):
    # Set context
    context = {}

    # Add session information
    context["session_name"] = session.session_name
    context["session_hash"] = session.session_hash
    context["session_code"] = session.session_code

    context["votion"] = get_votion_from_last_move(session)
    context["players"] = get_players_data(session)
    context['game_actions'] = get_dashboard_actions(session)[:15]
    context["command_bank"] = get_command_business_bank(session)
    context["command_players"] = get_command_players_data(session)

    return JsonResponse(context)


@login_required(login_url="/login/")
@check_user_session_hash
def dashboard(request, session):
    if session.online:
        context = {"session_code": str(session.session_code)}
        return render(request, "game/dashboard_online.html", context)

    if not session.online:
        return render(request, "game/dashboard.html")
