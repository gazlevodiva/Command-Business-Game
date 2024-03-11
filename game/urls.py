from django.urls import path

from game.views.player_panel import player_controller
from game.views.player_panel import sell_business
from game.views.player_panel import buy_business_data
from game.views.player_panel import buy_business
from game.views.player_panel import sell_share
from game.views.player_panel import whoisturn
from game.views.player_panel import surprise
from game.views.player_panel import make_move
from game.views import rules

from game.views import session_controller
from game.views import new_player
from game.views import dashboard
from game.views import finish
from game.views import voting
from game.views import login
from game.views import index


urlpatterns = [
    path(
        route="",
        view=index.index,
        name="index_view",
    ),
    path(
        route="s/<str:session_hash>/",
        view=index.index,
        name="index_view",
    ),
    path(
        route="rules/",
        view=rules.rules,
        name="rules_view",
    ),
    path(
        route="dashboard/",
        view=dashboard.dashboard,
        name="dashboard_view",
    ),
    path(
        route="dashboard_online/",
        view=dashboard.dashboard_online,
        name="dashboard_online_view",
    ),
    path(
        route="whoisturn/<int:player_id>/",
        view=whoisturn.whois_turn_data,
        name="whois_turn_data",
    ),
    path(
        route="finish_move_<int:move_id>/",
        view=player_controller.player_finish_move,
        name="player_finish_move",
    ),
    path(
        route="go_to_start_<int:move_id>/",
        view=player_controller.player_go_to_start,
        name="player_go_to_start",
    ),
    path(
        route="back_to_start_<int:move_id>/",
        view=player_controller.player_back_to_start,
        name="player_back_to_start",
    ),
    path(
        route="player_move_<int:player_id>_<str:dice_value>/",
        view=make_move.player_move,
        name="online_player_move_result",
    ),
    path(
        route="new_player/",
        view=new_player.new_player,
        name="new_player_view",
    ),
    path(
        route="player_control_<int:player_id>/",
        view=player_controller.player_control,
        name="player_control_view",
    ),
    path(
        route="get_player_control_data_<int:player_id>/",
        view=player_controller.player_control_data,
        name="player_control_data_ajax",
    ),
    path(
        route="get_player_control_business_data_<int:player_id>_<str:business_category>/",
        view=buy_business_data.player_control_business_data,
        name="player_control_business_data_ajax",
    ),
    path(
        route="buy_<str:is_command>_business_<int:player_id>_<int:business_id>/",
        view=buy_business.player_control_buy_business,
        name="player_control_buy_business_view",
    ),
    path(
        route="sell_business_<int:player_business_id>/",
        view=sell_business.sell_business,
        name="sell_business_view",
    ),
    path(
        route="sell_share_<int:player_id>_<int:count>/",
        view=sell_share.sell_share,
        name="sell_share_view",
    ),
    path(
        route="finish/",
        view=finish.finish,
        name="finish_view",
    ),
    path(
        route="game_settings/",
        view=session_controller.session_panel,
        name="session_panel_view",
    ),
    path(
        route="memory_setup/",
        view=session_controller.memory_setup,
        name="memory_setup",
    ),
    path(
        route="reset_game/",
        view=session_controller.reset_game,
        name="reset_game_fetch",
    ),
    path(
        route="session_players/",
        view=session_controller.session_players,
        name="session_players_fetch",
    ),
    path(
        route="delete_player/<int:player_id>/",
        view=session_controller.delete_player,
        name="delete_player_fetch",
    ),
    path(
        route="upload_memory_file/",
        view=session_controller.upload_memory_file,
        name="upload_memory_file_fetch",
    ),
    path(
        route="login/",
        view=login.login,
        name="login_view",
    ),
    path(
        route="new_vote/<int:move_id>/<int:player_id>/<str:vote_category>/",
        view=voting.set_vote,
        name="set_vote",
    ),
    path(
        route="get_votion_data/<int:move_id>/",
        view=voting.get_votion_data,
        name="get_votion_data",
    ),
]
