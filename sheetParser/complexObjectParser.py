from domain.complexObject import ComplexObject

class ComplexObjectParser:
    def __init__(self, types):
        self.types = types

    def parse(self, sheet):
        complexObjects = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            if name:
                type = self.findType(sheet.cell(rowx=row, colx=1).value)
                content = {}
                for column in type.shape.areas:
                    # headers...
                    if column < 1000:
                        content[column] = sheet.cell(rowx=row, colx=column).value
                    else:
                        content[column] = sheet.cell(rowx=0, colx=column-1000).value

                complexObjects.append(ComplexObject(name, type, content))
            row += 1
        return complexObjects

    def findType(self, name):
        for type in self.types:
            if type.name == name:
                return type
        raise ValueError("The ComplexType `" + str(name) + "` does not exist.") from None