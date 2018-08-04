# Tic-Tac-Toe AI

Training AI using [Reinforcement](https://en.wikipedia.org/wiki/Reinforcement_learning) Learning with [Feed Forward Neural Networks](https://en.wikipedia.org/wiki/Feedforward_neural_network)

## Usage
just run:
```
python main.py
```

You may want to update `main.py` first, to set up some parameter.

## Parameter
To set training parameter you need to modify `main.py`.

Above the main loop you can set the batch size (see [Training](#training) below). At the to of the main loop you can set up the agents that should play against each other (see [Agents](#agents) below).

### Training
The training process runs in batches. Afer each batch the agents models are saved and a statistics dataset is appended to `results.csv`. The training runs until you abort it by hitting `Ctrl+C`.

### Agents
name        | description
------------|-------------
RandomAgent | This agent takes random moves.
HumanAgent  | This agent asks the user for moves. So you can play against the AI to test it manually. (when asked for a move, syntax is: `<row>,<column>`)
AnnAgent    | The AI agent. It will (hopefully) learn to play while doing so.

## Analytics
If you have [Jupyter](http://jupyter.org/) installed, you can use the following notebooks to analyze the models:

Notebook                    | description
----------------------------|-------------
Visualize Training Progress | Plots win, draw and invalid move counts per batch to show how this values evolved over the training.
Analytics                   | Can be used to plot the Q values predicted by the given models for a given state.

The Notebooks should become self-descriptive, so no more description will be added here.
