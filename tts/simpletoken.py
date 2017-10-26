class SimpleToken():

    def __init__(self, typename, transform, color):
        self.typename = typename
        self.transform = transform
        self.color = color

    def get_tts_name(self):
        if self.typename.lower() == 'cube':
            return 'BlockSquare'
        elif self.typename.lower() == 'pawn':
            return 'PlayerPawn'
        elif self.typename.lower() == 'triangle':
            return 'BlockTriangle'
        else:
            raise ValueError("Unknown entity type: " + self.typename)

    def as_dict(self):
        return {
            'Name': self.get_tts_name(),
            'Transform': self.transform.as_dict(),
            'Nickname': '',
            'Description': '',
            'ColorDiffuse': {
                'r': self.color[0],
                'g': self.color[1],
                'b': self.color[2]
            },
            'Locked': False,
            'Grid': True,
            'Snap': True,
            'Autoraise': True,
            'Sticky': True,
            'Tooltip': True,
            'GridProjection': False,
            'Hands': False,
            'LuaScript': '',
            'LuaScriptState': '',
            'GUID': '8297db'
        }