import pygame

from drawer.textrect import render_fitted_textrect
from drawer.color import convert_tts_to_pygame

EDGE_MARGIN = 25

LEFTRIGHT_MARGIN = 10
TOPBOTTOM_MARGIN = 10

class ComplexObjectDrawer:

    def __init__(self, object):
        self.object = object
        self.size = self.getShapeSize(object.type.shape)

    def draw(self):
        w, h = self.getCardSize()
        self.surf = pygame.Surface((w - 2 * EDGE_MARGIN,h - 2 * EDGE_MARGIN))
        self.surf.fill(convert_tts_to_pygame(self.object.type.bgColor))
        for key, content in self.object.content.items():
            self.drawContentToArea(content, self.object.type.shape.areas[key])
        self.fullSurf = pygame.Surface((w, h))
        self.fullSurf.fill(convert_tts_to_pygame(self.object.type.bgColor))
        self.fullSurf.blit(self.surf, (EDGE_MARGIN, EDGE_MARGIN))
        return self.fullSurf

    def getCardSize(self):
        return self.object.type.size

    def getShapeSize(self, shape):
        return shape.size

    # note: areas in the shape are actually row, col and not x,y
    def drawContentToArea(self, content, area):
        w, h = self.getCardSize()
        dw = w - (2*EDGE_MARGIN)
        dh = h - (2*EDGE_MARGIN)
        rect = pygame.Rect(
            LEFTRIGHT_MARGIN + area[1] * dw / self.size[0],
            TOPBOTTOM_MARGIN + area[0] * dh / self.size[1],
            (area[3]+1) * dw / self.size[0] - LEFTRIGHT_MARGIN,
            (area[2]+1) * dh / self.size[1] - TOPBOTTOM_MARGIN
        )
        self.write(content, rect)

    def write(self, content, rect):
        if isinstance(content, float) and content.is_integer():
            content = int(content)

        # the render function expects a rect with 0,0 topleft.
        rerect = pygame.Rect((0,0, rect[2] - rect[0], rect[3] - rect[1]))
        surf = render_fitted_textrect(str(content), rerect, (0, 0, 0), (255, 255, 255))
        if not surf:
            raise BaseException("Unable to draw the card. Are you reserving enough space for all your content? Trying to write: " + str(content))
        self.surf.blit(surf, rect)