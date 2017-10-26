from reader.color import ColorReader
from domain.token import Token
from domain.token import ContentToken


class TokenParser:
    @staticmethod
    def parse(sheet):
        tokens = []
        row = 1
        while row < sheet.nrows:
            entity = sheet.cell(rowx=row, colx=1).value
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
        size = sheet.cell(rowx=row, colx=3).value
        return Token(name, entity, color, size)

    @staticmethod
    def _parseToken(sheet, row):
        entity = sheet.cell(rowx=row, colx=1).value
        name = sheet.cell(rowx=row, colx=0).value
        bg_color = ColorReader.read_color(sheet.cell(rowx=row, colx=2).value)
        text_color = ColorReader.read_color(sheet.cell(rowx=row, colx=4).value)
        content = sheet.cell(rowx=row, colx=5).value
        return ContentToken(name, entity, bg_color, text_color, content)
