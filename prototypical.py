import json
import xlrd

from creator.entityCreator import EntityCreator
from domain.token import ContentToken
from drawer.cardBackDrawer import CardBackDrawer
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.deckDrawer import DeckDrawer
from drawer.diceDrawer import DiceDrawer
from drawer.tokenDrawer import TokenDrawer
from sheetParser.complexObjectParser import ComplexObjectParser
from sheetParser.complexTypeParser import ComplexTypeParser
from sheetParser.deckParser import DeckParser
from sheetParser.diceParser import DiceParser
from sheetParser.bagParser import BagParser
from sheetParser.tokenParser import TokenParser
from domain.library import Library

import os, sys, pysftp
from shutil import copyfile

def tryAndFindSaveGamesFolder():
    if sys.platform != 'win32':
        return None

    try:
        import win32com.client
    except ImportError:
        return None

    objShell = win32com.client.Dispatch("WScript.Shell")
    docs = objShell.SpecialFolders("MyDocuments") + "\My Games\Tabletop Simulator\Saves"

    if os.path.isdir(docs):
        return docs

    return None

def parseFile(excelFile, progressCallback):
    # open excel file
    progressCallback("Reading spreadsheet: " + excelFile)
    workbook = xlrd.open_workbook(excelFile)

    # collect entity libraries
    progressCallback("Reading tokens... ", False)
    tokens = TokenParser.parse(workbook.sheet_by_name('Tokens'))
    progressCallback(str(len(tokens)) + " tokens succesfully extracted.")

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

    progressCallback("Reading bags... ", False)
    bagParser = BagParser(tokens + dice + complexObjects + decks)
    bags = bagParser.parse(workbook.sheet_by_name('Containers'))
    progressCallback(str(len(bags)) + " bags succesfully extracted.")

    # UGLY - we have to redo this step later because we set the image paths after drawing and these entities won't work
    progressCallback("Reading table content... ", False)
    creator = EntityCreator(tokens + dice + complexObjects + decks + bags)
    entities = creator.createEntities(workbook.sheet_by_name('Placement'))
    progressCallback("Read " + str(len(entities)) + " items to be placed.", True)

    return Library(tokens, dice, complexObjects, decks, bags)

def buildFile(excelFile, imageBuilder, saveDir, fileName, progressCallback):
    # setup pygame as drawing library
    import pygame
    pygame.init()

    # open save template
    with open('data/template.json', 'r') as infile:
        data = json.load(infile)
        data['SaveName'] = fileName

    # parse here
    library = parseFile(excelFile, progressCallback)

    progressCallback("Drawing all custom content.")

    # draw all the card decks
    progressCallback("Drawing decks... ", False)
    drawer = DeckDrawer()
    for deck in library.decks:
        path = imageBuilder.build(drawer.draw(deck), deck.name, "jpg")
        deck.setImagePath(path)

    # draw all the deck backs
    drawer = CardBackDrawer()
    for deck in library.decks:
        path = imageBuilder.build(drawer.draw(deck), deck.name + "_back", "jpg")
        deck.setBackImagePath(path)
    progressCallback(str(len(library.decks)) + " decks succesfully drawn.")

    # draw all the boards
    progressCallback("Drawing boards... ", False)
    done = 0
    for obj in library.complexObjects:
        if obj.type.type == 'board':
            drawer = ComplexObjectDrawer(obj)
            path = imageBuilder.build(drawer.draw(), obj.name, "jpg")
            obj.setImagePath(path)
            done += 1
    progressCallback(str(done) + " boards succesfully drawn.")

    # draw all the (custom) tokens
    progressCallback("Drawing tokens... ", False)
    done = 0
    for token in library.tokens:
        if isinstance(token, ContentToken):
            drawer = TokenDrawer(token)
            path = imageBuilder.build(drawer.draw(), "token_" + token.name, "jpg")
            token.setImagePath(path)
            done += 1
    progressCallback(str(done) + " custom tokens succesfully drawn.")

    # draw all dice
    progressCallback("Drawing dice... ", False)
    done = 0
    for die in library.dice:
        if die.customContent:
            drawer = DiceDrawer(die)
            path = imageBuilder.build(drawer.draw(), "die" + die.name, "png")
            die.setImagePath(path)
            done += 1
    progressCallback(str(done) + " dice succesfully drawn.")

    # UGLY - we already did this step during parsing but we need to create entities AFTER drawing or their image paths aren't set
    creator = EntityCreator(library.all())
    workbook = xlrd.open_workbook(excelFile)
    entities = creator.createEntities(workbook.sheet_by_name('Placement'))

    dicts = []
    for entity in entities:
        dicts.append(entity.as_dict())

    progressCallback("Placing all entities on the tabletop.")
    # add entities to save file
    data["ObjectStates"] = dicts
    progressCallback("All entities have been placed.")

    # save file
    path = saveDir + '\TS_' + fileName.replace(' ', '_') + '.json'
    progressCallback("Saving file to " + path)
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import font


