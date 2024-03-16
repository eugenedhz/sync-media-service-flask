def parse_formdata(formdata: dict) -> dict:
    formdata_dict = {}

    for key, value in formdata.items():
        if value.lower() == 'true':
            formdata_dict[key] = True
        elif value.lower() == 'false':
            formdata_dict[key] = False
        elif value.isdigit():
            formdata_dict[key] = int(value)
        else:
            formdata_dict[key] = value

    return formdata_dict