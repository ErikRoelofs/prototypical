import pygame
from font.font import Font
# 2,4,5
# 1,3,6 (1 and 6 are upside down)

# main image: 2048x2048

WIDTH = 500
HEIGHT = 500

DRAWSPOTS = [
    (71,1462, True),        #1
    (71,767, False),        #2
    (771, 1462, False),     #3
    (771,767, False),       #4
    (1462,767, False),      #5
    (1462, 1462, True),     #6

]

class DiceDrawer:
    def __init__(self, die):
        self.die = die
        self.largeFontObj = Font.getFont(256)
        self.smallFontObj = Font.getFont(96)

    def draw(self):
        surf = pygame.image.load('data/D6.png')
        for pos, spot in enumerate(DRAWSPOTS):
            content = self.die.customContent[pos]
            if isinstance(content, float) and content.is_integer():
                content = int(content)
            content = str(content)

            if len(content) > 2:
                text = self.smallFontObj.render(str(content), True, (0,0,0), (255,255,255))
            else:
                text = self.largeFontObj.render(str(content), True, (0, 0, 0), (255, 255, 255))
            rect = text.get_rect(center=(WIDTH/2,HEIGHT/2))

            drawSurf = pygame.Surface((WIDTH, HEIGHT))
            drawSurf.fill((255,255,255))
            drawSurf.blit(text, rect)

            if spot[2]: # should be upside down
                drawSurf = pygame.transform.rotate(drawSurf, 180)

            surf.blit(drawSurf, (spot[0], spot[1]))
        return surf
