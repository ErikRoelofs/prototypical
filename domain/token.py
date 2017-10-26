class Token():
    def __init__(self, name, entity, color, size):
        self.name = name
        self.entity = entity
        self.color = color
        self.size = size

class ContentToken(Token):
    def __init__(self, name, entity, bg_color, text_color, content ):
        self.name = name
        self.entity = entity
        self.bg_color = bg_color
        self.text_color = text_color
        self.content = content
        self.imagePath = ''

    def setImagePath(self, path):
        self.imagePath = path