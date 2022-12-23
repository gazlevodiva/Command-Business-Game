from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect

from game.models.GameSessions import GameSessions

from game.views.page404 import error_404
from game.views.new_player import new_player


def index( request, session_hash=False ):

    last_game_session = GameSessions.objects.latest( 'created_date' )

    if last_game_session.session_hash == session_hash:
        render_template = render(request, 'game/session_code.html')        
        
        if request.POST:            
            session_code = int( request.POST['session_code'] )
            last_game_session = GameSessions.objects.latest( 'created_date' )

            if last_game_session.session_code == session_code:                
                render_template = HttpResponseRedirect( '/new_player/' )       
                render_template.set_cookie( 'game_session_hash', session_hash )
                return render_template
        
        return render_template

    return error_404( request )

