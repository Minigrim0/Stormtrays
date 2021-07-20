import pygame

import src.constantes as constantes
from src.runnable import Runnable

from models.gameOptions import GameOptions

from menus.menu import Menu
from menus.levelSelection import LevelSelectMenu
from menus.quit import QuitMenu
from menus.options import OptionMenu
from menus.credits import CreditsMenu

from UI.components.button import Button
from UI.animations.animation import Animation


class MainMenu(Menu, Runnable):
    """The main menu class"""

    def __init__(self, screen, background: callable = None):
        super().__init__(screen, background)
        self.background = pygame.image.load(constantes.fondm).convert_alpha()

        options = GameOptions.getInstance()
        self.buttons.append(
            Button(
                (652, 464),
                (500, 50),
                pygame.image.load("assets/img/Boutons/MenuButton.png").convert_alpha(),
                self.launch,
                toLaunch="game",
            )
        )
        self.buttons[-1].build("Jouer", options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        self.buttons.append(
            Button(
                (752, 584),
                (500, 50),
                pygame.image.load("assets/img/Boutons/MenuButton.png").convert_alpha(),
                self.launch,
                toLaunch="options",
            )
        )
        self.buttons[-1].build("Options", options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        self.buttons.append(
            Button(
                (702, 524),
                (500, 50),
                pygame.image.load("assets/img/Boutons/MenuButton.png").convert_alpha(),
                self.launch,
                toLaunch="credits",
            )
        )
        self.buttons[-1].build("Credits", options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        self.buttons.append(
            Button(
                (802, 644),
                (500, 50),
                pygame.image.load("assets/img/Boutons/MenuButton.png").convert_alpha(),
                self.launch,
                toLaunch="quit",
            )
        )
        self.buttons[-1].build("Quitter", options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

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
            Animation("UI/animations/mainToSelect.json", self.screen)()
            LevelSelectMenu(self.screen, self._draw)()
        elif toLaunch == "quit":
            quitMenu = QuitMenu(self.screen, self._draw)
            if quitMenu() == "q":
                self.running = False
        elif toLaunch == "options":
            Animation("UI/animations/mainToOptions.json", self.screen)()
            OptionMenu(self.screen, self._draw)()
        elif toLaunch == "credits":
            Animation("UI/animations/mainToCredits.json", self.screen)()
            CreditsMenu(self.screen, self._draw)()
        else:
            print(f"Launching {toLaunch}")
