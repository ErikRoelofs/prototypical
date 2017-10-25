class Deck():
    def __init__(self, transform, name, cards, imagePath):
        self.transform = transform
        self.cards = cards
        self.name = name
        self.imagePath = imagePath

    def get_ids(self):
        ids = []
        for card in self.cards:
            ids.append(99 + card.id)
        return ids

    def get_cards(self):
        data = []
        for card in self.cards:
            data.append(self.card_as_dict(card))
        return data

    def card_as_dict(self, card):
        return {
            'Name': 'Card',
            'Transform': self.transform.as_dict(),
            'Nickname': '',
            'Description': '',
            'ColorDiffuse': {
                'r': 0.713235259,
                'g': 0.713235259,
                'b': 0.713235259
            },
            'Locked': False,
            'Grid': True,
            'Snap': True,
            'Autoraise': True,
            'Sticky': True,
            'Tooltip': True,
            'GridProjection': False,
            'Hands': True,
            'CardID': 99 + card.id,
            'SidewaysCard': False,
            'LuaScript': '',
            'LuaScriptState': '',
            'ContainedObjects': [],
            'GUID': '0b80cc'
        }

    def as_dict(self):
        return {
                'Name': 'DeckCustom',
                'Transform': self.transform.as_dict(),
                'Nickname': '',
                'Description': '',
                'ColorDiffuse': {
                    'r': 0.713235259,
                    'g': 0.713235259,
                    'b': 0.713235259
                },
                'Locked': False,
                'Grid': True,
                'Snap': True,
                'Autoraise': True,
                'Sticky': True,
                'Tooltip': True,
                'GridProjection': False,
                'Hands': False,
                'SidewaysCard': False,
                'DeckIDs': self.get_ids(),
                'CustomDeck': {
                    '1': {
                        'FaceURL': 'file:///' + self.imagePath,
                        'BackURL': 'file:///C:/Users/Pluisjen/Pictures/gradient.png',
                        'NumWidth': 10,
                        'NumHeight': 7,
                        'BackIsHidden': False,
                        'UniqueBack': False
                    }
                },
                'LuaScript': '',
                'LuaScriptState': '',
                'ContainedObjects': self.get_cards(),
                'GUID': 'a3cad1'
        }
