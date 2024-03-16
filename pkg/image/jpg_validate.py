def is_valid_jpg(data):
    if len(data) < 16:
        return False

    if not(data[:2] == b'\xff\xd8'):
        return False

    return True