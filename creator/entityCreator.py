import random
from domain.token import Token
from domain.token import ContentToken
from domain.die import Die
from domain.deck import Deck
from domain.complexObject import ComplexObject
from tts.simpletoken import SimpleToken
from tts.transform import Transform
from tts.die import Die as TTSDie
from tts.deck import Deck as TTSDeck
from tts.board import Board as TTSBoard
from tts.token import Token as TTSToken

XMIN = -27
XMAX = 27
ZMIN = -17
ZMAX = 17
YHEIGHT = 2
BOARDYHEIGHT = 1


class EntityCreator:
    def __init__(self, library):
        self.library = library

    def getCoordInChunk(self, chunkX, chunkY, numXChunks, numYChunks):
        width = (XMAX - XMIN) / numXChunks
        height = (ZMAX - ZMIN) / numYChunks
        xOffset = random.uniform(0, width)
        yOffset = random.uniform(0, height)
        return (xOffset + XMIN + (chunkX * width), yOffset + ZMIN + (chunkY * height))

    def findObjectByName(self, name):
        for type in self.library:
            if type.name == name:
                return type

    def createEntity(self, coords, entity):
        if isinstance(entity, Token):
            return self.placeToken(coords, entity)
        if isinstance(entity, Die):
            return self.placeDie(coords, entity)
        if isinstance(entity, Deck):
            return self.placeDeck(coords, entity)
        if isinstance(entity, ComplexObject):
            if entity.type.type == 'board':
                return self.placeBoard(coords, entity)
            else:
                raise ValueError("Only ComplexTypes of the 'board' type can be placed directly. The others go into a deck!")
        raise NotImplementedError("Not sure what to do with this: " + entity.__class__.__name__)

    def placeToken(self, coords, entity):
        if isinstance(entity, ContentToken):
            transform = Transform(coords[0], YHEIGHT, coords[1], 0, 180, 0, 0.1,0.1,0.1)
            bs = TTSToken(transform, entity.imagePath)
            return bs.as_dict()
        else:
            transform = Transform(coords[0], YHEIGHT, coords[1], 0, 0, 0, entity.size, entity.size, entity.size)
            bs = SimpleToken(entity.entity, transform, entity.color)
            return bs.as_dict()

    def placeDie(self, coords, entity):
        transform = Transform(coords[0], YHEIGHT, coords[1], 0, 0, 0, entity.size, entity.size, entity.size)
        die = TTSDie(entity.sides, entity.color, transform, entity.customContent)
        return die.as_dict()

    def placeDeck(self, coords, entity):
        transform = Transform(coords[0], YHEIGHT, coords[1], 0, 180, 180, 1,1,1)
        deck = TTSDeck(transform, entity.name, entity.cards, entity.imagePath, entity.backImagePath)
        return deck.as_dict()

    def placeBoard(self, coords, entity):
        transform = Transform(coords[0], BOARDYHEIGHT, coords[1], 0, 0, 0, 1, 1, 1)
        board = TTSBoard(transform, entity)
        return board.as_dict()

    def createEntities(self, sheet):
        chunksWide = sheet.cell(rowx=0, colx=1).value
        chunksHigh = sheet.cell(rowx=0, colx=2).value
        entities = []
        row = 1
        while row < sheet.nrows:
            xChunk = sheet.cell(rowx=row, colx=0).value
            yChunk = sheet.cell(rowx=row, colx=1).value
            col = 2
            while col < sheet.ncols and col < 10:
                numToPlace = sheet.cell(rowx=row, colx=col).value
                if numToPlace:
                    typeToPlace = sheet.cell(rowx=row, colx=col + 1).value
                    object = self.findObjectByName(typeToPlace)
                    for i in range(0, int(numToPlace)):
                        entities.append(self.createEntity(self.getCoordInChunk(xChunk, yChunk, chunksWide, chunksHigh), object))
                col += 2
            row += 1
        return entities