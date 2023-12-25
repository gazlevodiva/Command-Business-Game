from django.shortcuts import render

from game.models.Business import Business
from game.decorators import check_user_session_hash


@check_user_session_hash
def rules(request, session):
    businesses = Business.objects.all()
    return render(request, "game/rules.html", {"businesses": businesses})
