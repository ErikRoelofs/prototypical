import pygame
import drawer.complexObjectDrawer

class DeckDrawer:
    def __init__(self):
        self.size = (drawer.complexObjectDrawer.CARD_WIDTH * 10, drawer.complexObjectDrawer.CARD_HEIGHT * 7)
        self.cardSize = (drawer.complexObjectDrawer.CARD_WIDTH, drawer.complexObjectDrawer.CARD_HEIGHT)

    def draw(self, deck):
        surf = pygame.Surface(self.size)
        self.drawCards(surf, deck.cards)
        return surf

    def drawCards(self, surf, cards):
        done = 0
        for i in range(0,7):
            for j in range(0,10):
                cardDrawer = drawer.complexObjectDrawer.ComplexObjectDrawer(cards[done].object)
                surf.blit(cardDrawer.draw(), (j * self.cardSize[0], i * self.cardSize[1]))
                done += 1
                if done == len(cards):
                    return