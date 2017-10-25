import json, xlrd

from sheetParser.tokenParser import TokenParser
from sheetParser.diceParser import DiceParser
from sheetParser.complexTypeParser import ComplexTypeParser
from sheetParser.complexObjectParser import ComplexObjectParser
from sheetParser.deckParser import DeckParser

from drawer.deckDrawer import DeckDrawer
from drawer.complexObjectDrawer import ComplexObjectDrawer

from creator.entityCreator import EntityCreator

from tests.complexTypeParserTest import ComplexTypeParserTest

def runTests():
    # run test cases
    ComplexTypeParserTest().run()


def buildFile(excelFile, imagesDir, saveDir):
    # setup pygame as drawing library
    import pygame
    pygame.init()

    # open save template
    with open('template.json', 'r') as infile:
        data = json.load(infile)

    # open excel file
    workbook = xlrd.open_workbook(excelFile)

    # collect entity libraries
    tokens = TokenParser.parse(workbook.sheet_by_name('Tokens'))
    dice = DiceParser.parse(workbook.sheet_by_name('Dice'))

    complexTypes = ComplexTypeParser.parse(workbook.sheet_by_name('ComplexTypes'), workbook.sheet_by_name('Shapes'))
    complexParser = ComplexObjectParser(complexTypes)
    complexObjects = complexParser.parse(workbook.sheet_by_name('ComplexObjects'))
    decks = DeckParser.parse(workbook.sheet_by_name('Decks'), complexObjects)

    # draw all the card decks
    drawer = DeckDrawer()
    for deck in decks:
        pygame.image.save(drawer.draw(deck), deck.name + ".jpg")

    # draw all the boards
    for obj in complexObjects:
        if obj.type.type == 'board':
            drawer = ComplexObjectDrawer(obj)
            pygame.image.save(drawer.draw(), obj.name + ".jpg")

    # build all required entities
    creator = EntityCreator(tokens + dice + complexObjects + decks)
    entities = creator.createEntities(workbook.sheet_by_name('Placement'))

    # add entities to save file
    data["ObjectStates"] = entities

    # save file
    with open(saveDir + '/TS_Save_3.json', 'w') as outfile:
        json.dump(data, outfile)


from tkinter import *
from tkinter import filedialog

class Config:
    def __init__(self, excelFile, saveDir, imagesDir):
        self.excelFile = excelFile
        self.saveDir = saveDir
        self.imagesDir = imagesDir
        self.loadConfig()

    def setExcelFile(self):
        self.excelFile.set(filedialog.askopenfilename(initialdir='~'))
        self.saveConfig()

    def setSaveDir(self):
        self.saveDir.set(filedialog.askdirectory (initialdir='~'))
        self.saveConfig()

    def setImagesDir(self):
        self.imagesDir.set(filedialog.askdirectory (initialdir='~'))
        self.saveConfig()

    def readyToRun(self):
        return self.excelFile and self.saveDir and self.imagesDir

    def loadConfig(self):
        try:
            with open('settings.json', 'r') as infile:
                data = json.load(infile)
                self.excelFile.set(data['e'])
                self.saveDir.set(data['s'])
                self.imagesDir.set(data['i'])
        except FileNotFoundError:
            return

    def saveConfig(self):
        data = {
            "e": self.excelFile.get(),
            "s": self.saveDir.get(),
            "i": self.imagesDir.get()
        }
        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile)


class App:
    def __init__(self, master):
        master.geometry("600x200")
        self.config = Config(StringVar(), StringVar(), StringVar())

        frame = Frame(master)
        frame.grid()
        frame.grid_columnconfigure(1, minsize=400)

        self.button = Button(frame, text="QUIT", command=frame.quit)
        self.button.grid(row=0, column=0, columnspan=2)

        self.excelFile(frame)
        self.savedirFile(frame)
        self.imagedirFile(frame)

        self.buildButton= Button(frame, text="BUILD", command=self.build)
        self.buildButton.grid(row=4, column=0, columnspan=2)

    def excelFile(self, frame):
        self.excelButton = Button(frame, text="SET EXCEL FILE", command=self.config.setExcelFile)
        self.excelButton.grid(row=1, column=0)

        self.excelText = Label(frame, textvariable=self.config.excelFile)
        self.excelText.grid(row=1, column=1)

    def savedirFile(self, frame):
        self.savedirButton = Button(frame, text="SET SAVE DIR", command=self.config.setSaveDir)
        self.savedirButton.grid(row=2, column=0)

        self.savedirText = Label(frame, textvariable=self.config.saveDir)
        self.savedirText.grid(row=2, column=1)

    def imagedirFile(self, frame):
        self.imagedirButton = Button(frame, text="SET IMAGEDIR FILE", command=self.config.setImagesDir)
        self.imagedirButton.grid(row=3, column=0)

        self.imagedirText = Label(frame, textvariable=self.config.imagesDir)
        self.imagedirText.grid(row=3, column=1)

    def build(self):
        if self.config.readyToRun():
            buildFile(self.config.excelFile.get(), self.config.imagesDir.get(), self.config.saveDir.get())


root = Tk()
app = App(root)
root.mainloop()