from typing import Tuple, List
from os.path import isfile

import numpy as np
from keras.layers import Dense, Input, Reshape
from keras.models import Sequential, model_from_json

from . import Agent
from game.field import Field

class AnnAgent(Agent):
    def __init__(self, name: str) -> None:
        Agent.__init__(self, name)
        self._model = self._init_model()

    def move(self, field: Field) -> Tuple[ int, int ]:
        transformed_field = np.array([ self._transform_field(field.field) ])
        while True:
            print("getting move")
            decision = self._model.predict(transformed_field)[0]
            print(decision)
            move = np.unravel_index(decision.argmax(), (3, 3))
            print(move)
            if field.is_valid(*move):
                print("valid")
                return move
            else:
                print("invalid")
                label = np.ones(9)
                label[decision.argmax()] = 0
                self._model.fit(transformed_field, label.reshape(1, 9), epochs=1 )

    def save(self) -> None:
        print("saving model")
        model_filename = self._name + ".model"
        weights_filename = self._name + ".weights"

        with open(model_filename, "w") as f:
            f.write(self._model.to_json())
        
        self._model.save_weights(weights_filename)

    def train(self, winner: str, protocol) -> None:
        print("training", self.name)

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

        self._model.fit(np.array(x), np.array(y), epochs=10)

    def _transform_label(self, row: int, col: int) -> int:
        return row * 3 + col

    def _transform_field(self, field: List[List[str]]) -> List[ List[ int ] ]:
        field_map = {
            " ": [1, 0, 0],
            "X": [0, 1, 0],
            "O": [0, 0, 1],
        }
        return [ [ field_map[f] for f in row ] for row in field ]

    def _init_model(self) -> Sequential:
        print("initializing model")
        model_filename = self._name + ".model"
        weights_filename = self._name + ".weights"
        if isfile(model_filename) and isfile(weights_filename):
            print("saved model found")
            with open(model_filename) as f:
                model = model_from_json(f.read())
                model.load_weights(weights_filename)
        else:
            print("building new model")
            model = Sequential()
            # model.add(Input((3, 3, 3)))
            model.add(Reshape((27,), input_shape=(3, 3, 3)))
            model.add(Dense(15, activation="sigmoid"))
            model.add(Dense(9, activation="sigmoid"))

        model.compile("adam", "binary_crossentropy")

        return model
