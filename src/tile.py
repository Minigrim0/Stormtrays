import pygame as pg

from models.screen import Screen


class Tile:
    """Represents a tile from the editor"""

    def __init__(self, code: str, image: tuple, position: tuple = None, rotation: int = 0):
        self.code = code
        self.image: (pg.Surface, pg.Surface) = image
        self.rotation = rotation
        self.position = position

    @property
    def editor_image(self) -> pg.Surface:
        return self.image[1]

    def rotate(self, amount: int = 1):
        """Rotates the image by 90 degrees"""
        self.rotation = (self.rotation + amount) % 4
        self.image = (
            pg.transform.rotate(self.image[0], amount * 90) if self.image[0] is not None else None,
            pg.transform.rotate(self.image[1], amount * 90) if self.image[1] is not None else None,
        )

    def draw(self, screen: Screen, editor=False):
        """Draws the tile on screen

        Args:
            screen (Screen): The screen to draw the tile on
            editor (bool, optional): Whether to draw it as an editor
                tile or a game tile. Defaults to False.
        """
        if self.image[int(editor)] is not None:
            screen.blit(self.image[int(editor)], self.position)

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
