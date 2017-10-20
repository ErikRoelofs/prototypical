from domain.complexType import ComplexType
from reader.color import read_color
from reader.cell import read_cell

class ComplexTypeParser:
    def parse(sheet, shapeSheet):
        complexTypes = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            size = sheet.cell(rowx=row, colx=1).value

            topLeft = read_cell(sheet.cell(rowx=row, colx=2).value)
            bottomRight = read_cell(sheet.cell(rowx=row, colx=3).value)

            shape = ComplexTypeParser.parseShape(shapeSheet, topLeft, bottomRight)

            bgColor = read_color(sheet.cell(rowx=row, colx=4).value)
            backside = read_color(sheet.cell(rowx=row, colx=5).value)
            complexTypes.append(ComplexType(name, size, shape, bgColor, backside))
            row += 1
        return complexTypes

    def parseShape(shapeSheet, topLeft, bottomRight):
        firstRow = topLeft[0]
        firstCol = topLeft[1]
        lastRow = bottomRight[0]
        lastCol = bottomRight[1]

        rows = []
        for row in range(firstRow, lastRow + 1):
            cols = []
            for col in range(firstCol, lastCol + 1):
                cols.append(shapeSheet.cell(rowx = row, colx = col))
            rows.append(cols)

        return rows