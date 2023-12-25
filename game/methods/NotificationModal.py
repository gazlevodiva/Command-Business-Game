class Modal:
    def __init__(self, title, player, surprise_id=0):
        self._player = player
        self._id = surprise_id
        self._title = title
        self._type = ""
        self._actions = []
        self._surprise = ""
        self._income = 0
        self._outcome = 0
        self._profit = 0

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def actions(self):
        return self._actions

    @property
    def surprise(self):
        return self._surprise

    @surprise.setter
    def surprise(self, value):
        self._surprise = value

    @property
    def income(self):
        return self._income

    @property
    def outcome(self):
        return self._outcome

    @property
    def profit(self):
        return self._profit

    def _update_financials(self, action):
        if action.count < 0 and action.category != "COMMAND":
            self._outcome += action.count
        if action.count > 0 and action.category != "COMMAND":
            self._income += action.count
        self._profit += action.count

    def add_action(self, action):
        self._update_financials(action)
        self._actions.append(action)

    def __str__(self) -> str:
        return f"{self.player.name}: {self.title}"
