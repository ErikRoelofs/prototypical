class ComplexObject:
    def __init__(self, name, type, content):
        self.name = name
        self.type = type
        self.content = content
        # only used if this is a board, not used if its a deck
        self.imagePath = ''

    def setImagePath(self, path):
        self.imagePath = path

    def bgcolor(self):
        return self.type.bgColor