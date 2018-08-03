from npyscreen import Form
from agents import Agent
from .field import Field
from typing import Tuple, Dict, Any, List
from util import deep_copy

ProtocolAgentEntry = Dict[ str, Any ]
ProtocolEntry = Dict[ str, ProtocolAgentEntry ]
Protocol = List[ ProtocolEntry ]

class Game:
    def __init__(self, agent_1: Agent, agent_2: Agent):
        agent_1.symbol = "X"
        agent_2.symbol = "O"

        self._field = Field()
        self._agent_1 = agent_1
        self._agent_2 = agent_2
    
    def play(self) -> Tuple[ str, Protocol ]:
        protocol = []
        while True:
            protocol_entry = {}
            result, protocol_agent_entry = self._play(self._agent_1)
            protocol_entry[self._agent_1.name] = protocol_agent_entry
            if result != "continue":
                print(self._field.as_ascii)
                protocol.append(protocol_entry)
                if result == "win":
                    self._agent_1.train(self._agent_1.name, protocol)
                    self._agent_2.train(self._agent_1.name, protocol)
                return ( self._agent_1.name + ": " + result, protocol )

            result, protocol_agent_entry = self._play(self._agent_2)
            protocol_entry[self._agent_2.name] = protocol_agent_entry
            protocol.append(protocol_entry)
            if result != "continue":
                print(self._field.as_ascii)
                if result == "win":
                    self._agent_1.train(self._agent_2.name, protocol)
                    self._agent_2.train(self._agent_2.name, protocol)
                return ( self._agent_2.name + ": " + result, protocol )

        

    def _play(self, agent: Agent) -> Tuple[ str, ProtocolAgentEntry ]:
        protocol_agent_entry = { "field": deep_copy(self._field.field) }
        print(self._field.as_ascii)
        move = agent.move(self._field)
        protocol_agent_entry["move"] = move
        return ( self._field.move(*move, agent), protocol_agent_entry )
