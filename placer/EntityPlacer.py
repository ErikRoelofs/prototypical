import random

XMIN = -27
XMAX = 27
ZMIN = -17
ZMAX = 17
YHEIGHT = 1.5


class EntityPlacer:
    def __init__(self, library):
        self.library = library

    def getCoordInChunk(chunkX, chunkY, numXChunks, numYChunks):
        width = (XMAX - XMIN) / numXChunks
        height = (ZMAX - ZMIN) / numYChunks
        xOffset = random.uniform(0, width)
        yOffset = random.uniform(0, height)
        return (xOffset + XMIN + (chunkX * width), yOffset + ZMIN + (chunkY * height))

    def findObjectByName(self, name):
        for type in self.library:
            if type.name == name:
                return type

    def createEntity(self, entity, location):

    def createEntities(self, sheet):
        chunksWide = sheet.cell(rowx=0, colx=1).value
        chunksHigh = sheet.cell(rowx=0, colx=2).value

        row = 1
        while row < sheet.nrows:
            xChunk = sheet.cell(rowx=row, colx=0).value
            yChunk = sheet.cell(rowx=row, colx=1).value
            col = 2
            while col < sheet.ncols and col < 10:
                numToPlace = sheet.cell(rowx=row, colx=col).value
                if numToPlace:
                    typeToPlace = sheet.cell(rowx=row, colx=col + 1).value
                    object = self.findObjectByName(typeToPlace)
                    for i in range(0, int(numToPlace)):
                        self.createEntity(self.getCoordInChunk(xChunk, yChunk, chunksWide, chunksHigh), object)
                col += 2
            row += 1
