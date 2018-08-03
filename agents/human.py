from sys import stdin
from . import Agent
from game.field import Field

class HumanAgent(Agent):
    def __init__(self, name):
        Agent.__init__(self, name)

    def move(self, field: Field):
        print(field.as_ascii)
        print(self.name + "'s turn:")
        return eval(stdin.readline())

    def save(self) -> None:
        pass

    def train(self, winner: str, protocol) -> None:
        pass
