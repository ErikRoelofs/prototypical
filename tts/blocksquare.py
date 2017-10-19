class BlockSquare():

    def __init__(self, transform, color):
        self.transform = transform
        self.color = color

    def as_dict(self):
        return {
            'Name': 'BlockSquare',
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