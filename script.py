import json, xlrd

from sheetParser.tokenParser import TokenParser
from sheetParser.diceParser import DiceParser
from sheetParser.complexTypeParser import ComplexTypeParser
from sheetParser.complexObjectParser import ComplexObjectParser

from creator.entityCreator import EntityCreator

from tests.complexTypeParserTest import ComplexTypeParserTest

# setup pygame as drawing library
import pygame
pygame.init()

# run test cases
ComplexTypeParserTest().run()

# open save template
with open('template.json', 'r') as infile:
    data = json.load(infile)

# open excel file
workbook = xlrd.open_workbook('cubes.xls')

# collect entity libraries
tokens = TokenParser.parse(workbook.sheet_by_name('Tokens'))
dice = DiceParser.parse(workbook.sheet_by_name('Dice'))

complexTypes = ComplexTypeParser.parse(workbook.sheet_by_name('ComplexTypes'), workbook.sheet_by_name('Shapes'))
complexParser = ComplexObjectParser(complexTypes)
complexObjects = complexParser.parse(workbook.sheet_by_name('ComplexObjects'))

# build all required entities
creator = EntityCreator(tokens + dice + complexObjects)
entities = creator.createEntities(workbook.sheet_by_name('Placement'))


from drawer.ComplexObjectDrawer import ComplexObjectDrawer
drawer = ComplexObjectDrawer(complexObjects[0])
surf = drawer.draw()
pygame.image.save(surf, "test.jpg")


# add entities to save file
data["ObjectStates"] = entities

# save file
with open('TS_Save_3.json', 'w') as outfile:
    json.dump(data, outfile)