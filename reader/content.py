def read_content(value):
    if value == '':
        return ()
    parts = value.split(';')
    contentItems = []
    for part in parts:
        if part == '':
            continue
        splits = part.split('x', 1)
        if len(splits) == 1:
            amount = 1
            type = splits[0].strip()
        else:
            try:
                amount = int(splits[0])
                type = splits[1].strip()
            except ValueError as e:
                raise ValueError("Unable to read amount of items to place. " + splits[0] + " is not a valid number.") from None
        contentItems.append((amount, type))
    return contentItems
