from reader.color import read_color
from domain.die import Die


class DiceParser:
    def parse(sheet):
        dice = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            color = read_color(sheet.cell(rowx=row, colx=1).value)
            size = sheet.cell(rowx=row, colx=2).value
            sides = sheet.cell(rowx=row, colx=3).value
            dice.append(Die(name, color, size, sides))
            row += 1
        return dice