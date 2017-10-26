import pygame

from drawer.color import convert_tts_to_pygame

MARGIN = 10

class TokenDrawer:

    def __init__(self, token):
        self.token = token
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)

    def draw(self):
        content = self.token.content
        if isinstance(content, float) and content.is_integer():
            content = int(content)

        text = self.fontObj.render(str(content), True, convert_tts_to_pygame(self.token.text_color), convert_tts_to_pygame(self.token.bg_color))
        rect = text.get_rect()
        surf = pygame.Surface((rect[2] + 2 * MARGIN, rect[3] + 2 * MARGIN))
        surf.fill(convert_tts_to_pygame(self.token.bg_color))

        surf.blit(text, (MARGIN, MARGIN))
        return surf
