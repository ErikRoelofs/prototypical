def read_dimensions(value):
    strs = value.split('x')
    return (int(strs[0]), int(strs[1]))