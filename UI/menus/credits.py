import pygame as pg

from src import constantes as constants
from src.runnable import Runnable

from models.game_options import GameOptions

from UI.menus.menu import Menu

from UI.components.button import Button
from UI.components.animation import Animation
from UI.components.credits import Credits


class CreditsMenu(Menu, Runnable):
    """The menu that shows the game's credits"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        options = GameOptions.getInstance()
        self.scroll = 704
        self.buttons["back"] = Button(
            (702, 654),
            (500, 50),
            pg.image.load(options.fullPath("images", "Boutons/MenuButton.png")).convert_alpha(),
            self.back,
        )
        self.buttons["back"].build("Retour", options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        self.credits = Credits("assets/credits.json")

    def loop(self):
        """The bit of code called at each iteration"""
        if self.scroll < 0 - self.credits.height:
            self.back()

        self.draw()
        self.screen.flip()

        self.handleEvent()

    def _draw(self):
        """Draws the buttons/images on screen"""
        self.credits.draw(self.screen, self.scroll)
        self.scroll -= 40 * self.screen.timeElapsed

    def handleEvent(self):
        """Handles the user inputs"""
        for event in super().handleEvent():
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:
                self.back()

            if event.type == pg.locals.MOUSEBUTTONDOWN:
                if event.button == 5:
                    self.scroll -= 40
                elif event.button == 4:
                    self.scroll += 40

    def back(self):
        """Quits the credits menu"""
        anim = Animation("UI/animations/mainToCredits.json", self.screen, pickFrom=self.pickFrom)
        anim.invert()
        anim()
        self.running = False
