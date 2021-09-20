from gettext import gettext as _

import pygame as pg

from models.game_options import GameOptions
from models.screen import Screen
from src.runnable import Runnable
from UI.components.button import Button
from UI.menus.menu import Menu


class QuitMenu(Menu, Runnable):
    """A menu for the user to confirm his choice to quit the game"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._build()

        self.toReturn: str = None  # Either "q" or "c"

    def __call__(self, *args, **kwargs) -> str:
        super().__call__(*args, **kwargs)
        return self.toReturn

    def _build(self):
        """Builds the menu's background and buttons"""
        options = GameOptions.getInstance()

        self.buttons["reprise"] = Button(
            (516, 297), (120, 50),
            image=pg.image.load(options.fullPath("images", "buttons/small_button.png")).convert_alpha(),
            callback=self.cancel
        )
        self.buttons["reprise"].build(
            _("quit_menu_resume"), options.fonts["MedievalSharp-xOZ5"]["20"],
            text_position=("CENTER", "CENTER")
        )

        self.buttons["confirmQuit"] = Button(
            (516, 367), (120, 50),
            image=pg.image.load(options.fullPath("images", "buttons/small_button.png")).convert_alpha(),
            callback=self.confirm
        )
        self.buttons["confirmQuit"].build(
            _("quit_menu_quit"), options.fonts["MedievalSharp-xOZ5"]["25"],
            text_position=("CENTER", "CENTER")
        )

        self.menu_background = pg.image.load(
            options.fullPath("images", "backgrounds/submenu_background.png")
        ).convert_alpha()
        self.menu_background_position = (
            (Screen.getInstance().get_size()[0] - self.menu_background.get_size()[0]) / 2,
            (Screen.getInstance().get_size()[1] - self.menu_background.get_size()[1]) / 2
        )

        title = options.fonts["MedievalSharp-xOZ5"]["60"].render(
            _("quit_menu_askquit"), 1, (0, 0, 0)
        )

        title_pos = (self.menu_background.get_size()[0] - title.get_size()[0]) / 2

        self.menu_background.blit(
            title,
            (title_pos, 15)
        )

    def loop(self):
        """The bit of code called at each iteration"""
        super().loop()

        self.draw()
        self.handleEvent()

        self.screen.flip()

    def _draw(self):
        """Draws the buttons/images on screen and refreshes it"""
        self.screen.blit(self.menu_background, self.menu_background_position)

    def handleEvent(self):
        """Handles the user inputs"""
        for event in super().handleEvent():
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:
                self.running = False

    def cancel(self):
        """Callback for when the user decides to get back to the game"""
        self.running = False
        self.toReturn = "c"

    def confirm(self):
        """Callback for when the user decided to quit the game"""
        self.running = False
        self.toReturn = "q"
