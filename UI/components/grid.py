import pygame as pg

from models.screen import Screen


class Grid:
    """Represents a UI grid"""

    def __init__(self, size: tuple, tile_size: tuple, color: tuple = (0, 0, 0)):
        self.image: pg.Surface = pg.Surface(
            (
                int(size[0] * tile_size[0]),
                int(size[1] * tile_size[1])
            ),
            pg.SRCALPHA
        )
        self.size: tuple = size
        self.tile_size: tuple = tile_size
        self.color = color

        self._build()

    def _build(self):
        """Builds the grid based on its size and tile size"""
        for x in range(1, self.size[0]):
            pg.draw.line(
                self.image, self.color,
                (x * self.tile_size[0], 0), (x * self.tile_size[0], self.image.get_size()[1])
            )

        for y in range(1, self.size[1]):
            pg.draw.line(
                self.image, self.color,
                (0, y * self.tile_size[1]), (self.image.get_size()[0], y * self.tile_size[1])
            )

    def draw(self, screen: Screen, position: tuple):
        """Draws the grid on the screen"""
        screen.blit(self.image, position)
