class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.imagePath = ''
        self.backImagePath = ''

    def addCard(self, card):
        self.cards.append(card)

    def nextId(self):
        return len(self.cards)+1

    def setImagePath(self, path):
        self.imagePath = path

    def setBackImagePath(self, path):
        self.backImagePath = path
