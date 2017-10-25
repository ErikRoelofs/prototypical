class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)

    def nextId(self):
        return len(self.cards)+1