import pygame as pg

from src import constantes as constants

from models.screen import Screen

from menus.menu import Menu
from src.runnable import Runnable


class CreditsMenu(Menu, Runnable):

    def __init__(self, screen: Screen):
        super().__init__(screen)

        self.scroll = 0
        self.background = pg.image.load(constants.fondm)
        self.credits = pg.image.load(constants.Credits)

    def loop(self):
        if self.scroll > 2900:
            self.running = False

        self.draw()
        self.handleEvent()
        self.screen.flip()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.credits, (0, - self.scroll))
        self.scroll += 20 * self.screen.timeElapsed

    def handleEvent(self):
        for event in super().handleEvent():
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:
                self.running = False

            if event.type == pg.locals.MOUSEBUTTONDOWN:
                if event.button == 5:
                    self.scroll += 40
                elif event.button == 4:
                    self.scroll -= 40
