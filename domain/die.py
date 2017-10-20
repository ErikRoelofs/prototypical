class Die():
    def __init__(self, name, color, size, sides):
        self.name = name
        self.color = color
        self.size = size
        self.sides = sides

        if sides not in (4,6,8,10,12,20):
            raise ValueError("This number of dice-sides is not supported.")