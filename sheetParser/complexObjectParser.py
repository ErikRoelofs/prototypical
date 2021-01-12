from domain.complexObject import ComplexObject

class ComplexObjectParser:
    def __init__(self, types):
        self.types = types
        self.templateHeaders = {}

    def parse(self, sheet):
        complexObjects = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            typeName = sheet.cell(rowx=row, colx=1).value
            if name or typeName:
                isTemplate = self.isTemplate(typeName)
                if isTemplate:
                  type = self.findType(typeName)
                  content = {}
                  for column in type.shape.areas:
                    if column < 1000:
                      pass
                    else:
                      content[column] = sheet.cell(rowx=row, colx=column-1000).value
                  self.templateHeaders[type.name] = content
                else:
                    type = self.findType(typeName)
                    content = {}
                    for column in type.shape.areas:
                        # headers...
                        if column < 1000:
                            content[column] = sheet.cell(rowx=row, colx=column).value
                        else:
                            try:
                              content[column] = self.templateHeaders[type.name][column]
                            except KeyError as e:
                              raise ValueError(type.name + " contains headers, but no template was defined for it.")
                    complexObjects.append(ComplexObject(name, type, content))
            row += 1
        return complexObjects

    def isTemplate(self, type):
        return type[0] == '\\'

    def findType(self, name):
        # handle the template column
        if name[0] == '\\':
            name = name[1:]

        for type in self.types:
            if type.name == name:
                return type
        raise ValueError("The ComplexType `" + str(name) + "` does not exist.") from None