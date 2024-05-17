from typing import Optional


def parse_expand(expand: Optional[str], valid_fields: tuple[str, ...]) -> Optional[list[str]]:
    if expand is None:
        return None

    expand = expand.split(',')

    for field in expand:
        if field not in valid_fields:
            raise KeyError

    return expand
