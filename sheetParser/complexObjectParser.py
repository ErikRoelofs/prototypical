from domain.complexObject import ComplexObject

class ComplexObjectParser:
    def __init__(self, types):
        self.types = types

    def parse(self, sheet):
        complexObjects = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            type = self.findType(sheet.cell(rowx=row, colx=1).value)
            content = []
            col = 2
            while col < sheet.ncols:
                content.append(sheet.cell(rowx=row, colx=col).value)
                col += 1

            complexObjects.append(ComplexObject(name, type, content))
            row += 1
        return complexObjects

    def findType(self, name):
        for type in self.types:
            if type.name == name:
                return type
        raise ValueError("The ComplexType `" + name + "` does not exist.") from None