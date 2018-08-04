from typing import Tuple, List, Dict
from os.path import isfile
from datetime import datetime
import json
from util import Logger, deep_copy

import numpy as np
from keras.layers import Dense, Input, Reshape
from keras.models import Sequential, model_from_json

from . import Agent
from game.field import Field

class AnnAgent(Agent):
    def __init__(
        self,
        name: str,
        model_name: str = None,
        do_train: bool = True,
        silent: bool = False,
        **kwargs: Dict[ str, float ]
    ) -> None:
        Agent.__init__(self, name)
        self._model_name = model_name or name
        self._model = self._init_model()
        self._invalid_moves = 0
        self._protocol = []
        self._do_train = do_train
        self._log = Logger(self.__class__.__name__, silent).log

        default_params = self._load_params() or {
            "gamma": 0.9,
            "eps": 0.9,
            "eps_decay": 0.999,
            "min_eps": 0.1,
            "move_win_reward": -1,
            "move_loose_reward": 1,
            "move_draw_reward": 0,
            "win_reward": 30,
            "loose_reward": -30,
            "draw_reward": 0,
            "invalid_move_reward": -100,
        }
        self._params = { **default_params, **kwargs }

    def move(self, state: Field) -> Tuple[ int, int ]:
        transformed_field = self._transform_field(state.field)
        while True:
            self._log("eps:", self._params["eps"])
            mode = None
            if np.random.rand() < self._params["eps"]:
                mode = "exploring"
                self._log(mode)
                decision_field = np.random.randint(9)
            else:
                mode = "exploiting"
                self._log(mode)
                decision = self._model.predict(transformed_field)[0]
                self._log("Q's:\n", decision.reshape(3,3).T)
                decision_field = decision.argmax()
            move = np.unravel_index(decision_field, (3, 3))
            if state.is_valid(*move):
                self._protocol.append({
                    "state": deep_copy(state.field),
                    "action": decision_field,
                })
                return move
            else:
                if mode == "exploiting":
                    self._invalid_moves += 1
                self._train(state.field, decision_field, self._params["invalid_move_reward"])

    @property
    def invalid_moves(self):
        moves = self._invalid_moves
        self._invalid_moves = 0
        return moves

    def save(self) -> None:
        print("eps:", self._params["eps"])
        print("saving model")
        model_filename = self._model_name + ".model"
        weights_filename = self._model_name + ".weights"
        params_filename = self._model_name + ".params"

        with open(params_filename, "w") as f:
            json.dump(self._params, f)

        with open(model_filename, "w") as f:
            f.write(self._model.to_json())
        
        self._model.save_weights(weights_filename)

    def game_over(self, result: str) -> None:
        move_reward = self._params["move_{}_reward".format(result)]
        reward = len(self._protocol) * move_reward + self._params[result + "_reward"]
        for entry in self._protocol:
            self._train(entry["state"], entry["action"], reward)
            reward *= self._params["gamma"]
            
        if self._params["eps"] > self._params["min_eps"]:
            self._params["eps"] *= self._params["eps_decay"]
        self._protocol = []

    def _train(self, state: Field, action: int, reward: float) -> None:
        if not self._do_train: return
        self._log("reward:", reward)
        self._log("state:\n", Field.to_ascii(state, np.unravel_index(action, (3, 3))))
        state = self._transform_field(state)
        target_vec = self._model.predict(state)[0]
        self._log("Q's:\n", target_vec.reshape(3,3).T)
        target_vec[action] = reward
        self._log("target:\n", target_vec.reshape(3,3).T)
        self._model.fit(state, np.array([ target_vec ]), epochs=1, verbose=0)

    def _transform_label(self, row: int, col: int) -> int:
        return row * 3 + col

    def _transform_field(self, field: List[ List[ int ] ]) -> List[ List[ int ] ]:
        def map_field(field: str) -> List[int]:
            if field == " ": return [1, 0, 0]
            if field == self.symbol: return [0, 1, 0]
            return [0, 0, 1]
        return np.array([ [ [ map_field(f) for f in row ] for row in field ] ])

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
            model.add(Dense(100, activation="linear"))
            model.add(Dense(100, activation="linear"))
            model.add(Dense(9, activation="linear"))

        model.compile("adam", "mse")

        return model

    def _load_params(self) -> Dict[ str, float ]:
        filename = self._model_name + ".params"
        if not isfile(filename): return None
        with open(filename) as f:
            params = json.load(f)
            return params
