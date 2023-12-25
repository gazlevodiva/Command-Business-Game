from django.contrib import admin

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Business import Business
from game.models.Surprises import Surprises
from game.models.GameSessions import GameSessions
from game.models.MemoryAnswers import MemoryAnswers
from game.models.PlayersBusiness import PlayersBusiness
from game.models.PlayersBusinessStatus import PlayersBusinessStatus
from game.models.CommandPayments import CommandPayments
from game.models.BusinessPayments import BusinessPayments


class GameSessionsAdmin(admin.ModelAdmin):
    list_display = ("session_name", "session_hash", "game_mode")
    list_filter = ("game_mode",)


admin.site.register(GameSessions, GameSessionsAdmin)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "visible", "game_session")
    list_filter = ("game_session",)


admin.site.register(Player, PlayerAdmin)


class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "cost",
        "min_rent",
        "max_rent",
        "default",
        "game_mode",
    )
    list_filter = ("category", "game_mode")


admin.site.register(Business, BusinessAdmin)


class SurprisesAdmin(admin.ModelAdmin):
    list_display = ("name", "count", "category", "session_id")
    list_filter = ("session_id", "category")


admin.site.register(Surprises, SurprisesAdmin)


#################################################################################


# Filter for MovesAdmin
class FilterMoveByGameSession(admin.SimpleListFilter):
    title = "Game Session"
    parameter_name = "game_session"

    def lookups(self, request, model_admin):
        game_sessions = set(
            obj.player.game_session for obj in model_admin.model.objects.all()
        )
        return [(gs.pk, gs) for gs in game_sessions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(player__game_session__pk=self.value())
        return queryset


# Filter for MovesAdmin
class FilterMoveByPlayerInChosenSession(admin.SimpleListFilter):
    title = "Player in selected Game Session"
    parameter_name = "player_in_selected_game_session"

    def lookups(self, request, model_admin):
        game_session_id = request.GET.get("game_session", None)
        if game_session_id:
            players = Player.objects.filter(game_session__pk=game_session_id)
            return [(player.pk, player) for player in players]
        return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(player__pk=self.value())
        return queryset


class MovesAdmin(admin.ModelAdmin):
    list_display = ("number", "player", "get_game_session")
    list_filter = (
        FilterMoveByGameSession,
        FilterMoveByPlayerInChosenSession,
    )

    def get_game_session(self, obj):
        return obj.player.game_session


admin.site.register(Moves, MovesAdmin)


#################################################################################


# Filter for ActionsAdmin
class FilterActionsByPlayerInChosenSession(admin.SimpleListFilter):
    title = "Player in selected Game Session"
    parameter_name = "player_in_selected_game_session"

    def lookups(self, request, model_admin):
        game_session_id = request.GET.get("game_session", None)
        if game_session_id:
            players = Player.objects.filter(game_session__pk=game_session_id)
            return [(player.pk, player) for player in players]
        return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(move__player__pk=self.value())
        return queryset


# Filter for ActionsAdmin
class FilterActionByGameSession(admin.SimpleListFilter):
    title = "Game Session"
    parameter_name = "game_session"

    def lookups(self, request, model_admin):
        game_sessions = set(
            obj.move.player.game_session
            for obj in model_admin.model.objects.all()
            if obj.move
        )
        return [(gs.pk, gs) for gs in game_sessions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(move__player__game_session__pk=self.value())
        return queryset


class ActionsAdmin(admin.ModelAdmin):
    list_display = (
        "get_action_player",
        "get_move_number",
        "get_move_position",
        "move_stage",
        "name",
        "count",
        "category",
        "is_command",
        "is_public",
        "is_personal",
    )
    list_filter = (
        "move_stage",
        "category",
        "is_public",
        "is_personal",
        FilterActionByGameSession,
        FilterActionsByPlayerInChosenSession,
    )

    def get_move_number(self, obj):
        return obj.move.number if obj.move else None

    def get_action_player(self, obj):
        return obj.move.player if obj.move else None

    def get_move_position(self, obj):
        return obj.move.position if obj.move else None


admin.site.register(Actions, ActionsAdmin)


#################################################################################


# Filter for CommandPaymentsAdmin
class FilterCommandPaymentsByGameSession(admin.SimpleListFilter):
    title = "Game Session"
    parameter_name = "game_session"

    def lookups(self, request, model_admin):
        game_sessions = set(
            obj.move.player.game_session
            for obj in model_admin.model.objects.all()
            if obj.move
        )
        return [(gs.pk, gs) for gs in game_sessions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(move__player__game_session__pk=self.value())
        return queryset


class CommandPaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "get_player",
        "get_move_number",
        "count",
        "get_game_session",
        "category",
    )
    list_filter = (FilterCommandPaymentsByGameSession, "category")

    def get_player(self, obj):
        return obj.move.player

    def get_move_number(self, obj):
        return obj.move.number if obj.move else None

    def get_game_session(self, obj):
        return obj.move.player.game_session


admin.site.register(CommandPayments, CommandPaymentsAdmin)


#################################################################################


# Filter for PlayerBusinessAdmin
class FilterPlayerBusinessByPlayerInChosenSession(admin.SimpleListFilter):
    title = "Player in selected Game Session"
    parameter_name = "player_in_selected_game_session"

    def lookups(self, request, model_admin):
        game_session_id = request.GET.get("game_session", None)
        if game_session_id:
            players = Player.objects.filter(game_session__pk=game_session_id)
            return [(player.pk, player) for player in players]
        return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(player__pk=self.value())
        return queryset


# Filter for CommandPaymentsAdmin
class FilterPlayerBusinessByGameSession(admin.SimpleListFilter):
    title = "Game Session"
    parameter_name = "game_session"

    def lookups(self, request, model_admin):
        game_sessions = set(
            obj.player.game_session for obj in model_admin.model.objects.all()
        )
        return [(gs.pk, gs) for gs in game_sessions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(player__game_session__pk=self.value())
        return queryset


class PlayerBusinessAdmin(admin.ModelAdmin):
    list_display = (
        "business",
        "player",
        "get_game_session",
        "get_status",
        "is_command",
    )
    list_filter = (
        "is_command",
        FilterPlayerBusinessByGameSession,
        FilterPlayerBusinessByPlayerInChosenSession,
    )

    def get_game_session(self, obj):
        return obj.player.game_session

    def get_status(self, obj):
        res = PlayersBusinessStatus.objects.filter(players_business=obj).last()
        return res


admin.site.register(PlayersBusiness, PlayerBusinessAdmin)


#################################################################################


class PlayerBusinessStatusAdmin(admin.ModelAdmin):
    list_display = ("players_business", "move", "status")
    list_filter = ("players_business", "status")


admin.site.register(PlayersBusinessStatus, PlayerBusinessStatusAdmin)


#################################################################################


class BusinessPaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "get_player",
        "get_business",
        "get_move_number",
        "count",
        "get_game_session",
    )
    list_filter = ()

    def get_player(self, obj):
        return obj.move.player if obj.move else None

    def get_business(self, obj):
        return obj.player_business.business if obj.player_business else None

    def get_move_number(self, obj):
        return obj.move.number if obj.move else None

    def get_game_session(self, obj):
        return obj.move.player.game_session if obj.move else None


admin.site.register(BusinessPayments, BusinessPaymentsAdmin)


#################################################################################


class PlayersMemoryAnswersFilter(admin.SimpleListFilter):
    title = "Player"
    parameter_name = "player_answer"

    def lookups(self, request, model_admin):
        game_session_id = request.GET.get("game_session", None)
        if game_session_id:
            players = Player.objects.filter(game_session__pk=game_session_id)
            return [(player.pk, player.name) for player in players]
        return []

    def queryset(self, request, queryset):
        player_id = self.value()
        if player_id:
            return queryset.filter(action__move__player__id=player_id)
        return queryset


class GameSessionMemoryAnswersFilter(admin.SimpleListFilter):
    title = "Game Session"
    parameter_name = "game_session"

    def lookups(self, request, model_admin):
        game_sessions = set(
            obj.action.move.player.game_session
            for obj in model_admin.model.objects.all()
        )
        return [(gs.pk, gs) for gs in game_sessions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(action__move__player__game_session__pk=self.value())
        return queryset


class MemoryAnswersAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "answer",
        "get_player",
    )
    list_filter = (
        PlayersMemoryAnswersFilter,
        GameSessionMemoryAnswersFilter,
    )

    def get_player(self, obj):
        return obj.action.move.player

    get_player.short_description = "Player"


admin.site.register(MemoryAnswers, MemoryAnswersAdmin)