class Config:
    def __init__(self, excelFile, saveDir, imagesDir, fileName, ftpServer, ftpFolder, ftpUsername, ftpPassword, ftpBaseUrl):
        self.excelFile = excelFile
        self.saveDir = saveDir
        self.imagesDir = imagesDir
        self.fileName = fileName
        self.ftpServer = ftpServer
        self.ftpFolder = ftpFolder
        self.ftpUsername = ftpUsername
        self.ftpPassword = ftpPassword
        self.ftpBaseUrl = ftpBaseUrl
        self.saveFolderDeduced = False
        self.loadConfig()
        folder = tryAndFindSaveGamesFolder()
        if folder:
            self.saveDir.set(folder)
            self.saveFolderDeduced = True

    def setExcelFile(self):
        self.excelFile.set(filedialog.askopenfilename(initialdir='~'))
        self.saveConfig()

    def setSaveDir(self):
        self.saveDir.set(filedialog.askdirectory(initialdir='~'))
        self.saveConfig()

    def setImagesDir(self):
        self.imagesDir.set(filedialog.askdirectory(initialdir='~'))
        self.saveConfig()

    def setFilename(self):
        self.fileName.set(simpledialog.askstring("Filename?", "Enter the filename:"))
        self.saveConfig()

    def setFtpSettings(self):
        self.ftpServer.set(simpledialog.askstring("Ftp server url?", "Enter the ftp url:"))
        if self.ftpServer.get() == '':
            self.ftpUsername.set('')
            self.ftpPassword.set('')
            self.ftpBaseUrl.set('')
            self.saveConfig()
            return
        self.ftpFolder.set(simpledialog.askstring("Ftp folder to use?", "Enter the folder:"))
        self.ftpUsername.set(simpledialog.askstring("Ftp server username?", "Enter the username:"))
        self.ftpPassword.set(simpledialog.askstring("Ftp server password?", "Enter the ftp password:"))
        self.ftpBaseUrl.set(simpledialog.askstring("Ftp www base url?", "Enter the ftp www base url:"))
        self.saveConfig()

    def readyToRun(self):
        return self.excelFile.get() and self.saveDir.get() and self.imagesDir.get() and self.fileName.get()

    def readyToParse(self):
        return self.excelFile.get()

    def isSaveFolderDeduced(self):
        return self.saveFolderDeduced

    def loadConfig(self):
        try:
            with open('settings.json', 'r') as infile:
                data = json.load(infile)
                self.excelFile.set(data['e'])
                self.saveDir.set(data['s'])
                self.imagesDir.set(data['i'])
                self.fileName.set(data['f'])
                try:
                    self.ftpServer.set(data['f_s'])
                    self.ftpUsername.set(data['f_u'])
                    self.ftpPassword.set(data['f_p'])
                    self.ftpBaseUrl.set(data['f_w'])
                    self.ftpFolder.set(data['f_f'])
                except KeyError:
                    pass
        except FileNotFoundError:
            return

    def saveConfig(self):
        data = {
            "e": self.excelFile.get(),
            "s": self.saveDir.get(),
            "i": self.imagesDir.get(),
            "f": self.fileName.get(),
            "f_s": self.ftpServer.get(),
            "f_u": self.ftpUsername.get(),
            "f_p": self.ftpPassword.get(),
            "f_w": self.ftpBaseUrl.get(),
            "f_f": self.ftpFolder.get()
        }
        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile)


