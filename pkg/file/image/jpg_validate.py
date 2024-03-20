def is_valid_jpg(data, extension: str, valid_extensions: tuple[str, ...]):
    if extension not in valid_extensions:
        return False

    if len(data) < 16:
        return False

    if not(data[:2] == b'\xff\xd8'):
        return False

    return True