from gettext import gettext as _

import pygame

from models.game_options import GameOptions
from src.runnable import Runnable
from UI.components.animation import Animation
from UI.components.button import Button
from UI.menus.credits import CreditsMenu
from UI.menus.levelSelection import LevelSelectMenu
from UI.menus.menu import Menu
from UI.menus.options import OptionMenu
from UI.menus.quit import QuitMenu


class MainMenu(Menu, Runnable):
    """The main menu class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        options = GameOptions.getInstance()

        self.background = pygame.image.load(
            f"{options['paths']['images']}backgrounds/main_background.png").convert_alpha()
        self.title = options.fonts["MedievalSharp-xOZ5"]["60"].render(
            "StormTrays",
            1,
            (0, 0, 0)
        )
        self._build()

    def _build(self):
        """Builds the menu's buttons"""
        options = GameOptions.getInstance()

        self.buttons["play"] = Button(
            (652, 464),
            (500, 50),
            image=pygame.image.load(f"{options['paths']['images']}buttons/MenuButton.png").convert_alpha(),
            callback=self.launch,
            toLaunch="game",
        )
        self.buttons["play"].build(_("mainMenu_play_button"), options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        self.buttons["options"] = Button(
            (752, 584),
            (500, 50),
            image=pygame.image.load(f"{options['paths']['images']}buttons/MenuButton.png").convert_alpha(),
            callback=self.launch,
            toLaunch="options",
        )
        self.buttons["options"].build(_("mainMenu_options_button"), options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        self.buttons["credits"] = Button(
            (702, 524),
            (500, 50),
            image=pygame.image.load(f"{options['paths']['images']}buttons/MenuButton.png").convert_alpha(),
            callback=self.launch,
            toLaunch="credits",
        )
        self.buttons["credits"].build(_("mainMenu_credits_button"), options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        self.buttons["quit"] = Button(
            (802, 644),
            (500, 50),
            image=pygame.image.load(f"{options['paths']['images']}buttons/MenuButton.png").convert_alpha(),
            callback=self.launch,
            toLaunch="quit",
        )
        self.buttons["quit"].build(_("mainMenu_quit_button"), options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

    def loop(self):
        """The bit of code called at each iteration"""
        super().loop()

        self.draw()
        self.screen.flip()

        self.handleEvent()

    def _draw(self, draw_title=True):  # skipcq PYL-W0221
        """Draws the buttons/images on screen"""
        self.screen.blit(self.background, (0, 0))
        if draw_title:
            self.screen.blit(self.title, (50, 50))

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
            Animation("UI/animations/mainToSelect.json", self.screen, pickFrom=self.pickFrom, background=self._draw)()
            LevelSelectMenu(self.screen, pickFrom=self.pickFrom, background=self._draw)()
        elif toLaunch == "quit":
            quitMenu = QuitMenu(self.screen, background=self._draw)
            if quitMenu() == "q":
                self.running = False
        elif toLaunch == "options":
            Animation("UI/animations/mainToOptions.json", self.screen, pickFrom=self.pickFrom, background=self._draw)()
            OptionMenu(self.screen, pickFrom=self.pickFrom, background=self._draw)()
        elif toLaunch == "credits":
            Animation("UI/animations/mainToCredits.json", self.screen, pickFrom=self.pickFrom, background=self._draw)()
            CreditsMenu(self.screen, pickFrom=self.pickFrom, background=self._draw, draw_title=False)()
