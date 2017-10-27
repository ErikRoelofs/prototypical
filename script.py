import json, xlrd

from sheetParser.tokenParser import TokenParser
from sheetParser.diceParser import DiceParser
from sheetParser.complexTypeParser import ComplexTypeParser
from sheetParser.complexObjectParser import ComplexObjectParser
from sheetParser.deckParser import DeckParser

from drawer.deckDrawer import DeckDrawer
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.cardBackDrawer import CardBackDrawer
from drawer.tokenDrawer import TokenDrawer
from drawer.diceDrawer import DiceDrawer

from creator.entityCreator import EntityCreator

from tests.complexTypeParserTest import ComplexTypeParserTest

from domain.token import ContentToken

def runTests():
    # run test cases
    ComplexTypeParserTest().run()


def buildFile(excelFile, imagesDir, saveDir, fileName, progressCallback):

    # setup pygame as drawing library
    import pygame
    pygame.init()

    # open save template
    with open('template.json', 'r') as infile:
        data = json.load(infile)
        data['SaveName'] = fileName

    # open excel file
    progressCallback("Reading excel file: " + excelFile)
    workbook = xlrd.open_workbook(excelFile)

    # collect entity libraries
    progressCallback("Reading tokens... ", False)
    tokens = TokenParser.parse(workbook.sheet_by_name('Tokens'))
    progressCallback(str(len(tokens)) + " token succesfully extracted.")

    progressCallback("Reading dice... ", False)
    dice = DiceParser.parse(workbook.sheet_by_name('Dice'))
    progressCallback(str(len(dice)) + " dice succesfully extracted.")

    progressCallback("Reading complex types... ", False)
    complexTypes = ComplexTypeParser.parse(workbook.sheet_by_name('ComplexTypes'), workbook.sheet_by_name('Shapes'))
    progressCallback(str(len(complexTypes)) + " types succesfully extracted.")

    progressCallback("Reading complex objects... ", False)
    complexParser = ComplexObjectParser(complexTypes)
    complexObjects = complexParser.parse(workbook.sheet_by_name('ComplexObjects'))
    progressCallback(str(len(complexObjects)) + " complex objects succesfully extracted.")

    progressCallback("Reading decks... ", False)
    decks = DeckParser.parse(workbook.sheet_by_name('Decks'), complexObjects)
    progressCallback(str(len(decks)) + " decks succesfully extracted.")

    progressCallback("Drawing all custom content.")

    # draw all the card decks
    progressCallback("Drawing decks... ", False)
    drawer = DeckDrawer()
    for deck in decks:
        path = imagesDir + '/' + deck.name + ".jpg"
        pygame.image.save(drawer.draw(deck), path )
        deck.setImagePath( path )

    # draw all the deck backs
    drawer = CardBackDrawer()
    for deck in decks:
        path = imagesDir + '/' + deck.name + "_back.jpg"
        pygame.image.save(drawer.draw(deck), path)
        deck.setBackImagePath(path)
    progressCallback(str(len(decks)) + " decks succesfully drawn.")

    # draw all the boards
    progressCallback("Drawing boards... ", False)
    done = 0
    for obj in complexObjects:
        if obj.type.type == 'board':
            path = imagesDir + '/' + obj.name + ".jpg"
            drawer = ComplexObjectDrawer(obj)
            pygame.image.save(drawer.draw(), path )
            obj.setImagePath(path)
            done+=1
    progressCallback(str(done) + " boards succesfully drawn.")

    # draw all the (custom) tokens
    progressCallback("Drawing tokens... ", False)
    done = 0
    for token in tokens:
        if isinstance(token, ContentToken):
            path = imagesDir + '/token_' + token.name + ".jpg"
            drawer = TokenDrawer(token)
            pygame.image.save(drawer.draw(), path)
            token.setImagePath(path)
            done += 1
    progressCallback(str(done) + " custom tokens succesfully drawn.")

    # draw all dice
    progressCallback("Drawing dice... ", False)
    done = 0
    for die in dice:
        if die.customContent:
            path = imagesDir + '/die_' + die.name + ".png"
            drawer = DiceDrawer(die)
            pygame.image.save(drawer.draw(), path)
            die.setImagePath(path)
            done += 1
    progressCallback(str(done) + " dice succesfully drawn.")

    progressCallback("Placing all entities on the tabletop.")
    # build all required entities
    creator = EntityCreator(tokens + dice + complexObjects + decks)
    entities = creator.createEntities(workbook.sheet_by_name('Placement'))
    progressCallback("All entities have been placed.")

    # add entities to save file
    data["ObjectStates"] = entities

    # save file
    path = saveDir + '/TS_' + fileName.replace(' ', '_') + '.json'
    progressCallback("Saving file to " + path)
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import font

