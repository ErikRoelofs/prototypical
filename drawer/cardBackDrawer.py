import pygame
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.color import convert_tts_to_pygame

class CardBackDrawer:
    def __init__(self, config):
        self.config = config

    def draw(self, deck):
        drawer = ComplexObjectDrawer(deck.cards[0].object, self.config)
        surf = pygame.Surface(drawer.getCardSize())
        self.drawCardBacks(drawer, surf, deck.cards)
        return surf

    def drawCardBacks(self, drawer, surf, cards):
        if isinstance(cards[0].object.type.backside, str):
            drawer.drawImage(surf, cards[0].object.type.backside, surf.get_rect())
        else:
            surf.fill(convert_tts_to_pygame(cards[0].object.type.backside))