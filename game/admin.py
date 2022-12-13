from django.contrib import admin

from game.models.Player import Player
from game.models.Actions import Actions
from game.models.Business import Business
from game.models.PlayersBusiness import PlayersBusiness
from game.models.CommandPayments import CommandPayments
from game.models.BusinessPayments import BusinessPayments


admin.site.register(Player)
admin.site.register(Business)
admin.site.register(BusinessPayments)
admin.site.register(CommandPayments)
admin.site.register(Actions)
admin.site.register(PlayersBusiness)