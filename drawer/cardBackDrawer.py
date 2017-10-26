import pygame
import drawer.complexObjectDrawer
from drawer.color import convert_tts_to_pygame

class CardBackDrawer:
    def __init__(self):
        self.size = (drawer.complexObjectDrawer.CARD_WIDTH, drawer.complexObjectDrawer.CARD_HEIGHT)
        self.cardSize = (drawer.complexObjectDrawer.CARD_WIDTH, drawer.complexObjectDrawer.CARD_HEIGHT)

    def draw(self, deck):
        surf = pygame.Surface(self.size)
        self.drawCardBacks(surf, deck.cards)
        return surf

    def drawCardBacks(self, surf, cards):
        surf.fill(convert_tts_to_pygame(cards[0].object.type.backside))