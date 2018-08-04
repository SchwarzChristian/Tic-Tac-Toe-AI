# Tic-Tac-Toe AI

Training AI using Reinforcement Learning with Feed Forward Neural Networks

## Usage
just run:
```
python main.py
```

You may want to update `main.py` first, to set up some parameter.

## Parameter
To set training parameter you need to modify `main.py`.

Above the main loop you can set the batch size (see [Training]() below). At the to of the main loop you can set up the agents that should play against each other (see [Agents]() below).

### Training
The training process runs in batches. Afer each batch the agents models are saved and a statistics dataset is appended to `results.csv`. The training runs until you abort it by hitting `Ctrl+C`.

### Agents
name        | description
------------|---
RandomAgent | This agent takes random moves.
HumanAgent  | This agent asks the user for moves. So you can play against the AI to test it manually. (when asked for a move, syntax is: `<row>,<column>`)
AnnAgent    | The AI agent. It will (hopefully) learn to play while doing so.
