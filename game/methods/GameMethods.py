from game.models.Player import Player


def get_players_in_creation_order():
    return Player.objects.filter(visible=True).order_by("created_at")
