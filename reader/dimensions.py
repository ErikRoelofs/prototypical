def read_dimensions(value):
    strs = value.split('x')
    if len(strs) != 2:
        raise ValueError("Malformed dimensions: " + value + " (should be something like `600x400`)")
    vals = (int(strs[0]), int(strs[1]))
    if vals[0] <= 0 or vals[1] <= 0:
        raise ValueError("Malformed dimensions: " + value + " (both sides should be numbers that are 0 or greater")

    return vals