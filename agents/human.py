from sys import stdin
from . import Agent

class HumanAgent(Agent):
    def __init__(self, name):
        Agent.__init__(self, name)

    def move(self, field):
        print(self.name + "'s turn:")
        return eval(stdin.readline())

    def save(self) -> None:
        pass

    def train(self, winner: str, protocol) -> None:
        pass
        