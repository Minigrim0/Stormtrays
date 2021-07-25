import pygame

from models.screen import Screen


class Tile:
    """Represents a tile from the editor"""

    def __init__(self, code: str, image: tuple, position: tuple = None, rotation: int = 0):
        self.code = code
        self.image = image
        self.rotation = rotation
        self.position = position

    def rotate(self, amount: int = 1):
        """Rotates the image by 90 degrees"""
        self.rotation = (self.rotation + amount) % 4
        self.image = (
            pygame.transform.rotate(self.image[0], amount * 90),
            pygame.transform.rotate(self.image[1], amount * 90),
        )

    def draw(self, screen: Screen, editor=False):
        """Draws the tile on screen

        Args:
            screen (Screen): The screen to draw the tile on
            editor (bool, optional): Whether to draw it as an editor
                tile or a game tile. Defaults to False.
        """
        screen.blit(self.image[int(editor)], self.position)

    def direction(self):
        if (self.code, self.rotation) in (("c1", 0), ("t1", 180), ("t2", 270)):
            return (1, 0)
        elif (self.code, self.rotation) in (("c1", 90), ("t1", 270), ("t2", 0)):
            return (0, -1)
        elif (self.code, self.rotation) in (("c1", 180), ("t1", 0), ("t2", 90)):
            return (-1, 0)
        elif (self.code, self.rotation) in (("c1", 270), ("t1", 90), ("t2", 180)):
            return (0, 1)
        elif self.code == "x1":
            return (0, 0)

    def move(self, pos):
        self.position = pos

    def toJson(self):
        return {"code": self.code, "rotation": self.rotation}
