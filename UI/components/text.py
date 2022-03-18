import pygame as pg

class Text:
    def __init__(self, text: pg.Surface, position: tuple):
        self.position = position
        self.image = text

    def render(self, text: str, font: pg.font, aa = 1, color = (255, 255, 255)):
        self.image = font.render(text, aa, color)

    def draw(self, screen):
        screen.blit(self.image, self.position)