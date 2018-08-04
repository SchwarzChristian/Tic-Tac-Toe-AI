from random import shuffle
from os.path import isfile

import pandas as pd

from game import Game
from agents.human import HumanAgent
from agents.random import RandomAgent
from agents.AnnAgent import AnnAgent
from agents import Agent

batch_size = 100
result_filename = "results.csv"

batch = 0
while True:
    # agent_1 = RandomAgent("random")
    # agent_1 = HumanAgent("human")
    agent_1 = AnnAgent("klaus", "001", do_train=True, silent=True)
    agent_2 = AnnAgent("fritz", "002", do_train=True, silent=True)

    winners = []
    for game in range(batch_size):
        agents = [agent_1, agent_2]
        shuffle(agents)
        winner = Game(*agents).play()
        print("batch {:5d} | game: {:5d}/{:5d}: {}".format(batch + 1, game + 1, batch_size, winner))
        winners.append(winner)

    agent_1.save()
    agent_2.save()

    result = pd.Series(winners).value_counts()
    result["invalid_moves_klaus"] = agent_1.invalid_moves
    result["invalid_moves_fritz"] = agent_2.invalid_moves

    results = pd.DataFrame()
    if isfile(result_filename):
        results = pd.read_csv(result_filename, index_col=0)
    results = results.append(result, ignore_index=True)
    print(result)

    results.to_csv(result_filename)
    batch += 1
