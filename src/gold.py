import math

import pygame as pg

from models.screen import Screen
from models.game_options import GameOptions
from models.image_bank import ImageBank


class Gold:
    """A flying gold image to show the winned gold when an ennemy has been killed"""

    def __init__(self, pos: tuple, amount: int):
        self.posx, self.posy = pos
        bank = ImageBank.getInstance()
        if bank.exists("gold"):
            self.image = bank["gold"]
        else:
            self.image = pg.image.load("assets/images/coin.png")
            bank.set("gold", self.image)

        self.amount = amount
        self.life_span = 2  # seconds
        font = GameOptions.getInstance().fonts["MedievalSharp-xOZ5"]["14"]
        self.NbrsAffiche = font.render(str(self.amount), 1, (0, 0, 0))

    def update(self, timeElapsed):
        """Updates the position and life_span of the gold coin

        Returns:
            bool: whether the animation is over or not
        """
        self.life_span -= timeElapsed
        self.posy -= 64 * timeElapsed
        if self.life_span <= 0:
            return True

    def draw(self, screen: Screen):
        """Draws the coin on the screen"""
        screen.blit(
            self.image,
            (
                self.posx - 12 + 3 * math.cos(10 * self.life_span),
                self.posy - 6
            )
        )
        screen.blit(
            self.NbrsAffiche,
            (
                self.posx + 3 * math.cos(10 * self.life_span),
                self.posy - 6
            )
        )
