import pygame

CARD_WIDTH = 400
CARD_HEIGHT = 600

class ComplexObjectDrawer:

    def __init__(self, object):
        self.object = object
        self.size = self.getShapeSize(object.type.shape)
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)

    def draw(self):
        self.surf = pygame.Surface((CARD_WIDTH,CARD_HEIGHT))
        for key, content in enumerate(self.object.content):
            if key in self.object.type.shape.areas:
                self.drawContentToArea(content, self.object.type.shape.areas[key])
        return self.surf

    def getShapeSize(self, shape):
        height = 0
        width = 0
        for number, area in shape.areas.items():
            if area[3] > width:
                width = area[3]
            if area[2] > height:
                height = area[2]
        return (width + 1, height + 1)

    # note: areas in the shape are actually row, col and not x,y
    def drawContentToArea(self, content, area):
        rect = pygame.Rect(
            area[1] * CARD_WIDTH / self.size[0],
            area[0] * CARD_HEIGHT / self.size[1],
            (area[3]+1) * CARD_WIDTH / self.size[0],
            (area[2]+1) * CARD_HEIGHT / self.size[1],
        )
        self.write(content, rect)

    def write(self, content, rect):
        textSurfaceObj = self.fontObj.render(content, True, (255,0,0), (255,255,255))
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.left = rect[0]
        textRectObj.top = rect[1]
        self.surf.blit(textSurfaceObj, textRectObj)
