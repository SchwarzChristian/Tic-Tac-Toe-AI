from game import Game
from agents.human import HumanAgent
from agents.random import RandomAgent
from agents.AnnAgent import AnnAgent
from agents import Agent
import pandas as pd
from random import shuffle

# agent_1 = AnnAgent("human", "001")
agent_1 = RandomAgent("random")
# agent_1 = HumanAgent("ai opponent")
agent_2 = AnnAgent("ai", "001")

games = []
game_count = 10000
for i in range(game_count):
    agents = [agent_1, agent_2]
    shuffle(agents)
    result, protocol = Game(*agents, silent=True).play()
    print("{:5d}/{:5d}: {}".format(i + 1, game_count, result))
    games.append(result)

agent_2.save()

print()
print(pd.Series(games).value_counts())
