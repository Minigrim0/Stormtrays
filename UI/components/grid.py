import pygame as pg

from models.screen import Screen


class Grid:
    """Represents a UI grid"""

    def __init__(self, size: tuple, tile_size: tuple, color: tuple = (0, 0, 0)):
        self.image: pg.Surface = None
        self.size: tuple[int, int] = size
        self.tile_size: tuple[int, int] = tile_size
        self.color: tuple[int, int, int] = color
        self.position: tuple[int, int] = (0, 0)

        self._build()

    def _build(self):
        """Builds the grid based on its size and tile size"""
        self.image = pg.Surface(
            (
                int(self.size[0] * self.tile_size[0]),
                int(self.size[1] * self.tile_size[1])
            ),
            pg.SRCALPHA
        )

        for x in range(1, self.size[0]):
            pg.draw.line(
                self.image, self.color,
                (self.position[0] + x * self.tile_size[0], self.position[1]),
                (self.position[0] + x * self.tile_size[0], self.position[1] + self.image.get_size()[1])
            )

        for y in range(1, self.size[1]):
            pg.draw.line(
                self.image, self.color,
                (self.position[0], self.position[1] + y * self.tile_size[1]),
                (self.position[0] + self.image.get_size()[0], self.position[1] + y * self.tile_size[1])
            )

    def move(self, vec: tuple[int, int]) -> None:
        """Moves the position of the grid by the given vector"""
        self.position = (
            self.position[0] + vec[0],
            self.position[1] + vec[1]
        )

    def set_size(self, size: tuple, tile_size: tuple) -> None:
        """Updates the size of the grid"""
        self.size = size
        self.tile_size = tile_size
        self._build()

    def _posToTile(self, pos) -> tuple[int, int]:
        """Returns the coordinates of the tile under the position"""
        event_x, event_y = pg.mouse.get_pos()
        event_x -= self.position[0]
        event_y -= self.position[1]

        tile = (
            event_x // self.tile_size[0],
            event_y // self.tile_size[1]
        )
        return tile if (tile[0] >= 0 and tile[0] < self.size[0]) and (tile[1] >= 0 and tile[1] < self.size[1]) else None

    def update(self, event: pg.event) -> None:
        """Highlights the case hovered by the mouse"""
        pass

    def draw(self, screen: Screen):
        """Draws the grid on the screen"""
        screen.blit(self.image, self.position)
        highlighted_tile = self._posToTile(pg.mouse.get_pos())
        if highlighted_tile is not None:
            pg.draw.rect(
                screen.fenetre,
                (128, 0, 0),
                pg.Rect(
                    (
                        self.position[0] + (highlighted_tile[0] * self.tile_size[0]),
                        self.position[1] + (highlighted_tile[1] * self.tile_size[1]),
                    ),
                    (self.tile_size[0], self.tile_size[1])
                ),
                width=2
            )
