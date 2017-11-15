class Library:
    def __init__(self, tokens, dice, complexObjects, decks, bags, entities):
        self.tokens = tokens
        self.dice = dice
        self.complexObjects = complexObjects
        self.decks = decks
        self.bags = bags
        self.entities = entities

    def all(self):
        return self.tokens + self.dice + self.complexObjects + self.decks + self.bags