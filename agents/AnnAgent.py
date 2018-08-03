from typing import Tuple, List
from os.path import isfile

import numpy as np
from keras.layers import Dense, Input, Reshape
from keras.models import Sequential, model_from_json

from . import Agent
from game.field import Field

class AnnAgent(Agent):
    def __init__(self, name: str, model_name: str = None) -> None:
        Agent.__init__(self, name)
        self._model_name = model_name or name
        self._model = self._init_model()
        self._randomness = 0.2
        self._invalid_moves = 0

    def move(self, field: Field) -> Tuple[ int, int ]:
        transformed_field = np.array([ self._transform_field(field.field) ])
        while True:
            decision = self._model.predict(transformed_field)[0] + np.random.rand(9) * self._randomness - self._randomness / 2
            decision_field = decision.argmax()
            move = np.unravel_index(decision_field, (3, 3))
            if not self.silent:
                print("quality", decision[decision_field] - decision.mean())
            if field.is_valid(*move):
                return move
            else:
                self._invalid_moves += 1
                label = np.ones(9)
                label[decision_field] = 0
                self._model.fit(transformed_field, label.reshape(1, 9), epochs=1, verbose=int(not self.silent))

    def save(self) -> None:
        print("invalid moves:", self._invalid_moves)
        print("saving model")
        model_filename = self._model_name + ".model"
        weights_filename = self._model_name + ".weights"

        with open(model_filename, "w") as f:
            f.write(self._model.to_json())
        
        self._model.save_weights(weights_filename)

    def train(self, winner: str, protocol) -> None:
        x = []
        y_idx = []

        for entry in protocol:
            if not winner in entry.keys():
                break
            entry = entry[winner]
            x.append(self._transform_field(entry["field"]))
            y_idx.append(self._transform_label(*entry["move"]))

        x = np.array(x)
        y = np.zeros((len(y_idx), 9))
        y[np.arange(len(y_idx)), y_idx] = 1

        self._model.fit(np.array(x), np.array(y), epochs=10, verbose=int(not self.silent))

    def _transform_label(self, row: int, col: int) -> int:
        return row * 3 + col

    def _transform_field(self, field: List[List[str]]) -> List[ List[ int ] ]:
        def map_field(field: str) -> List[int]:
            if field == " ": return [1, 0, 0]
            if field == self.symbol: return [0, 1, 0]
            return [0, 0, 1]
        return [ [ map_field(f) for f in row ] for row in field ]

    def _init_model(self) -> Sequential:
        print("initializing model")
        model_filename = self._model_name + ".model"
        weights_filename = self._model_name + ".weights"
        if isfile(model_filename) and isfile(weights_filename):
            print("saved model found")
            with open(model_filename) as f:
                model = model_from_json(f.read())
                model.load_weights(weights_filename)
        else:
            print("building new model")
            model = Sequential()
            model.add(Reshape((27,), input_shape=(3, 3, 3)))
            model.add(Dense(15, activation="sigmoid"))
            model.add(Dense(9, activation="sigmoid"))

        model.compile("adam", "binary_crossentropy")

        return model
