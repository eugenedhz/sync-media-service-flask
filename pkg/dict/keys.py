from typing import Any


def find_keys(dict: dict[str, Any], keys: tuple[str, ...]) -> list[str, ...] | None:
    found_keys = []
    for key in keys:
        if key in dict.keys():
            found_keys.append(key)
    return found_keys
