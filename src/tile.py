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

    def move(self, pos):
        self.position = pos

    def toJson(self):
        return {"code": self.code, "rotation": self.rotation}
