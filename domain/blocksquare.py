class BlockSquare():

    def __init__(self, transform):
        self.transform = transform

    def as_dict(self):
        return {
            'Name': 'BlockSquare',
            'Transform': self.transform.as_dict(),
            'Nickname': '',
            'Description': '',
            'ColorDiffuse': {
                'r': 0.9264706,
                'g': 0.0,
                'b': 0.0
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