class Config:
    def __init__(self, excelFile, saveDir, imagesDir, fileName):
        self.excelFile = excelFile
        self.saveDir = saveDir
        self.imagesDir = imagesDir
        self.fileName = fileName
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

    def setFilename(self):
        self.fileName.set(simpledialog.askstring("Filename?", "Enter the filename:"))
        self.saveConfig()

    def readyToRun(self):
        return self.excelFile.get() and self.saveDir.get() and self.imagesDir.get() and self.fileName.get()

    def loadConfig(self):
        try:
            with open('settings.json', 'r') as infile:
                data = json.load(infile)
                self.excelFile.set(data['e'])
                self.saveDir.set(data['s'])
                self.imagesDir.set(data['i'])
                self.fileName.set(data['f'])
        except FileNotFoundError:
            return

    def saveConfig(self):
        data = {
            "e": self.excelFile.get(),
            "s": self.saveDir.get(),
            "i": self.imagesDir.get(),
            "f": self.fileName.get()
        }
        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile)


class App:
    def __init__(self, master):
        self.master = master
        master.geometry("700x600")
        self.filenameVar = StringVar()
        self.config = Config(StringVar(), StringVar(), StringVar(), self.filenameVar)

        frame = Frame(master)
        frame.grid()
        frame.grid_columnconfigure(1, minsize=400)

        self.customFont = font.Font(family="Arial", size=18)
        self.headerLabel = Label(frame, text="Prototypical!", font=self.customFont)
        self.headerLabel.grid(row=0, column=0, columnspan=2)

        self.excelFile(frame)
        self.savedirFile(frame)
        self.imagedirFile(frame)
        self.filename(frame)

        buttonFrame = Frame(frame)
        buttonFrame.grid(row=5, column=1)

        self.buildButton= Button(buttonFrame, text="BUILD", command=self.build)
        self.buildButton.grid(row=0, column=0)

        self.button = Button(buttonFrame, text="QUIT", command=frame.quit)
        self.button.grid(row=0, column=1)

        self.statusLabel = Label(frame, text="Status:")
        self.statusLabel.grid(row=6, column=0, columnspan=2)

        self.status = Text(frame)
        self.status.grid(row=7, column=0, columnspan=2)
        self.status.tag_configure("error", foreground="red", underline=True)

    def excelFile(self, frame):
        self.excelButton = Button(frame, text="SET EXCEL FILE", command=self.config.setExcelFile, width=30)
        self.excelButton.grid(row=1, column=0)

        self.excelText = Label(frame, textvariable=self.config.excelFile)
        self.excelText.grid(row=1, column=1)

    def savedirFile(self, frame):
        self.savedirButton = Button(frame, text="SET SAVE DIR", command=self.config.setSaveDir, width=30)
        self.savedirButton.grid(row=2, column=0)

        self.savedirText = Label(frame, textvariable=self.config.saveDir)
        self.savedirText.grid(row=2, column=1)

    def imagedirFile(self, frame):
        self.imagedirButton = Button(frame, text="SET IMAGEDIR FILE", command=self.config.setImagesDir, width=30)
        self.imagedirButton.grid(row=3, column=0)

        self.imagedirText = Label(frame, textvariable=self.config.imagesDir)
        self.imagedirText.grid(row=3, column=1)

    def filename(self, frame):
        self.filenameButton = Button(frame, text="SET FILENAME", command=self.config.setFilename, width=30)
        self.filenameButton.grid(row=4, column=0)

        self.filenameText = Label(frame, textvariable=self.config.fileName)
        self.filenameText.grid(row=4, column=1)

    def build(self):
        if self.config.readyToRun():
            self.flushStatus()
            self.pushStatusMessage("Going to build!")
            try:
                buildFile(self.config.excelFile.get(), self.config.imagesDir.get(), self.config.saveDir.get(), self.config.fileName.get(), self.pushStatusMessage)
                self.pushStatusMessage("Done building!")
            except BaseException as e:
                self.pushErrorMessage(e)
                raise e

    def pushErrorMessage(self, e):
        self.pushStatusMessage("\n")
        index = self.status.index(INSERT)
        curline = index.split('.')[0]
        self.pushStatusMessage("\nUh oh, there was a problem while building:")
        self.status.tag_add("error", str(int(curline) + 1) + ".0", str(int(curline) + 2) + ".0")
        self.pushStatusMessage(str(e))

    def pushStatusMessage(self, msg, newline=True):
        self.status.insert(END, msg + ("\n" if newline else ''))
        self.master.update()

    def flushStatus(self):
        self.status.delete(1.0, END)

root = Tk()
app = App(root)
root.mainloop()