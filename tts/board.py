from tts.guid import guid

class Board():
    def __init__(self, transform, object):
        self.transform = transform
        self.object = object

    def as_dict(self):
        return {
            "Name": "Custom_Board",
            "Transform": self.transform.as_dict(),
            "Nickname": "",
            "Description": "",
            "ColorDiffuse": {
                "r": 0.7867647,
                "g": 0.7867647,
                "b": 0.7867647
            },
            "Locked": True,
            "Grid": True,
            "Snap": True,
            "Autoraise": True,
            "Sticky": True,
            "Tooltip": True,
            "GridProjection": False,
            "Hands": False,
            "CustomImage": {
                "ImageURL": 'file:///' + self.object.imagePath,
                "ImageSecondaryURL": "",
                "WidthScale": 1.42857146
            },
            "LuaScript": "",
            "LuaScriptState": "",
            "GUID": guid()
        }
