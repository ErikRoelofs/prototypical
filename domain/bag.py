class Bag:
    def __init__(self, name, size, color):
        self.name = name
        self.size = size
        self.color = color
        self.content = []

    def addContent(self, amount, content):
        for i in range(0,amount):
            self.content.append(content)

class InfiniteBag (Bag):
    def addContent(self, amount, content):
        if len(self.content) == 1:
            raise ValueError("There is no point to putting more than one thing in an Infinite bag.")
        self.content.append(content)
