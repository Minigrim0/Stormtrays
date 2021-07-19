from pygame.locals import MOUSEBUTTONDOWN

from UI.components.button import Button
from models.screen import Screen


class Menu:
    """The base class for all menus"""

    def __init__(self, screen: Screen):
        self.buttons: [Button] = []
        self.screen = screen

    @staticmethod
    def loop():
        """Plays music if needed"""
        from models.game import Game

        Game.getInstance().playMusic()

    def draw(self):
        """Draws the menu's buttons on screen"""
        for button in self.buttons:
            button.draw(self.screen)

    def handleEvent(self):
        """Handles pygame events and yields it to the calling method"""
        for event in self.screen.getEvent():
            if event.type == MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click(event.pos)

            yield event
