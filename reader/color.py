import xlrd

class ColorReader():

    colors = None

    @staticmethod
    def init():
        ColorReader.colors = {}
        workbook = xlrd.open_workbook('data/colors.xls')
        sheet = workbook.sheet_by_index(0)
        for i in range(0, sheet.nrows):
            colorName = sheet.cell(rowx=i, colx=0).value
            colorCode = sheet.cell(rowx=i, colx=1).value
            ColorReader.colors[colorName] = ColorReader.codeToRGB(colorCode)

    @staticmethod
    def codeToRGB(code):
        try:
            r = float(int(code[1:3],16)) / 255
            g = float(int(code[3:5],16)) / 255
            b = float(int(code[5:7],16)) / 255
            return(r,g,b)
        except ValueError as e:
            raise ValueError("Unable to read hex-based color: " + code)

    @staticmethod
    def read_color(value):
        if not ColorReader.colors:
            ColorReader.init()

        if value[0] == '#':
            return ColorReader.read_color_by_code(value)
        elif value[0] == '\\':
            return value  # this is an image or icon
        else:
            return ColorReader.read_color_by_name(value)

    @staticmethod
    def read_color_by_name(value):
        try:
            return ColorReader.colors[value.lower()]
        except KeyError:
            raise ValueError("Unknown color requested: " + value)

    @staticmethod
    def read_color_by_code(value):
        return ColorReader.codeToRGB(value)