XMIN = -27
XMAX = 27
ZMIN = -17
ZMAX = 17
YHEIGHT = 1.5

import json, random, xlrd,sys
from tts.blocksquare import BlockSquare
from tts.transform import Transform
from tts.die import Die as TTSDie

from domain.token import Token
from domain.die import Die
from sheetParser.tokenParser import TokenParser
from sheetParser.diceParser import DiceParser

def findObjectByName(name):
    maybe = findTokenByName(name)
    if maybe:
        return maybe
    maybe = findDieByName(name)
    if maybe:
        return maybe

def findTokenByName(name):
    for token in tokens:
        if token.name == name:
            return token

def findDieByName(name):
    for die in dice:
        if die.name == name:
            return die

def placeEntity(coords,entity):
    if isinstance(entity, Token):
        placeToken(coords, entity)
    if isinstance(entity, Die):
        placeDie(coords, entity)

def placeToken(coords,entity):
    transform = Transform(coords[0], YHEIGHT, coords[1], 0, 0, 0, entity.size, entity.size, entity.size)
    bs = BlockSquare(transform, entity.color)
    data["ObjectStates"].append(bs.as_dict())

def placeDie(coords,entity):
    transform = Transform(coords[0], YHEIGHT, coords[1], 0, 0, 0, entity.size, entity.size, entity.size)
    die = TTSDie(entity.sides, entity.color, transform)
    data["ObjectStates"].append(die.as_dict())

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

tokens = TokenParser.parse(workbook.sheet_by_name('Tokens'))
dice = DiceParser.parse(workbook.sheet_by_name('Dice'))

# read item locations
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
            token = findObjectByName(typeToPlace)
            for i in range(0,int(numToPlace)):
                placeEntity(getCoordInChunk(xChunk, yChunk, chunksWide, chunksHigh), token)
        col += 2
    row += 1

with open('TS_Save_3.json', 'w') as outfile:
    json.dump(data, outfile)