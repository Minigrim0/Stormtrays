import pygame as pg

import src.constantes as constants

from models.gameOptions import GameOptions

from menus.menu import Menu
from src.runnable import Runnable

from UI.components.button import Button


class OptionMenu(Menu, Runnable):
    """The menu of options"""

    def __init__(self, screen):
        super().__init__(screen)

        self.background = pg.image.load(constants.fondm).convert_alpha()
        self.Fond_Menu_Opt = pg.image.load(constants.Fond_Menu_Opti).convert_alpha()
        self.OptionsTxt = pg.image.load(constants.OptionsTxt__).convert_alpha()

        options = GameOptions.getInstance()

        self.Diffictxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Difficulté : {}".format(options.difficulty), 1, (255, 50, 20))
        self.Volumetxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Volume : {}".format(int(options.volume * 10)), 1, (255, 50, 20))

        Moins = pg.image.load(constants.Moins__).convert_alpha()
        Plus = pg.image.load(constants.Plus__).convert_alpha()

        self.buttons.append(
            Button(
                (655, 302), (40, 40),
                Moins, self.updateVolume, -1
            )
        )
        self.buttons.append(
            Button(
                (705, 302), (40, 40),
                Plus, self.updateVolume, 1
            )
        )
        self.buttons.append(
            Button(
                (655, 347), (40, 40),
                Moins, self.updateDifficulty, -1
            )
        )
        self.buttons.append(
            Button(
                (705, 347), (40, 40),
                Plus, self.updateDifficulty, 1
            )
        )
        self.buttons.append(
            Button(
                (516, 407), (120, 50),
                pg.image.load(constants.quitpaus).convert_alpha(), self.quitMenu
            )
        )

    def loop(self):
        """The bit of code called at each iteration"""
        self.draw()
        self.handleEvent()
        self.screen.flip()

    def draw(self):
        """Draws the buttons/images on screen"""
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.Fond_Menu_Opt, (386, 142))
        self.screen.blit(self.OptionsTxt, (386, 132))
        self.screen.blit(self.Volumetxt, (410, 302))
        self.screen.blit(self.Diffictxt, (410, 347))

        super().draw()

    def handleEvent(self):
        """Handles user inputs"""
        for _ in super().handleEvent():
            pass

    def updateDifficulty(self, value: int):
        """Updates the difficulty of the game"""
        GameOptions.getInstance().changeDifficulty(value)
        options = GameOptions.getInstance()

        self.Diffictxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Difficulté : {}".format(options.difficulty), 1, (255, 50, 20))

    def updateVolume(self, value: int):
        """Updates the volume of the music"""
        GameOptions.getInstance().changeVolume(value)
        options = GameOptions.getInstance()

        self.Volumetxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Volume : {}".format(int(options.volume * 10)), 1, (255, 50, 20))

    def quitMenu(self):
        """Quits the option menu"""
        self.running = False
