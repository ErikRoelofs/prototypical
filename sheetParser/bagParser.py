from domain.bag import Bag, InfiniteBag

from reader.fromlist import read_fromlist
from reader.color import ColorReader
from reader.number import read_float
from reader.content import read_content

class BagParser:
    def __init__(self, types):
        self.types = types

    def parse(self, sheet):
        bags = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            type = read_fromlist(sheet.cell(rowx=row, colx=1).value, ('bag', 'infinite-bag'))
            color = ColorReader.read_color(sheet.cell(rowx=row, colx=2).value)
            size = read_float(sheet.cell(rowx=row, colx=3).value)

            bag = Bag(name, size, color) if type == 'bag' else InfiniteBag(name, size, color)
            contentNum = 0
            while contentNum < (sheet.ncols - 4):
                content = read_content(sheet.cell(rowx=row, colx=contentNum+4).value)
                for key, item in enumerate(content):
                    bag.addContent(item[0], self.findType(item[1]))
                contentNum += 1

            bags.append(bag)
            row += 1
        return bags

    def findType(self, name):
        for type in self.types:
            if type.name == name:
                return type
        raise ValueError("Unknown bag content: `" + str(name) + "`.") from None