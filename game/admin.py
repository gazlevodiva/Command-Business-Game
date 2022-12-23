from django.contrib import admin

from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Business import Business
from game.models.Surprises import Surprises
from game.models.GameSessions import GameSessions
from game.models.PlayersBusiness import PlayersBusiness
from game.models.CommandPayments import CommandPayments
from game.models.BusinessPayments import BusinessPayments


admin.site.register( CommandPayments )
admin.site.register( GameSessions )


class PlayerAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'level', 'visible' )

admin.site.register( Player, PlayerAdmin )


class ActionsAdmin( admin.ModelAdmin ):
    list_display = ( 'player', 'name', 'count' )
    list_filter = ( 'category', 'player' )

admin.site.register( Actions, ActionsAdmin )


class BusinessAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'category', 'cost', 'min_rent', 'max_rent', 'default' )
    list_filter = ( 'category', )

admin.site.register( Business, BusinessAdmin )


class PlayerBusinessAdmin( admin.ModelAdmin ):
    list_display = ('player', 'business', 'status', 'is_command' )
    list_filter = ( 'player', 'is_command', 'status', )

admin.site.register( PlayersBusiness, PlayerBusinessAdmin)


class BusinessPaymentsAdmin( admin.ModelAdmin ):
    list_display = ('player_business', 'count' )

admin.site.register( BusinessPayments, BusinessPaymentsAdmin )


class SurprisesAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'count', 'category' )
    list_filter = ( 'category', )

admin.site.register( Surprises, SurprisesAdmin )
