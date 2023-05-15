from django.urls import path

from game.views.player_panel import player_controller
from game.views.player_panel import sell_business
from game.views.player_panel import sell_share
from game.views.player_panel import new_level
from game.views.player_panel import surprise
from game.views.player_panel import rules

from game.views import session_controller
from game.views import new_player
from game.views import dashboard
from game.views import finish
from game.views import login
from game.views import index
from game.views import test


urlpatterns = [
    path(
        route = '', 
        view  = index.index, 
        name  = 'index_view',
    ),
    path(
        route = 's/<str:session_hash>/', 
        view  = index.index, 
        name  = 'index_view',
    ),
    path(
        route = 'test/', 
        view  = test.test, 
        name  = 'test_view',
    ),
    path(
        route = 'rules/', 
        view  = rules.rules, 
        name  = 'rules_view',
    ),
    path(
        route = 'get_surprise_<int:player_id><str:surprise_type>/', 
        view  = surprise.surprise, 
        name  = 'surprise_view',
    ),
    path(
        route = 'dashboard/', 
        view  = dashboard.dashboard, 
        name  = 'dashboard_view',
    ),
    path(
        route = 'new_player/', 
        view  = new_player.new_player, 
        name  = 'new_player_view',
    ),
    path(
        route = 'player_control_<int:player_id>/', 
        view  = player_controller.player_control, 
        name  = 'player_control_view',
    ),
    path(
        route = 'get_player_control_data_<int:player_id>/', 
        view  = player_controller.player_control_data, 
        name  = 'player_control_data_ajax',
    ),
    path(
        route = 'get_player_control_business_data_<int:player_id>_<str:business_category>/', 
        view  = player_controller.player_control_business_data, 
        name  = 'player_control_business_data_ajax',
    ),
    path(
        route = 'buy_<str:is_command>_business_<int:player_id>_<int:business_id>/', 
        view  = player_controller.player_control_buy_business, 
        name  = 'player_control_buy_business_view',
    ),
    path(
        route = 'sell_business_<int:player_business_id>/', 
        view  = sell_business.sell_business, 
        name  = 'sell_business_view',
    ),
    path(
        route = 'sell_share_<int:player_id>_<int:count>/', 
        view  = sell_share.sell_share, 
        name  = 'sell_share_view',
    ),
    path(
        route = 'new_level_<int:player_id>/', 
        view  = new_level.new_level, 
        name  = 'new_level_view',
    ),
    path(
        route = 'finish/', 
        view  = finish.finish, 
        name  = 'finish_view',
    ),
    path(
        route = 'game_settings/', 
        view  = session_controller.session_panel, 
        name  = 'session_panel_view',
    ),
    path(
        route = 'reset_last_move/', 
        view  = session_controller.reset_last_move, 
        name  = 'reset_last_move_view',
    ),
    path(
        route = 'delete_player/<int:player_id>/', 
        view  = session_controller.delete_player, 
        name  = 'delete_player'
    ),
    path(
        route = 'login/', 
        view  = login.login, 
        name  = 'login_view',
    ),
]
