from npyscreen import Form
from agents import Agent
from .field import Field
from typing import Tuple, Dict, Any, List
from util import deep_copy

class Game:
    def __init__(self, agent_1: Agent, agent_2: Agent):
        agent_1.symbol = "X"
        agent_2.symbol = "O"

        self._field = Field()
        self._agent_1 = agent_1
        self._agent_2 = agent_2
    
    def play(self) -> str:
        while True:
            result = self._play(self._agent_1)
            if result == "draw":
                self._agent_1.game_over("draw")
                self._agent_2.game_over("draw")
                return "draw"

            if result == "win":
                self._agent_1.game_over("win")
                self._agent_2.game_over("loose")
                return self._agent_1.name

            result = self._play(self._agent_2)
            if result == "draw": 
                self._agent_1.game_over("draw")
                self._agent_2.game_over("draw")
                return "draw"
            if result == "win":
                self._agent_1.game_over("loose")
                self._agent_2.game_over("win")
                return self._agent_2.name

        

    def _play(self, agent: Agent) -> str:
        move = agent.move(self._field)
        result = self._field.move(*move, agent)
        return result
