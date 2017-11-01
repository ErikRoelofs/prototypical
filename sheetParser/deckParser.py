from domain.deck import Deck
from domain.card import Card
from reader.number import read_number

class DeckParser:
    def parse(sheet, complexObjects):
        decks = []
        current_deck = None
        row = 0
        while row < sheet.nrows:
            if sheet.cell(rowx=row, colx=0).value == 'Deck':
                # a new deck begins
                if current_deck and current_deck.cards:
                    decks.append(current_deck)
                current_deck = Deck(sheet.cell(rowx=row, colx=1).value)
            else:
                # add card to current deck
                try:
                    card = DeckParser.findObject(sheet.cell(rowx=row, colx=0).value, complexObjects)
                    amount = read_number(sheet.cell(rowx=row, colx=1).value)
                except ValueError as e:
                    raise ValueError(str(e) + " (while generating content for " + current_deck.name + ")") from None

                id = current_deck.nextId()
                current_deck.addCard(Card(card, amount, id))
            row += 1

        if current_deck and current_deck.cards:
            decks.append(current_deck)
        return decks

    def findObject(name, objects):
        for obj in objects:
            if obj.name == name:
                return obj
        raise ValueError("Unknown card by name: " + str(name))