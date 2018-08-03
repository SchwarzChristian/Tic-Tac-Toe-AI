from typing import Any

def deep_copy(obj: Any) -> Any:
    if type(obj) == list:
        return [ deep_copy(entry) for entry in obj ]

    if type(obj) == dict:
        return { k: deep_copy(v) for k, v in obj.items() }

    return obj
