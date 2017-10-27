from reader.color import ColorReader
from domain.token import Token
from domain.token import ContentToken
from reader.fromlist import read_fromlist
from reader.number import read_float

class TokenParser:
    @staticmethod
    def parse(sheet):
        tokens = []
        row = 1
        while row < sheet.nrows:
            try:
                entity = read_fromlist(sheet.cell(rowx=row, colx=1).value, ("cube", "triangle", "pawn", "token"))
            except ValueError as e:
                raise ValueError(str(e) + " (while checking " + str(sheet.cell(rowx=row, colx=0).value) + ")") from None

            if entity.lower() == 'token':
                token = TokenParser._parseToken(sheet, row)
            else:
                token = TokenParser._parseSimpleToken(sheet, row)

            tokens.append(token)
            row += 1
        return tokens

    @staticmethod
    def _parseSimpleToken(sheet, row):
        entity = sheet.cell(rowx=row, colx=1).value
        name = sheet.cell(rowx=row, colx=0).value
        color = ColorReader.read_color(sheet.cell(rowx=row, colx=2).value)
        try:
            size = read_float(sheet.cell(rowx=row, colx=3).value)
        except ValueError as e:
            raise ValueError(str(e) + " (while reading " + name + ")") from None
        return Token(name, entity, color, size)

    @staticmethod
    def _parseToken(sheet, row):
        entity = sheet.cell(rowx=row, colx=1).value
        name = sheet.cell(rowx=row, colx=0).value
        bg_color = ColorReader.read_color(sheet.cell(rowx=row, colx=2).value)
        text_color = ColorReader.read_color(sheet.cell(rowx=row, colx=4).value)
        content = sheet.cell(rowx=row, colx=5).value
        return ContentToken(name, entity, bg_color, text_color, content)
