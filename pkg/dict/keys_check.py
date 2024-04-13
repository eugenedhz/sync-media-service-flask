from typing import Any


def find_keys(dict: dict[str, Any], f_keys: tuple[str, ...]) -> list[str, ...] | None:
    found_keys = []
    for f_key in f_keys:
        if f_key in dict.keys():
            found_keys.append(f_key)
    if found_keys:
        return found_keys
    return None
