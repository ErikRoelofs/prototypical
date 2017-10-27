from reader.color import ColorReader
from domain.die import Die
from reader.number import read_float

class DiceParser:
    def parse(sheet):
        dice = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            try:
                color = ColorReader.read_color(sheet.cell(rowx=row, colx=1).value)
                size = read_float(sheet.cell(rowx=row, colx=2).value)
            except ValueError as e:
                raise ValueError(str(e) + " (while reading " + name + ")") from None
            sides = sheet.cell(rowx=row, colx=3).value

            customContent = None
            if sheet.cell(rowx=row, colx=4).value:
                customContent = [
                    sheet.cell(rowx=row, colx=4).value,
                    sheet.cell(rowx=row, colx=5).value,
                    sheet.cell(rowx=row, colx=6).value,
                    sheet.cell(rowx=row, colx=7).value,
                    sheet.cell(rowx=row, colx=8).value,
                    sheet.cell(rowx=row, colx=9).value,
                ]

            try:
                dice.append(Die(name, color, size, sides, customContent))
            except ValueError as e:
                raise ValueError(str(e) + " (while reading " + name + ")") from None
            row += 1
        return dice