from django.shortcuts import render, redirect

from game.models.GameSessions import GameSessions
from game.views.page404 import error_404



def index( request, session_hash=False ):

    last_game_session = GameSessions.objects.latest( 'created_date' )

    if last_game_session.session_hash == session_hash:
        render_template = render(request, 'game/session_code.html')        
        render_template.set_cookie( 'game_session_hash', session_hash )
        
        if request.POST:            
            session_code = int( request.POST['session_code'] )
            last_game_session = GameSessions.objects.latest( 'created_date' )

            if last_game_session.session_code == session_code:                
                return redirect( '/new_player/' )
        
        return render_template

    return error_404( request )

