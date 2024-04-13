def files_in_request(request, files: tuple[str]) -> bool:
    for filename in files:
        if filename in request.files:
            return True
    return False
