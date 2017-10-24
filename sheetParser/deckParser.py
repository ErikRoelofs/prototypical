from domain.deck import Deck

class DeckParser:
    def parse(sheet):
        decks = {}
        current_deck = None
        row = 0
        while row < sheet.nrows:
            if sheet.cell(rowx=row, colx=0).value == 'Deck':
                # a new deck begins
                if current_deck:
                    decks[current_deck.name] = current_deck
                current_deck = Deck(sheet.cell(rowx=row, colx=1).value)
            else:
                # add card to current deck
                current_deck.addCard(sheet.cell(rowx=row, colx=0).value, int(sheet.cell(rowx=row, colx=1).value))
            row += 1

        if current_deck:
            decks[current_deck.name] = current_deck
        return decks
