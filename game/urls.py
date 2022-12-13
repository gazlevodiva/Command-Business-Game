from django.urls import path

from game.views import reset
from game.views import dashboard
from game.views import new_player
from game.views import player_control
from game.views import sell_business
from game.views import set_defoult
from game.views import new_level
from game.views import sell_share
from game.views import surprise
from game.views import index
from game.views import rules
from game.views import test

urlpatterns = [
    path(
        route='', 
        view=index.index, 
        name='index_view',
    ),
    path(
        route='test/', 
        view=test.test, 
        name='test_view',
    ),
    path(
        route='reset/', 
        view=reset.reset, 
        name='reset_view',
    ),
    path(
        route='rules/', 
        view=rules.rules, 
        name='rules_view',
    ),
    path(
        route='get_surprise_<int:player_id>/', 
        view=surprise.surprise, 
        name='surprise_view',
    ),
    path(
        route='dashboard/', 
        view=dashboard.dashboard, 
        name='dashboard_view',
    ),
    path(
        route='new_player/', 
        view=new_player.new_player, 
        name='new_player_view',
    ),
    path(
        route='player_control_<int:player_id>/', 
        view=player_control.player_control, 
        name='player_control_view',
    ),
    path(
        route='sell_business_<int:player_business_id>/', 
        view=sell_business.sell_business, 
        name='sell_business_view',
    ),
    path(
        route='sell_share_<int:player_id>/', 
        view=sell_share.sell_share, 
        name='sell_share_view',
    ),
    path(
        route='new_level_<int:player_id>/', 
        view=new_level.new_level, 
        name='new_level_view',
    ),
    path(
        route='set_defoult_<int:player_business_id>/', 
        view=set_defoult.set_defoult, 
        name='set_defoult_view',
    ),
]