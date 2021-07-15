from pygame.locals import MOUSEBUTTONDOWN

from UI.components.button import Button
from models.screen import Screen


class Menu:
    def __init__(self, screen: Screen):
        self.buttons: [Button] = []
        self.screen = screen

    def handleEvent(self):
        for event in self.screen.getEvent():
            if event.type == MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click(event.pos)

            yield event

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)

    def loop(self):
        from models.game import Game

        Game.getInstance().playMusic()
