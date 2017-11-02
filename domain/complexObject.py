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
        return self.type.decide_bg_color(self)

    def backcolor(self):
        return self.type.decide_back_color(self)