class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def addCard(self, card, count):
        self.cards.append((card, count))