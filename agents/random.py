from . import Agent
from numpy.random import randint
from game.field import Field

class RandomAgent(Agent):
    def __init__(self, name: str):
        Agent.__init__(self, name)

    def move(self, field: Field) -> tuple:
        move = (-1, -1)
        while not field.is_valid(*move):
            move = (randint(3), randint(3))
        return move

    def save(self) -> None:
        pass

    def game_over(self, result: str) -> None:
        pass
