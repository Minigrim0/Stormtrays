import pygame
import math

from src.screen import Screen


class GoldAnim:
    def __init__(self, pos: tuple, amount: int):
        self.posx = pos[0]
        self.posy = pos[1]
        self.amount = amount
        self.i = 0
        myfont = pygame.font.SysFont("Viner Hand ITC", 15)
        self.NbrsAffiche = myfont.render(str(self.amount), 1, (0, 0, 0))

    def bouge(self, screen: Screen, goldImg, niveau):
        self.i += 1
        self.posy -= 2
        if self.i == 24:
            niveau.GoldTab.remove(self)
        screen.blit(
            goldImg, (self.posx - 12 + 3 * math.cos(self.i), self.posy - 6))
        screen.blit(
            self.NbrsAffiche, (self.posx + 3 * math.cos(self.i), self.posy - 6))
