import random
from domain.token import Token
from domain.token import ContentToken
from domain.die import Die
from domain.deck import Deck
from domain.complexObject import ComplexObject
from domain.bag import Bag, InfiniteBag
from tts.simpletoken import SimpleToken
from tts.transform import Transform
from tts.die import Die as TTSDie
from tts.deck import Deck as TTSDeck
from tts.board import Board as TTSBoard
from tts.token import Token as TTSToken
from tts.bag import Bag as TTSBag
from reader.content import read_content

XMIN = -27
XMAX = 27
ZMIN = -17
ZMAX = 17
YHEIGHT = 2
BOARDYHEIGHT = 1

XCHUNKS = 15
YCHUNKS = 15

class EntityCreator:
    def __init__(self, library):
        self.library = library

    def getCoordInChunk(self, chunkX, chunkY, numXChunks, numYChunks):
        if not 0 <= chunkX < numXChunks:
            raise ValueError("Trying to place an object outside the playing field; x-coordinates should be between 0 and " + str(int(numXChunks - 1)))
        if not 0 <= chunkY < numYChunks:
            raise ValueError("Trying to place an object outside the playing field; y-coordinates should be between 0 and " + str(int(numYChunks - 1)))

        width = (XMAX - XMIN) / numXChunks
        height = (ZMAX - ZMIN) / numYChunks
        xOffset = random.uniform(0, width)
        yOffset = random.uniform(0, height)
        return (xOffset + XMIN + (chunkX * width), yOffset + ZMIN + (chunkY * height))

    def findObjectByName(self, name):
        for type in self.library:
            if type.name == name:
                return type
        raise ValueError("Unknown entity type: " + name)

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
                raise ValueError("Only ComplexTypes of the 'board' type can be placed directly. The others go into a deck! (Tried placing a " + entity.name + ")")
        if isinstance(entity, Bag):
            return self.placeBag(coords, entity)
        raise NotImplementedError("Not sure what to do with this: " + entity.__class__.__name__)

    def placeToken(self, coords, entity):
        if isinstance(entity, ContentToken):
            transform = Transform(coords[0], YHEIGHT, coords[1], 0, 180, 0, entity.size,entity.size,entity.size)
            bs = TTSToken(transform, entity.imagePath)
            return bs
        else:
            transform = Transform(coords[0], YHEIGHT, coords[1], 0, 0, 0, entity.size, entity.size, entity.size)
            bs = SimpleToken(entity.entity, transform, entity.color)
            return bs

    def placeDie(self, coords, entity):
        transform = Transform(coords[0], YHEIGHT, coords[1], 0, 0, 0, entity.size, entity.size, entity.size)
        die = TTSDie(entity.sides, entity.color, transform, entity.customContent, entity.imagePath)
        return die

    def placeDeck(self, coords, entity):
        transform = Transform(coords[0], YHEIGHT, coords[1], 0, 180, 180, 1,1,1)
        deck = TTSDeck(transform, entity.name, entity.cards, entity.imagePath, entity.backImagePath)
        return deck

    def placeBoard(self, coords, entity):
        transform = Transform(coords[0], BOARDYHEIGHT, coords[1], 0, 0, 0, 1, 1, 1)
        board = TTSBoard(transform, entity)
        return board

    def placeBag(self, coords, entity):
        transform = Transform(coords[0], BOARDYHEIGHT, coords[1], 0, 0, 0, entity.size, entity.size, entity.size)
        bag = TTSBag(transform, entity.color, entity.name, self.convertToTTS(coords, entity.content), isinstance(entity, InfiniteBag))
        return bag

    def convertToTTS(self, coords, items):
        converted = []
        for item in items:
            converted.append(self.createEntity(coords, item))
        return converted

    def createEntities(self, sheet):
        entities = []
        for col in range(0,min(14, sheet.ncols)):
            for row in range(0,min(14, sheet.nrows)):
                content = read_content(sheet.cell(rowx=row, colx=col).value)
                for item in content:
                    try:
                        object = self.findObjectByName(item[1])
                    except ValueError as e:
                        raise ValueError(str(e) + " (while trying to place items on the board)")
                    for i in range(0, int(item[0])):
                        entities.append(self.createEntity(self.getCoordInChunk(row, col, XCHUNKS, YCHUNKS), object))
        return entities