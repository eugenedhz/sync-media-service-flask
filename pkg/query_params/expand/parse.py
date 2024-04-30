from typing import Optional


def parse_expand(expand: Optional[str], valid_fields: tuple[str, ...]) -> Optional[dict]:
    if expand is None:
        return None

    expand = expand.split(',')

    expand = [field.split('.') for field in expand]

    for field in expand:
        if field[0] not in valid_fields:
            raise KeyError

    expand_dict = {}

    for field in expand:
        if len(field) == 2:
            expand_dict[field[0]] = field[1].split('select=')[1]
        else:
            expand_dict[field[0]] = None

    return expand_dict
