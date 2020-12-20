from tts.guid import guid

class Token():

    def __init__(self, transform, image ):
        self.transform = transform
        self.image = image

    def as_dict(self):
        return {
            'Name': 'Custom_Token',
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
            "CustomImage": {
                "ImageURL": self.image,
                "ImageSecondaryURL": "",
                "WidthScale": 0.0,
                "CustomToken": {
                    "Thickness": 0.1,
                    "MergeDistancePixels": 15.0,
                    "Stackable": False
                }
            },
            'LuaScript': '',
            'LuaScriptState': '',
            "GUID": guid()
        }