class Library:
    def __init__(self, tokens, dice, complexObjects, decks, bags):
        self.tokens = tokens
        self.dice = dice
        self.complexObjects = complexObjects
        self.decks = decks
        self.bags = bags

    def all(self):
        return self.tokens + self.dice + self.complexObjects + self.decks + self.bags