from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
from game.models.GameSessions import GameSessions


def login(request):
    logout(request)

    if request.POST:
        username = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)

                try:
                    session = GameSessions.objects.get(
                        session_name=f"{username} game"
                    )
                except Exception as e:
                    print(e)
                    session = GameSessions.objects.create(
                        session_name=f"{username} game"
                    )

                render_template = HttpResponseRedirect("/game_settings/")
                render_template.set_cookie(
                    "game_session_hash",
                    session.session_hash
                )
                return render_template

    return render(request, "game/session_control/session_admin_login.html")
