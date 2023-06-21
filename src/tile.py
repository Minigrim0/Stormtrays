import logging
import pygame as pg

from models.screen import Screen

logger = logging.getLogger(__file__)


class Tile(pg.sprite.Sprite):
    """Represents a tile from the editor"""

    def __init__(self, group: pg.sprite.Group, code: str, image: pg.Surface, position: tuple = None, rotation: int = 0):
        super().__init__(group)
        self.code = code

        self.image = image
        if self.image is None or position is None:
            raise RuntimeError("Tile image or position can't be None")

        self.rect = self.image.get_rect(center=position)

        self.rotation = rotation

    def rotate(self, amount: int = 1):
        """Rotates the image by 90 degrees"""
        self.rotation = (self.rotation + amount) % 4
        self.image = (
            pg.transform.rotate(self.image[0], amount * 90) if self.image[0] is not None else None,
            pg.transform.rotate(self.image[1], amount * 90) if self.image[1] is not None else None,
        )

    def resize(self, size: tuple[int, int]) -> None:
        """Resizes the tile to the given size"""
        self.image = (
            pg.transform.scale(self.image[0], size) if self.image[0] is not None else None,
            pg.transform.scale(self.image[1], size) if self.image[1] is not None else None,
        )

    def draw(self, screen: Screen, editor=False, offset: tuple[int, int] = (0, 0)):
        """Draws the tile on screen

        Args:
            screen (Screen): The screen to draw the tile on
            editor (bool, optional): Whether to draw it as an editor
                tile or a game tile. Defaults to False.
        """
        if self.image[int(editor)] is not None:
            screen.blit(self.image[int(editor)], (self.position[0] + offset[0], self.position[1] + offset[1]))

    def direction(self) -> tuple:
        """Returns the direction the current tile leads towards"""
        if (self.code, self.rotation) in (("c1", 0), ("s1", 0), ("t1", 2), ("t2", 3)):
            return (1, 0)
        if (self.code, self.rotation) in (("c1", 1), ("s1", 1), ("t1", 3), ("t2", 0)):
            return (0, -1)
        if (self.code, self.rotation) in (("c1", 2), ("s1", 2), ("t1", 0), ("t2", 1)):
            return (-1, 0)
        if (self.code, self.rotation) in (("c1", 3), ("s1", 3), ("t1", 1), ("t2", 2)):
            return (0, 1)
        if self.code == "x1":
            return (0, 0)
        return (-1, -1)

    def move(self, pos):
        """Moves the tile to the given position"""
        self.position = pos

    def toJson(self) -> dict:
        """Serializes the tiles information to a dictionnary"""
        return {"code": self.code, "rotation": self.rotation}
