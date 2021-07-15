import pygame as pg

from UI.components.button import Button


class Card(Button):
    def __init__(self, pos: tuple, size: tuple, thumbnail: pg.Surface, title: str, description: str, **kwargs):
        super().__init__(pos, size)

        self.thumbnail = thumbnail
        self.title = title
        self.description = description
        self.generateImage(**kwargs)

    def generateImage(self, **kwargs):
        """Generates the card image"""
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.image.fill((0, 0, 0, 255))

        self.image.blit(self.thumbnail, (5, 5))
