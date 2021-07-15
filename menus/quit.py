import pygame as pg

from menus.menu import Menu
from src.runnable import Runnable

from UI.components.button import Button
import src.constantes as constants


class QuitMenu(Menu, Runnable):
    """A menu for the user to confirm his choice to quit the game"""

    def __init__(self, screen):
        super().__init__(screen)

        self.buttons.append(Button((516, 297), (120, 50), pg.image.load(constants.reprise).convert_alpha()))
        self.buttons[-1].callback = self.cancel
        self.buttons.append(Button((516, 367), (120, 50), pg.image.load(constants.quitpaus).convert_alpha()))
        self.buttons[-1].callback = self.confirm

        self.background = pg.image.load(constants.fondm).convert_alpha()
        self.confirmQuit = pg.image.load(constants.ConfirmQuit).convert_alpha()

        self.toReturn: str = None  # Either "q" or "c"

    def __call__(self) -> str:
        super().__call__()
        return self.toReturn

    def loop(self):
        """The bit of code called at each iteration"""
        self.draw()
        self.handleEvent()

    def draw(self):
        """Draws the buttons/images on screen and refreshes it"""
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.confirmQuit, (376, 152))
        super().draw()

        self.screen.flip()

    def handleEvent(self):
        """Handles the user inputs"""
        for event in super().handleEvent():
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:
                self.running = False

    def cancel(self):
        """Callback for when the user decides to get back to the game"""
        self.running = False
        self.toReturn = "c"

    def confirm(self):
        """Callback for when the user decided to quit the game"""
        self.running = False
        self.toReturn = "q"
