
from django.shortcuts import redirect
from django.http import Http404

from game.models.GameSessions import GameSessions
from game.views.page404 import error_404


def check_user_session_hash( view ):
    def wrapped( request, *args, **kwargs ):

        if request.user.is_authenticated:
            return view( request, *args, **kwargs )

        try:
            print('check_user_session_hash: Try get session_hash') 

            session_hash = request.COOKIES['game_session_hash'] 
            last_game_session = GameSessions.objects.latest( 'created_date' )

            if last_game_session.session_hash != session_hash:
                print('check_user_session_hash: No session_hash in DB. Return 404')
                return error_404( request )
        
        except:
            print('check_user_session_hash: No session_hash. Return 404')
            return error_404( request )

        return view( request, *args, **kwargs )

    return wrapped
