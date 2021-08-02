import pygame as pg

from UI.components.button import Button

from models.game_options import GameOptions


class Card(Button):
    """A UI element with a background, an image, a title and a description"""

    def __init__(self, pos: tuple, size: tuple, thumbnail: pg.Surface, title: str, description: str, **kwargs):
        super().__init__(pos, size)

        self.thumbnail = thumbnail
        self.title = title
        self.description = description
        self.generateImage(**kwargs)

    def generateImage(self, **kwargs):
        """Generates the card image"""
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.image.fill((0, 0, 0, 128))

        coefficient = ((self.size[1] - 10) / self.thumbnail.get_size()[1])
        self.thumbnail = pg.transform.smoothscale(
            self.thumbnail,
            (
                int(coefficient * self.thumbnail.get_size()[0]),
                int(coefficient * self.thumbnail.get_size()[1])
            )
        )
        self.image.blit(self.thumbnail, (5, 5))

        options = GameOptions.getInstance()
        title_max_size = self.size[1] // 3
        font_size = min(options.fonts["MedievalSharp-xOZ5"].keys(), key=lambda x: abs(int(x) - title_max_size))
        titleImage = options.fonts["MedievalSharp-xOZ5"][str(font_size)].render(self.title, 1, (255, 255, 255))
        self.image.blit(titleImage, (self.thumbnail.get_size()[0] + 10, 5))

        descr_max_size = self.size[1] // 5
        font_size = min(options.fonts["MedievalSharp-xOZ5"].keys(), key=lambda x: abs(int(x) - descr_max_size))
        titleImage = options.fonts["MedievalSharp-xOZ5"][str(font_size)].render(self.description, 1, (255, 255, 255))
        self.image.blit(titleImage, (self.thumbnail.get_size()[0] + 10, 10 + title_max_size))
