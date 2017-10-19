import json
from domain.blocksquare import BlockSquare
from domain.transform import Transform
import xlrd

# open save template
with open('template.json', 'r') as infile:
    data = json.load(infile)

# open excel file
workbook = xlrd.open_workbook('cubes.xls')
sheet = workbook.sheet_by_name('Cubes')

# read cube position/sizes
row = 1
while row < sheet.nrows:
    nameCell = sheet.cell(rowx=row, colx=0)
    x = sheet.cell(rowx=row, colx=1)
    y = sheet.cell(rowx=row, colx=2)
    z = sheet.cell(rowx=row, colx=3)
    scale = sheet.cell(rowx=row, colx=4)
    transform = Transform(x.value, y.value, z.value, 0, 0, 0, scale.value, scale.value, scale.value)
    data['ObjectStates'].append(BlockSquare(transform).as_dict())
    row += 1

with open('TS_Save_3.json', 'w') as outfile:
    json.dump(data, outfile)