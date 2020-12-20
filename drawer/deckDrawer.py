import pygame
from drawer.complexObjectDrawer import ComplexObjectDrawer

class DeckDrawer:
    def __init__(self, config):
        self.config = config

    def draw(self, deck):
        drawer = ComplexObjectDrawer(deck.cards[0].object, self.config)
        w, h = drawer.getCardSize()
        self.size = (w * 10, h * 7)
        self.cardSize = (w, h)

        surf = pygame.Surface(self.size)
        self.drawCards(surf, deck.cards)
        return surf

    def drawCards(self, surf, cards):
        done = 0
        for i in range(0,7):
            for j in range(0,10):
                cardDrawer = ComplexObjectDrawer(cards[done].object, self.config)
                surf.blit(cardDrawer.draw(), (j * self.cardSize[0], i * self.cardSize[1]))
                done += 1
                if done == len(cards):
                    return