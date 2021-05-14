import pygame

from src.screen import Screen


class Tile:
    def __init__(self, image: tuple, position: tuple, rotation: int):
        self.image = image
        self.rotation = rotation
        self.position = position

    def rotate(self):
        """rotates the image by 90 degrees
        """
        self.rotation = (self.rotation + 1) % 4
        self.image = (
            pygame.transform.rotate(self.image[0], 90),
            pygame.transform.rotate(self.image[1], 90)
        )

    def draw(self, screen: Screen, editor=False):
        """Draws the tile on screen

        Args:
            screen (Screen): The screen to draw the tile on
            editor (bool, optional): Whether to draw it as an editor tile or a game tile. Defaults to False.
        """
        screen.blit(self.image[int(editor)], self.position)
