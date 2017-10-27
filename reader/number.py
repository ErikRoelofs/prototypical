def read_number(value):
    try:
        return int(value)
    except ValueError as e:
        raise ValueError("This is not a valid number: " + value)

def read_float(value):
    try:
        return float(value)
    except ValueError as e:
        raise ValueError("This is not a valid number: " + value)