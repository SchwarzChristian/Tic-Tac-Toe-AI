from typing import List
from agents import Agent

class Field:
    def __init__(self, player_map = None):
        self._field = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ]
        self._last_move = (-1, -1)

    @property
    def field(self) -> List[ List[str] ]:
        return self._field

    @property
    def as_ascii(self) -> str:
        field = "+---+---+---+\n"
        for y in range(3):
            field += "|"
            for x in range (3):
                if self._last_move == (x, y):
                    field += ">{}<|".format(self._field[y][x])
                else:
                    field += " {} |".format(self._field[y][x])
            field += "\n+---+---+---+\n"
        return field
        
    def move(self, x: int, y: int, agent: Agent) -> str:
        self._last_move = (x, y)

        if not self.is_valid(x, y):
            return "invalid move"
        
        self._field[y][x] = agent.symbol

        if self._is_win(x, y):
            return "win"

        if self._is_draw():
            return "draw"

        return "continue"

    def is_valid(self, x: int, y: int) -> bool:
        if not x in range(3) or not y in range(3): return False
        return self._field[y][x] == " "

    def _is_win(self, x: int, y: int) -> bool:
        if self._field[y][0] == self._field[y][1] and self._field[y][0] == self._field[y][2]: return True
        if self._field[0][x] == self._field[1][x] and self._field[0][x] == self._field[2][x]: return True
        if self._field[1][1] != " ":
            if self._field[0][0] == self._field[1][1] and self._field[0][0] == self._field[2][2]: return True
            if self._field[0][2] == self._field[1][1] and self._field[0][2] == self._field[2][0]: return True
        return False

    def _is_draw(self) -> bool:
        return not True in [ " " in a for a in self._field ]