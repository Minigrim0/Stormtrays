import pygame

import src.constantes as constantes
from src.runnable import Runnable

from models.gameOptions import GameOptions

from UI.menus.menu import Menu
from UI.menus.levelSelection import LevelSelectMenu
from UI.menus.quit import QuitMenu
from UI.menus.options import OptionMenu
from UI.menus.credits import CreditsMenu

from UI.components.button import Button
from UI.components.animation import Animation


class MainMenu(Menu, Runnable):
    """The main menu class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = pygame.image.load(constantes.fondm).convert_alpha()

        options = GameOptions.getInstance()
        self.buttons["play"] = Button(
            (652, 464),
            (500, 50),
            pygame.image.load("assets/img/Boutons/MenuButton.png").convert_alpha(),
            self.launch,
            toLaunch="game",
        )
        self.buttons["play"].build("Jouer", options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        self.buttons["options"] = Button(
            (752, 584),
            (500, 50),
            pygame.image.load("assets/img/Boutons/MenuButton.png").convert_alpha(),
            self.launch,
            toLaunch="options",
        )
        self.buttons["options"].build("Options", options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        self.buttons["credits"] = Button(
            (702, 524),
            (500, 50),
            pygame.image.load("assets/img/Boutons/MenuButton.png").convert_alpha(),
            self.launch,
            toLaunch="credits",
        )
        self.buttons["credits"].build("Credits", options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        self.buttons["quit"] = Button(
            (802, 644),
            (500, 50),
            pygame.image.load("assets/img/Boutons/MenuButton.png").convert_alpha(),
            self.launch,
            toLaunch="quit",
        )
        self.buttons["quit"].build("Quitter", options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

    def loop(self):
        """The bit of code called at each iteration"""
        super().loop()

        self.draw()
        self.screen.flip()

        self.handleEvent()

    def _draw(self):
        """Draws the buttons/images on screen"""
        self.screen.blit(self.background, (0, 0))

    def handleEvent(self):
        """Handles the user inputs"""
        for event in super().handleEvent():
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                self.launch("quit")

    def launch(self, toLaunch: str):
        """Callback for the buttons

        Args:
            toLaunch (str): The argument describing the button that's been pressed and what should be launched
        """

        if toLaunch == "game":
            Animation("UI/animations/mainToSelect.json", self.screen, pickFrom=self.pickFrom)()
            LevelSelectMenu(self.screen, self._draw, pickFrom=self.pickFrom)()
        elif toLaunch == "quit":
            quitMenu = QuitMenu(self.screen, self._draw)
            if quitMenu() == "q":
                self.running = False
        elif toLaunch == "options":
            Animation("UI/animations/mainToOptions.json", self.screen, pickFrom=self.pickFrom)()
            OptionMenu(self.screen, self._draw, pickFrom=self.pickFrom)()
        elif toLaunch == "credits":
            Animation("UI/animations/mainToCredits.json", self.screen, pickFrom=self.pickFrom)()
            CreditsMenu(self.screen, self._draw, pickFrom=self.pickFrom)()
