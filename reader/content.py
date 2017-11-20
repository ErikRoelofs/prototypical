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
            content_type = splits[0].strip()
        else:
            if splits[0].isdigit():
                amount = int(splits[0])
                content_type = splits[1].strip()
            else:
                amount = 1
                content_type = splits[0].strip() + "x" + splits[1].strip()
        contentItems.append((amount, content_type))
    return contentItems