class App:
    def __init__(self, master):
        import pygame
        self.pygame = pygame
        self.master = master
        master.geometry("700x600")
        self.filenameVar = StringVar()
        self.config = Config(StringVar(), StringVar(), StringVar(), self.filenameVar, StringVar(), StringVar(), StringVar(), StringVar(), StringVar())

        frame = Frame(master)
        frame.grid()
        frame.grid_columnconfigure(1, minsize=400)

        self.customFont = font.Font(family="Arial", size=18)
        self.headerLabel = Label(frame, text="Prototypical!", font=self.customFont)
        self.headerLabel.grid(row=0, column=0, columnspan=2)

        self.ftpStatusText = StringVar()
        self.setFtpStatus()

        self.excelFile(frame)
        self.savedirFile(frame)
        self.imagedirFile(frame)
        self.filename(frame)
        self.ftpSettings(frame)

        buttonFrame = Frame(frame)
        buttonFrame.grid(row=6, column=1)

        self.parseButton = Button(buttonFrame, text="PARSE GAME", command=self.parse)
        self.parseButton.grid(row=0, column=0)

        self.buildButton = Button(buttonFrame, text="BUILD GAME", command=self.build)
        self.buildButton.grid(row=0, column=1)

        self.newTemplateButton = Button(buttonFrame, text="NEW TEMPLATE", command=self.template)
        self.newTemplateButton.grid(row=0, column=2)

        self.statusLabel = Label(frame, text="Status:")
        self.statusLabel.grid(row=7, column=0, columnspan=2)

        self.status = Text(frame)
        self.status.grid(row=8, column=0, columnspan=2)
        self.status.tag_configure("error", foreground="red", underline=True)

        try:
            version = open('data/version', 'r').readline(10)
        except FileNotFoundError as e:
            version = 'dev'

        self.statusLabel = Label(frame, text="version: " + version)
        self.statusLabel.grid(row=9, column=0, columnspan=2)

    def setFtpStatus(self):
        if self.config.ftpServer.get() != '':
            if testFtpConnection(self.config):
                self.ftpStatusText.set(self.config.ftpServer.get() + ' as ' + self.config.ftpUsername.get())
            else:
                self.ftpStatusText.set("Failed to connect to " + self.config.ftpServer.get())
        else:
            self.ftpStatusText.set("Turned off (local only)")

    def excelFile(self, frame):
        self.excelButton = Button(frame, text="SET SPREADSHEET", command=self.config.setExcelFile, width=30)
        self.excelButton.grid(row=1, column=0)

        self.excelText = Label(frame, textvariable=self.config.excelFile)
        self.excelText.grid(row=1, column=1)

    def savedirFile(self, frame):
        if not self.config.isSaveFolderDeduced():
            self.savedirButton = Button(frame, text="SET SAVE DIR", command=self.config.setSaveDir, width=30)
            self.savedirButton.grid(row=2, column=0)

            self.savedirText = Label(frame, textvariable=self.config.saveDir)
            self.savedirText.grid(row=2, column=1)

    def imagedirFile(self, frame):
        self.imagedirButton = Button(frame, text="SET IMAGES DIR", command=self.config.setImagesDir, width=30)
        self.imagedirButton.grid(row=3, column=0)

        self.imagedirText = Label(frame, textvariable=self.config.imagesDir)
        self.imagedirText.grid(row=3, column=1)

    def filename(self, frame):
        self.filenameButton = Button(frame, text="SET GAME NAME", command=self.config.setFilename, width=30)
        self.filenameButton.grid(row=4, column=0)

        self.filenameText = Label(frame, textvariable=self.config.fileName)
        self.filenameText.grid(row=4, column=1)

    def ftpSettings(self, frame):
        self.ftpButton = Button(frame, text="CONFIGURE FTP", command=self.doFtpSettingsUpdate, width=30)
        self.ftpButton.grid(row=5, column=0)

        self.ftpText = Label(frame, textvariable=self.ftpStatusText)
        self.ftpText.grid(row=5, column=1)

    def doFtpSettingsUpdate(self):
        self.config.setFtpSettings()
        self.setFtpStatus()

    def template(self):
        file = filedialog.asksaveasfilename()
        if file:
            path = file + ".xls"
            try:
                copyfile("data/template.xls", path)
                self.pushStatusMessage("Created a new empty template: " + path)
                if sys.platform == 'win32':
                    os.startfile(path)
            except FileNotFoundError as e:
                self.pushErrorMessage(
                    "The base template is missing. Please ensure that the application was installed successfully.",
                    "creating template")

    def build(self):
        if self.config.readyToRun():
            self.flushStatus()
            self.pushStatusMessage("Going to build!")
            try:
                buildFile(self.config.excelFile.get(), imageBuilder(self.pygame, self.config), self.config.saveDir.get(),
                          self.config.fileName.get(), self.pushStatusMessage)
                self.pushStatusMessage("Done building!")
            except BaseException as e:
                self.pushErrorMessage(e)
                raise e
        else:
            self.pushErrorMessage("Missing some settings. Please ensure all 4 settings above are configured properly.")

    def parse(self):
        self.flushStatus()
        self.pushStatusMessage("Going to parse!")
        try:
            parseFile(self.config.excelFile.get(), self.pushStatusMessage)
            self.pushStatusMessage("Done parsing!")
        except BaseException as e:
            self.pushErrorMessage(e)
            raise e

    def pushErrorMessage(self, e, during="building"):
        import traceback
        self.pushStatusMessage("\n")
        index = self.status.index(INSERT)
        curline = index.split('.')[0]
        self.pushStatusMessage("\nUh oh, there was a problem while " + during + ":")
        self.status.tag_add("error", str(int(curline) + 1) + ".0", str(int(curline) + 2) + ".0")
        self.pushStatusMessage(str(e))
        self.pushStatusMessage("\n" + traceback.format_exc())

    def pushStatusMessage(self, msg, newline=True):
        self.status.insert(END, msg + ("\n" if newline else ''))
        self.master.update()

    def flushStatus(self):
        self.status.delete(1.0, END)

