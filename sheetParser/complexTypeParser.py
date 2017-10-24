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
                # make sure this isn't outside our left boundary
                ComplexTypeParser.validateAllowed(char, rowNum, colNum, areas)
                if char == '0':
                    continue
                if char in areas:
                    areas[char] = ComplexTypeParser.updateArea(areas[char], rowNum, colNum)
                else:
                    areas[char] = (rowNum, colNum, rowNum, colNum)
        return Shape(areas)

    # make sure we aren't intruding into some other char's position
    # make sure it's possible to extend here (we can only extend to the right on our first row, and only down after)
    # todo: make sure an area cannot be entirely inside another
    # todo: test cases!
    def validateAllowed(char, rowNum, colNum, areas):
        if char in areas:
            if areas[char][1] > colNum:
                raise ValueError("Malformed Shape: trying to extend " + char + " to the left, that means this shape is not a rectangle!")
            if colNum > areas[char][3] and areas[char][0] != areas[char][2]:
                raise ValueError("Malformed shape: trying to extend " + char + " to the right, but already on a second row. This shape is not a rectangle!")
            if areas[char][2]+1 < rowNum:
                raise ValueError("Malformed shape: trying to extend " + char + " down by two rows at once. This shape is not a rectangle!")
        for charKey, area in areas.items():
            if charKey != char:
                if rowNum == area[2] and area[1] < colNum < area[3]:
                    raise ValueError("Malformed shape: a " + char + " is inside an area already claimed by " + charKey + ". This shape is not a rectangle!")
        return True

    # will expand the size of this area to include the new cell (if required)
    def updateArea(current, rowNum, colNum):
        if rowNum > current[2]:
            current = (current[0], current[1], rowNum, current[3])
        if colNum > current[3]:
            current = (current[0], current[1], current[2], colNum)
        return current
