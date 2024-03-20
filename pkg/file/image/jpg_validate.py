def is_valid_jpg(data, extension: str):
    if extension not in ('.jpg', '.jpeg'):
        return False

    if len(data) < 16:
        return False

    if not(data[:2] == b'\xff\xd8'):
        return False

    return True