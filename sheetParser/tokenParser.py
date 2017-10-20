from reader.color import read_color
from domain.token import Token


class TokenParser:
    def parse(sheet):
        tokens = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            entity = sheet.cell(rowx=row, colx=1).value
            color = read_color(sheet.cell(rowx=row, colx=2).value)
            size = sheet.cell(rowx=row, colx=3).value
            tokens.append(Token(name, entity, color, size))
            row += 1
        return tokens