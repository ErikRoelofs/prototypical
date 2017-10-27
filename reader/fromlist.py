def read_fromlist(value, list):
    if not value.lower() in list:
        raise ValueError( value + " is not in list: " + str(list) )
    return value.lower()