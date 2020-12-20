from tts.guid import guid

class Die():
    def __init__(self, sides, color, transform, customContent = None, imagePath = None):
        self.sides = sides
        self.color = color
        self.transform = transform
        self.customContent = customContent
        self.imagePath = imagePath

    def as_dict(self):
        base = {
            "name": self.name(),
            'Transform': self.transform.as_dict(),
            'Nickname': '',
            'Description': '',
            'ColorDiffuse': {
                'r': self.color[0],
                'g': self.color[1],
                'b': self.color[2]
            },
            "Locked": False,
            "Grid": False,
            "Snap": False,
            "Autoraise": True,
            "Sticky": True,
            "Tooltip": True,
            "GridProjection": False,
            "Hands": False,
            "MaterialIndex": 0,
            "LuaScript": "",
            "LuaScriptState": "",
            "GUID": guid(),
            "RotationValues": self.getRotValues()
        }
        if self.customContent:
            base['CustomImage'] = self.customDice()

        return base

    def name(self):
        if self.customContent:
            return "Custom_Dice"
        return "Die_" + str(int(self.sides))

    def customDice(self):
        return {
            "ImageURL": self.imagePath,
            "ImageSecondaryURL": "",
            "WidthScale": 0.0,
            "CustomDice": {
                "Type": 1
            }
        }

    def getRotValues(self):
        if self.customContent:
            return self.getRotValuesCustom()
        if self.sides == 4:
            return self.getRotValues4()
        if self.sides == 6:
            return self.getRotValues6()
        if self.sides == 8:
            return self.getRotValues8()
        if self.sides == 12:
            return self.getRotValues12()
        if self.sides == 20:
            return self.getRotValues20()

    def getRotValuesCustom(self):
        return [
        {
          "Value": self.customContent[0],
          "Rotation": {
            "x": -90.0,
            "y": 0.0,
            "z": 0.0
          }
        },
        {
          "Value": self.customContent[1],
          "Rotation": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
          }
        },
        {
          "Value": self.customContent[2],
          "Rotation": {
            "x": 0.0,
            "y": 0.0,
            "z": -90.0
          }
        },
        {
          "Value": self.customContent[3],
          "Rotation": {
            "x": 0.0,
            "y": 0.0,
            "z": 90.0
          }
        },
        {
          "Value": self.customContent[4],
          "Rotation": {
            "x": 0.0,
            "y": 0.0,
            "z": -180.0
          }
        },
        {
          "Value": self.customContent[5],
          "Rotation": {
            "x": 90.0,
            "y": 0.0,
            "z": 0.0
          }
        }
      ]


    def getRotValues4(self):
        return [
            {
                "Value": 1,
                "Rotation": {
                    "x": 18.0,
                    "y": -241.0,
                    "z": -120.0
                }
            },
            {
                "Value": 2,
                "Rotation": {
                    "x": -90.0,
                    "y": -60.0,
                    "z": 0.0
                }
            },
            {
                "Value": 3,
                "Rotation": {
                    "x": 18.0,
                    "y": -121.0,
                    "z": 0.0
                }
            },
            {
                "Value": 4,
                "Rotation": {
                    "x": 18.0,
                    "y": 0.0,
                    "z": -240.0
                }
            }
        ]

    def getRotValues6(self):
        return [
        {
          "Value": 1,
          "Rotation": {
            "x": -90.0,
            "y": 0.0,
            "z": 0.0
          }
        },
        {
          "Value": 2,
          "Rotation": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
          }
        },
        {
          "Value": 3,
          "Rotation": {
            "x": 0.0,
            "y": 0.0,
            "z": -90.0
          }
        },
        {
          "Value": 4,
          "Rotation": {
            "x": 0.0,
            "y": 0.0,
            "z": 90.0
          }
        },
        {
          "Value": 5,
          "Rotation": {
            "x": 0.0,
            "y": 0.0,
            "z": -180.0
          }
        },
        {
          "Value": 6,
          "Rotation": {
            "x": 90.0,
            "y": 0.0,
            "z": 0.0
          }
        }
      ]

    def getRotValues8(self):
        return [
            {
                "Value": 1,
                "Rotation": {
                    "x": -33.0,
                    "y": 0.0,
                    "z": 90.0
                }
            },
            {
                "Value": 2,
                "Rotation": {
                    "x": -33.0,
                    "y": 0.0,
                    "z": 180.0
                }
            },
            {
                "Value": 3,
                "Rotation": {
                    "x": 33.0,
                    "y": 180.0,
                    "z": -180.0
                }
            },
            {
                "Value": 4,
                "Rotation": {
                    "x": 33.0,
                    "y": 180.0,
                    "z": 90.0
                }
            },
            {
                "Value": 5,
                "Rotation": {
                    "x": 33.0,
                    "y": 180.0,
                    "z": -90.0
                }
            },
            {
                "Value": 6,
                "Rotation": {
                    "x": 33.0,
                    "y": 180.0,
                    "z": 0.0
                }
            },
            {
                "Value": 7,
                "Rotation": {
                    "x": -33.0,
                    "y": 0.0,
                    "z": 0.0
                }
            },
            {
                "Value": 8,
                "Rotation": {
                    "x": -33.0,
                    "y": 0.0,
                    "z": -90.0
                }
            }
        ]

    def getRotValues10(self):
        return [
            {
                "Value": 1,
                "Rotation": {
                    "x": -38.0,
                    "y": 0.0,
                    "z": 234.0
                }
            },
            {
                "Value": 2,
                "Rotation": {
                    "x": 38.0,
                    "y": 180.0,
                    "z": -233.0
                }
            },
            {
                "Value": 3,
                "Rotation": {
                    "x": -38.0,
                    "y": 0.0,
                    "z": 20.0
                }
            },
            {
                "Value": 4,
                "Rotation": {
                    "x": 38.0,
                    "y": 180.0,
                    "z": -17.0
                }
            },
            {
                "Value": 5,
                "Rotation": {
                    "x": -38.0,
                    "y": 0.0,
                    "z": 90.0
                }
            },
            {
                "Value": 6,
                "Rotation": {
                    "x": 38.0,
                    "y": 180.0,
                    "z": -161.0
                }
            },
            {
                "Value": 7,
                "Rotation": {
                    "x": -38.0,
                    "y": 0.0,
                    "z": 307.0
                }
            },
            {
                "Value": 8,
                "Rotation": {
                    "x": 38.0,
                    "y": 180.0,
                    "z": -304.0
                }
            },
            {
                "Value": 9,
                "Rotation": {
                    "x": -38.0,
                    "y": 0.0,
                    "z": 163.0
                }
            },
            {
                "Value": 10,
                "Rotation": {
                    "x": 38.0,
                    "y": 180.0,
                    "z": -90.0
                }
            }
        ]

    def getRotValues12(self):
        return [
            {
                "Value": 1,
                "Rotation": {
                    "x": 27.0,
                    "y": 0.0,
                    "z": 72.0
                }
            },
            {
                "Value": 2,
                "Rotation": {
                    "x": 27.0,
                    "y": 0.0,
                    "z": 144.0
                }
            },
            {
                "Value": 3,
                "Rotation": {
                    "x": 27.0,
                    "y": 0.0,
                    "z": -72.0
                }
            },
            {
                "Value": 4,
                "Rotation": {
                    "x": -27.0,
                    "y": 180.0,
                    "z": 180.0
                }
            },
            {
                "Value": 5,
                "Rotation": {
                    "x": 90.0,
                    "y": 180.0,
                    "z": 0.0
                }
            },
            {
                "Value": 6,
                "Rotation": {
                    "x": 27.0,
                    "y": 0.0,
                    "z": -144.0
                }
            },
            {
                "Value": 7,
                "Rotation": {
                    "x": -27.0,
                    "y": 180.0,
                    "z": 36.0
                }
            },
            {
                "Value": 8,
                "Rotation": {
                    "x": -90.0,
                    "y": 180.0,
                    "z": 0.0
                }
            },
            {
                "Value": 9,
                "Rotation": {
                    "x": 27.0,
                    "y": 0.0,
                    "z": 0.0
                }
            },
            {
                "Value": 10,
                "Rotation": {
                    "x": -27.0,
                    "y": 180.0,
                    "z": 108.0
                }
            },
            {
                "Value": 11,
                "Rotation": {
                    "x": -27.0,
                    "y": 108.0,
                    "z": -36.0
                }
            },
            {
                "Value": 12,
                "Rotation": {
                    "x": -27.0,
                    "y": 36.0,
                    "z": -108.0
                }
            }
        ]

    def getRotValues20(self):
        return [
            {
                "Value": 1,
                "Rotation": {
                    "x": -11.0,
                    "y": 60.0,
                    "z": 17.0
                }
            },
            {
                "Value": 2,
                "Rotation": {
                    "x": 52.0,
                    "y": -60.0,
                    "z": -17.0
                }
            },
            {
                "Value": 3,
                "Rotation": {
                    "x": -11.0,
                    "y": -180.0,
                    "z": 90.0
                }
            },
            {
                "Value": 4,
                "Rotation": {
                    "x": -11.0,
                    "y": -180.0,
                    "z": 162.0
                }
            },
            {
                "Value": 5,
                "Rotation": {
                    "x": -11.0,
                    "y": -60.0,
                    "z": 234.0
                }
            },
            {
                "Value": 6,
                "Rotation": {
                    "x": -11.0,
                    "y": -180.0,
                    "z": 306.0
                }
            },
            {
                "Value": 7,
                "Rotation": {
                    "x": 52.0,
                    "y": -60.0,
                    "z": 55.0
                }
            },
            {
                "Value": 8,
                "Rotation": {
                    "x": 52.0,
                    "y": -60.0,
                    "z": 198.0
                }
            },
            {
                "Value": 9,
                "Rotation": {
                    "x": 52.0,
                    "y": -60.0,
                    "z": 127.0
                }
            },
            {
                "Value": 10,
                "Rotation": {
                    "x": 52.0,
                    "y": -180.0,
                    "z": -90.0
                }
            },
            {
                "Value": 11,
                "Rotation": {
                    "x": 308.0,
                    "y": 0.0,
                    "z": 90.0
                }
            },
            {
                "Value": 12,
                "Rotation": {
                    "x": 306.0,
                    "y": -240.0,
                    "z": -52.0
                }
            },
            {
                "Value": 13,
                "Rotation": {
                    "x": -52.0,
                    "y": -240.0,
                    "z": 18.0
                }
            },
            {
                "Value": 14,
                "Rotation": {
                    "x": 307.0,
                    "y": 120.0,
                    "z": 233.0
                }
            },
            {
                "Value": 15,
                "Rotation": {
                    "x": 11.0,
                    "y": 120.0,
                    "z": -234.0
                }
            },
            {
                "Value": 16,
                "Rotation": {
                    "x": 11.0,
                    "y": 0.0,
                    "z": 54.0
                }
            },
            {
                "Value": 17,
                "Rotation": {
                    "x": 11.0,
                    "y": -120.0,
                    "z": -17.0
                }
            },
            {
                "Value": 18,
                "Rotation": {
                    "x": 11.0,
                    "y": 0.0,
                    "z": -90.0
                }
            },
            {
                "Value": 19,
                "Rotation": {
                    "x": -52.0,
                    "y": -240.0,
                    "z": -198.0
                }
            },
            {
                "Value": 20,
                "Rotation": {
                    "x": 11.0,
                    "y": 0.0,
                    "z": -162.0
                }
            }
        ]
