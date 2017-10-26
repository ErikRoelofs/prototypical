import xlrd

class ColorReader():

    colors = None

    @staticmethod
    def init():
        ColorReader.colors = {}
        workbook = xlrd.open_workbook('colors.xls')
        sheet = workbook.sheet_by_index(0)
        for i in range(0, sheet.nrows):
            colorName = sheet.cell(rowx=i, colx=0).value
            colorCode = sheet.cell(rowx=i, colx=1).value
            ColorReader.colors[colorName] = ColorReader.codeToRGB(colorCode)

    @staticmethod
    def codeToRGB(code):
        r = float(int(code[1:3],16)) / 255
        g = float(int(code[3:5],16)) / 255
        b = float(int(code[5:7],16)) / 255
        return(r,g,b)

    @staticmethod
    def read_color(value):
        if not ColorReader.colors:
            ColorReader.init()

        if value[0] == '#':
            return ColorReader.read_color_by_code(value)
        else:
            return ColorReader.read_color_by_name(value)

    @staticmethod
    def read_color_by_name(value):
        return ColorReader.colors[value.lower()]

    @staticmethod
    def read_color_by_code(value):
        return ColorReader.codeToRGB(value)