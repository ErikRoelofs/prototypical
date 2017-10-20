import json, xlrd

from sheetParser.tokenParser import TokenParser
from sheetParser.diceParser import DiceParser

from creator.entityCreator import EntityCreator


# open save template
with open('template.json', 'r') as infile:
    data = json.load(infile)

# open excel file
workbook = xlrd.open_workbook('cubes.xls')

# collect entity libraries
tokens = TokenParser.parse(workbook.sheet_by_name('Tokens'))
dice = DiceParser.parse(workbook.sheet_by_name('Dice'))

# build all required entities
creator = EntityCreator(tokens + dice)
entities = creator.createEntities(workbook.sheet_by_name('Placement'))

# add entities to save file
data["ObjectStates"] = entities

# save file
with open('TS_Save_3.json', 'w') as outfile:
    json.dump(data, outfile)