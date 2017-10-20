from domain.complexType import ComplexType
from domain.shape import Shape
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
                cols.append(shapeSheet.cell(rowx = row, colx = col).value)
            rows.append(cols)

        return ComplexTypeParser.constructShape(rows)

    # construct a shape from the given rows of chars
    def constructShape(rows):
        areas = {}
        for rowNum, row in enumerate(rows):
            for colNum, char in enumerate(row):
                ComplexTypeParser.validateAllowed(char, rowNum, colNum, areas)
                if char == '0':
                    continue
                if char in areas:
                    areas[char] = ComplexTypeParser.updateArea(areas[char], rowNum, colNum)
                else:
                    areas[char] = (rowNum, colNum, rowNum, colNum)
        return Shape(areas)

    # make sure that this position is not already claimed by a different char
    # make sure that this char does not already have a defined area that cannot contain this position
    def validateAllowed(char, rowNum, colNum, areas):
        return True

    # will expand the size of this area to include the new cell (if required)
    def updateArea(current, rowNum, colNum):
        if rowNum > current[2]:
            current = (current[0], current[1], rowNum, current[3])
        if colNum > current[3]:
            current = (current[0], current[1], current[2], colNum)
        return current
