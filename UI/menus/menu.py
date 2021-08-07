from pygame.locals import MOUSEBUTTONDOWN

from models.screen import Screen
from UI.components.button import Button


class Menu:
    """The base class for all menus"""

    def __init__(self, screen: Screen, pickFrom: dict = {}, background: callable = None, **background_kwargs):
        self.buttons: {Button} = {}
        self.pickFromBase = pickFrom
        self.screen = screen
        self.backgroundCallback: callable = background
        self.background_kwargs = background_kwargs

    @staticmethod
    def loop():
        """Plays music if needed"""
        from models.stormtrays import Stormtrays

        Stormtrays.getInstance().playMusic()

    @property
    def pickFrom(self):
        return self.pickFromBase | {key: self.buttons[key].image for key in self.buttons.keys()}

    def draw(self):
        """Draws the menu's buttons on screen"""
        if self.backgroundCallback is not None:
            self.backgroundCallback(**self.background_kwargs)

        self._draw()

        for button in self.buttons.values():
            button.draw(self.screen)

    def handleEvent(self):
        """Handles pygame events and yields it to the calling method"""
        for event in self.screen.getEvent():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons.values():
                    button.click(event.pos)

            yield event

    def _draw(self):
        raise NotImplementedError()