def imageBuilder(pygame, config):
    if config.ftpBaseUrl.get() != '':
        return ftpDirImageBuilder(
            pygame,
            config.imagesDir.get(),
            config.ftpBaseUrl.get(),
            config.ftpServer.get(),
            config.ftpFolder.get(),
            config.ftpUsername.get(),
            config.ftpPassword.get(),
            config.fileName.get()
        )
    else:
        return imagesDirImageBuilder(pygame, config.imagesDir.get())

class imagesDirImageBuilder:
    def __init__(self, pygame, basePath):
        self.pygame = pygame
        self.basePath = basePath
    def build(self, image, file, extension):
        path = self.basePath + '/' + file + "." + extension
        self.pygame.image.save(image, path)
        return "file:///" + path

class ftpDirImageBuilder:
    def __init__(self, pygame, imageBasePath, ftpBasePath, ftpServer, ftpFolder, ftpUsername, ftpPassword, gameName):
        self.imageBasePath = imageBasePath
        self.ftpBasePath = ftpBasePath
        self.pygame = pygame
        self.ftpServer = ftpServer
        self.ftpFolder = ftpFolder
        self.ftpUsername = ftpUsername
        self.ftpPassword = ftpPassword
        self.gameName = gameName
    def build(self, image, file, extension):
        localPath = self.imageBasePath + '/' + file + "." + extension
        localName = file + '.' + extension
        self.pygame.image.save(image, localPath)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        con = pysftp.Connection(
            host=self.ftpServer,
            username=self.ftpUsername,
            password=self.ftpPassword,
            cnopts=cnopts
        )
        with pysftp.cd(self.imageBasePath):
            con.chdir(self.ftpFolder)
            if not con.exists(self.gameName):
                con.mkdir(self.gameName)
            con.chdir(self.gameName)
            if con.exists(self.gameName):
                con.remove(localName)
            con.put(localName)
        con.close()
        return self.ftpBasePath + '/' + self.gameName + '/' + file + '.' + extension


def testFtpConnection(config):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    try:
        con = pysftp.Connection(
            host=config.ftpServer.get(),
            username=config.ftpUsername.get(),
            password=config.ftpPassword.get(),
            cnopts=cnopts
        )
        con.close()
        return True
    except BaseException:
        return False


# tests - need to be moved!! (and not run on every load)
from tests.complexTypeParserTest import ComplexTypeParserTest
from tests.reader.color import ColorReaderTest
from tests.reader.number import NumberReaderTest
from tests.reader.dimensions import DimensionsReaderTest
from tests.reader.content import ContentReaderTest

def runTests():
    # run test cases
    ComplexTypeParserTest().run()
    ColorReaderTest().run()
    NumberReaderTest().run()
    DimensionsReaderTest().run()
    ContentReaderTest().run()
    def emptyCallback(msg, newLine = True):
        pass
    parseFile("data/testgame.xls", emptyCallback)

runTests()

# run the app
root = Tk()
root.wm_title("Prototypical")
app = App(root)
root.mainloop()
