class Bag:
    def __init__(self, name):
        self.name = name
        self.content = []

    def addContent(self, amount, content):
        self.content.append((amount, content))

class InfiniteBag (Bag):
    def addContent(self, amount, content):
        if len(self.content) == 1:
            raise ValueError("There is no point to putting more than one thing in an Infinite bag.")
        self.content.append((amount, content))
