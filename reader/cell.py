import re

def read_cell(value):
    parts = re.findall('\d+|\D+', value)
    if len(parts) != 2:
        raise ValueError("Malformed cell value: " + value)
    col = 0
    for char in parts[0]:
        # move forward one position
        col *= 26
        # convert column name to number
        col += ord(char) - 64

    # both zero indexed
    return(col - 1, int(parts[1]) - 1 )