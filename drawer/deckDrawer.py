import pygame
from drawer.complexObjectDrawer import ComplexObjectDrawer
from drawer.color import convert_tts_to_pygame

class DeckDrawer:

    def draw(self, deck):
        front = self.drawFronts(deck)
        back = self.drawBacks(deck)
        return front, back

    def drawFronts(self, deck):
        drawer = ComplexObjectDrawer(deck.cards[0].object)
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
                cardDrawer = ComplexObjectDrawer(cards[done].object)
                surf.blit(cardDrawer.draw(), (j * self.cardSize[0], i * self.cardSize[1]))
                done += 1
                if done == len(cards):
                    return

    def drawBacks(self, deck):
        drawer = ComplexObjectDrawer(deck.cards[0].object)
        if deck.uniqueBacks:
            size = drawer.getCardSize()
            surf = pygame.Surface(size[0] * 19, size[1] * 7)
        else:
            surf = pygame.Surface(drawer.getCardSize())
        self.drawCardBacks(surf, deck, deck.cards)
        return surf

    def drawCardBacks(self, surf, deck, cards):
        if deck.uniqueBacks:
            done = 0
            for i in range(0, 7):
                for j in range(0, 10):
                    if cards[done].object.backcolor() != "NEXT":
                        drawer = ComplexObjectDrawer(self.findBackside(cards[done]))
                        theBack = drawer.draw()
                    else:
                        drawer = ComplexObjectDrawer(cards[done])
                        theBack = pygame.Surface(drawer.getCardSize())
                        theBack.fill(convert_tts_to_pygame(cards[done].object.backcolor()))

                    surf.blit(theBack, (j * self.cardSize[0], i * self.cardSize[1]))
                    done += 1
                    if done == len(cards):
                        return

        else:
            surf.fill(convert_tts_to_pygame(cards[0].object.backcolor()))