class ComplexObject:
    def __init__(self, name, type, content):
        self.name = name
        self.type = type
        self.content = content
        self.imagePath = ''

    def setImagePath(self, path):
        self.imagePath = path