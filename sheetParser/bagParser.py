from domain.bag import Bag, InfiniteBag

from reader.fromlist import read_fromlist

class BagParser:
    def __init__(self, types):
        self.types = types

    def parse(self, sheet):
        bags = []
        row = 1
        while row < sheet.nrows:
            name = sheet.cell(rowx=row, colx=0).value
            type = read_fromlist(sheet.cell(rowx=row, colx=1).value, ('bag', 'infinite-bag'))
            bag = Bag(name) if type == 'bag' else InfiniteBag(name)
            contentNum = 0
            while contentNum < (sheet.ncols - 4):
                contentValue = sheet.cell(rowx=row, colx=contentNum+4).value
                if contentValue:
                    bag.addContent(1, self.findType(contentValue))
                contentNum += 1

            bags.append(bag)
            row += 1
        return bags

    def findType(self, name):
        for type in self.types:
            if type.name == name:
                return type
        raise ValueError("Unknown bag content: `" + str(name) + "`.") from None