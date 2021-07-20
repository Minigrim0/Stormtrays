import pygame as pg

import src.constantes as constants

from models.gameOptions import GameOptions

from UI.menus.menu import Menu
from src.runnable import Runnable

from UI.components.button import Button
from UI.animations.animation import Animation


class OptionMenu(Menu, Runnable):
    """The menu of options"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = pg.image.load(constants.fondm).convert_alpha()
        self.Fond_Menu_Opt = pg.image.load(constants.Fond_Menu_Opti).convert_alpha()
        self.OptionsTxt = pg.image.load(constants.OptionsTxt__).convert_alpha()

        options = GameOptions.getInstance()

        self.Diffictxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Difficulté : {}".format(options.difficulty), 1, (0, 0, 0)
        )
        self.Volumetxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Volume : {}".format(int(options.volume * 10)), 1, (0, 0, 0)
        )

        Moins = pg.image.load(constants.Moins__).convert_alpha()
        Plus = pg.image.load(constants.Plus__).convert_alpha()

        self.buttons["lessVolume"] = Button((655, 302), (40, 40), Moins, self.updateVolume, -1)
        self.buttons["moreVolume"] = Button((705, 302), (40, 40), Plus, self.updateVolume, 1)
        self.buttons["lessDifficulty"] = Button((655, 347), (40, 40), Moins, self.updateDifficulty, -1)
        self.buttons["moreDifficulty"] = Button((705, 347), (40, 40), Plus, self.updateDifficulty, 1)
        self.buttons["quitOptions"] = Button(
            (516, 407), (120, 50), pg.image.load(constants.quitpaus).convert_alpha(), self.quitMenu
        )

        self.buttons["play"] = Button((1102, 464), (500, 50), self.pickFromBase["play"])
        self.buttons["credits"] = Button((1102, 524), (500, 50), self.pickFromBase["credits"])
        self.buttons["options"] = Button((1002, 584), (500, 50), self.pickFromBase["options"])
        self.buttons["quit"] = Button((1102, 644), (500, 50), self.pickFromBase["quit"])

    def loop(self):
        """The bit of code called at each iteration"""
        super().loop()

        self.draw()
        self.screen.flip()

        self.handleEvent()

    def _draw(self):
        """Draws the buttons/images on screen, called by Menu class, in between background and buttons"""
        self.screen.blit(self.Fond_Menu_Opt, (386, 142))
        self.screen.blit(self.OptionsTxt, (386, 132))
        self.screen.blit(self.Volumetxt, (410, 302))
        self.screen.blit(self.Diffictxt, (410, 347))

    def handleEvent(self):
        """Handles user inputs"""
        for _ in super().handleEvent():
            pass

    def updateDifficulty(self, value: int):
        """Updates the difficulty of the game"""
        GameOptions.getInstance().changeDifficulty(value)
        options = GameOptions.getInstance()

        self.Diffictxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Difficulté : {}".format(options.difficulty), 1, (0, 0, 0)
        )

    def updateVolume(self, value: int):
        """Updates the volume of the music"""
        GameOptions.getInstance().changeVolume(value)
        options = GameOptions.getInstance()

        self.Volumetxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Volume : {}".format(int(options.volume * 10)), 1, (0, 0, 0)
        )

    def quitMenu(self):
        """Quits the option menu"""
        anim = Animation("UI/animations/mainToOptions.json", self.screen, pickFrom=self.pickFrom)
        anim.invert()
        anim()
        self.running = False
