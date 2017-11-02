def read_column_reference(value,reduceF):
    if value[0] == '{' and value[len(value)-1] == '}':
        col = value[1:len(value)-1]
        return reduceF(col)
    raise ValueError("Could not read " + value + " as a column reference.")