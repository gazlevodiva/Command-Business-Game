
class Modal:

    def __init__(self, title, player):
        self.player = player
        self.title = title
        self.type = ""
        self.actions = []
        self.surprise = ""

    def add_action(self, action):
        self.actions.append(
            action
        )

    def __str__(self) -> str:
        return f'''{self.player.name}: {self.title}'''

    def obj(self):
        return self
