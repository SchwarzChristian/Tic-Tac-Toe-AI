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

    def game_over(self, result: str) -> None:
        raise NotImplementedError

    def move(self, filed) -> Tuple[int, int]:
        raise NotImplementedError