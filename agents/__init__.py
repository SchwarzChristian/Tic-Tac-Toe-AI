class Agent:
    @property
    def name(self):
        return "{} ({})".format(self._name, self.symbol)

    def __init__(self, name):
        self._name = name
        self.symbol = "-"

    def save(self) -> None:
        raise NotImplementedError

    def train(self, winner: str, protocol) -> None:
        raise NotImplementedError
