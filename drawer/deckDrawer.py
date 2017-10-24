import pygame
import drawer.complexObjectDrawer

class DeckDrawer:
    def __init__(self):
        self.cards = []
        self.size = (drawer.complexObjectDrawer.CARD_WIDTH * 10, drawer.complexObjectDrawer.CARD_HEIGHT * 7)
        self.cardSize = (drawer.complexObjectDrawer.CARD_WIDTH, drawer.complexObjectDrawer.CARD_HEIGHT)

    def addCard(self, card):
        self.cards.append(card)

    def draw(self):
        surf = pygame.Surface(self.size)
        self.drawCards(surf)
        return surf

    def drawCards(self, surf):
        done = 0
        for i in range(0,7):
            for j in range(0,10):
                surf.blit(self.cards[done].draw(), (j * self.cardSize[0], i * self.cardSize[1]))
                done += 1
                if done == len(self.cards):
                    return