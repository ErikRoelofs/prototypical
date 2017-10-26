import pygame
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.color import convert_tts_to_pygame

class CardBackDrawer:

    def draw(self, deck):
        drawer = ComplexObjectDrawer(deck.cards[0].object)
        surf = pygame.Surface(drawer.getCardSize())
        self.drawCardBacks(surf, deck.cards)
        return surf

    def drawCardBacks(self, surf, cards):
        surf.fill(convert_tts_to_pygame(cards[0].object.type.backside))