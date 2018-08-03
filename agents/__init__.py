from typing import Tuple

class Agent:
    @property
    def name(self):
        return self._name

    def __init__(self, name):
        self._name = name
        self.symbol = "-"
        self.silent = False

    def save(self) -> None:
        raise NotImplementedError

    def train(self, winner: str, protocol) -> None:
        raise NotImplementedError

    def move(self, filed) -> Tuple[int, int]:
        raise NotImplementedError