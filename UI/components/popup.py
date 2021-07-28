import pygame as pg

from UI.components.button import Button


class Popup:
    def __init__(
        self, position: tuple, background: pg.Surface,
        button_position: tuple, button_size: tuple, button_image: pg.Surface
    ):

        self.buttons: [Button] = []

        self.opened: bool = False
        self.position: tuple = position
        self.background = background

        background_size = self.background.get_size()

        self.button = Button(button_position, button_size, button_image, callback=self.toggleVisibility)
        self.cross_button = Button(
            (self.position[0] + background_size[0] - 15, self.position[1] - 5),
            (20, 20),
            pg.image.load("UI/assets/images/cross.png"),
            callback=self.toggleVisibility
        )

    def addButton(self, button: Button):
        self.buttons.append(button)

    def update(self, timeElapsed):
        pass

    def handleEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

            if self.opened:
                self.cross_button.click(event.pos)
                for button in self.buttons:
                    button.click(event.pos)
            else:
                self.button.click(event.pos)

    def draw(self, screen):
        if self.opened:
            screen.blit(self.background, self.position)
            self.cross_button.draw(screen)
            for button in self.buttons:
                button.draw(screen)
        else:
            self.button.draw(screen)

    def toggleVisibility(self):
        self.opened = not self.opened
