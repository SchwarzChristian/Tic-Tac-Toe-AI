from typing import Any
from datetime import datetime

def deep_copy(obj: Any) -> Any:
    if type(obj) == list:
        return [ deep_copy(entry) for entry in obj ]

    if type(obj) == dict:
        return { k: deep_copy(v) for k, v in obj.items() }

    return obj

class Logger:
    def __init__(self, name: str, silent: bool = False) -> None:
        self._name = name
        self.silent = silent

    def log(self, *msg: Any) -> None:
        if not self.silent:
            print("{} - [{}]: ".format(str(datetime.now()), self._name), *msg)