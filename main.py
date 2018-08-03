from game import Game
from agents.human import HumanAgent
from agents.random import RandomAgent
from agents.AnnAgent import AnnAgent
from agents import Agent
import pandas as pd
from random import shuffle

agent_1 = HumanAgent("human agent")
agent_2 = AnnAgent("ai agent")

games = []
for i in range(10):
    agents = [agent_1, agent_2]
    shuffle(agents)
    result, protocol = Game(*agents).play()
    print(result)
    games.append(result)

agent_2.save()

print()
print(pd.Series(games).value_counts())
