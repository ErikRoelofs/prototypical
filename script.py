XMIN = -27
XMAX = 27
ZMIN = -17
ZMAX = 17
YHEIGHT = 1.5

import json, random, xlrd
from tts.blocksquare import BlockSquare
from tts.transform import Transform
from domain.token import Token
from reader.color import read_color

def findTokenByName(name):
    for token in tokens:
        if token.name == name:
            return token

def placeEntity(coords,entity):
    transform = Transform(coords[0], YHEIGHT, coords[1], 0, 0, 0, entity.size, entity.size, entity.size)
    bs = BlockSquare(transform, entity.color)
    data["ObjectStates"].append(bs.as_dict())

def getCoordInChunk(chunkX, chunkY, numXChunks, numYChunks):
    width = (XMAX - XMIN) / numXChunks
    height = (ZMAX - ZMIN) / numYChunks
    xOffset = random.uniform(0, width)
    yOffset = random.uniform(0, height)
    return ( xOffset + XMIN + (chunkX * width), yOffset + ZMIN + (chunkY * height))



# open save template
with open('template.json', 'r') as infile:
    data = json.load(infile)

# open excel file
workbook = xlrd.open_workbook('cubes.xls')
sheet = workbook.sheet_by_name('Tokens')

# read token types
tokens = []
row = 1
while row < sheet.nrows:
    name = sheet.cell(rowx=row, colx=0).value
    entity = sheet.cell(rowx=row, colx=1).value
    color = read_color(sheet.cell(rowx=row, colx=2).value)
    size = sheet.cell(rowx=row, colx=3).value
    tokens.append(Token(name, entity, color, size))
    row += 1

# read number of chunks
placementSheet = workbook.sheet_by_name('Placement')
chunksWide = placementSheet.cell(rowx=0, colx=1).value
chunksHigh = placementSheet.cell(rowx=0, colx=2).value

row = 1
while row < placementSheet.nrows:
    xChunk = placementSheet.cell(rowx=row, colx=0).value
    yChunk = placementSheet.cell(rowx=row, colx=1).value
    col = 2
    while col < placementSheet.ncols and col < 10:
        numToPlace = placementSheet.cell(rowx=row, colx=col).value
        if numToPlace:
            typeToPlace = placementSheet.cell(rowx=row, colx=col+1).value
            token = findTokenByName(typeToPlace)
            for i in range(0,int(numToPlace)):
                placeEntity(getCoordInChunk(xChunk, yChunk, chunksWide, chunksHigh), token)
        col += 2
    row += 1

with open('TS_Save_3.json', 'w') as outfile:
    json.dump(data, outfile)