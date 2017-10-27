def read_dimensions(value):
    strs = value.split('x')
    if len(strs) != 2:
        raise ValueError("Malformed dimensions: " + value + " (should be something like `600x400`)")
    return (int(strs[0]), int(strs[1]))