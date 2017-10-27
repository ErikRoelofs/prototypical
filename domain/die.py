class Die():
    def __init__(self, name, color, size, sides, customContent = None, imagePath = None):
        self.name = name
        self.color = color
        self.size = size
        self.sides = sides
        self.customContent = customContent
        self.imagePath = imagePath

        if customContent and sides != 6:
            raise ValueError("Only 6 sided dice support custom content at this time.")

        if sides not in (4,6,8,10,12,20):
            raise ValueError("This number of dice-sides is not supported.")

    def setImagePath(self, path):
        self.imagePath = path