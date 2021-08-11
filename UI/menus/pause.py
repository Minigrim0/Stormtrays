from copy import copy

import pygame as pg

from models.game_options import GameOptions
from models.screen import Screen
from src.runnable import Runnable
from UI.components.button import Button
from UI.menus.menu import Menu
from UI.menus.options_game import GameOptionsMenu


class PauseMenu(Menu, Runnable):
    """Represents the in game pause menu"""

    def __init__(self, *args, **kwargs):
        super().__init__(Screen.getInstance(), *args, **kwargs)

        options = GameOptions.getInstance()

        self.background = pg.Surface((1152, 704), pg.SRCALPHA)
        self.background.fill((0, 0, 0, 128))

        self.menu_background = pg.image.load(
            options.fullPath("images", "backgrounds/submenu_background.png")
        ).convert_alpha()
        self.menu_background_position = (
            (Screen.getInstance().get_size()[0] - self.menu_background.get_size()[0]) / 2,
            (Screen.getInstance().get_size()[1] - self.menu_background.get_size()[1]) / 2
        )
        self._build()

    def _build(self):
        options = GameOptions.getInstance()

        title = options.fonts["MedievalSharp-xOZ5"]["60"].render(
            "Pause", 1, (0, 0, 0)
        )

        title_pos = (self.menu_background.get_size()[0] - title.get_size()[0]) / 2

        self.menu_background.blit(
            title,
            (title_pos, 15)
        )

        button_image = pg.image.load(options.fullPath("images", "buttons/small_button.png")).convert_alpha()

        self.buttons["reprise"] = Button(
            ((1152 - button_image.get_size()[0]) // 2, 300), button_image.get_size(),
            image=copy(button_image),
            callback=self.resume
        )
        self.buttons["options"] = Button(
            ((1152 - button_image.get_size()[0]) // 2, 350), button_image.get_size(),
            image=copy(button_image),
            callback=self.options_menu
        )
        self.buttons["quit"] = Button(
            ((1152 - button_image.get_size()[0]) // 2, 400), button_image.get_size(),
            image=copy(button_image),
            callback=self.quit_game
        )

        self.buttons["reprise"].build(
            "Reprendre", options.fonts["MedievalSharp-xOZ5"]["25"],
            text_position=("CENTER", "CENTER")
        )
        self.buttons["options"].build(
            "Options", options.fonts["MedievalSharp-xOZ5"]["25"],
            text_position=("CENTER", "CENTER")
        )
        self.buttons["quit"].build(
            "Quitter", options.fonts["MedievalSharp-xOZ5"]["25"],
            text_position=("CENTER", "CENTER")
        )

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.menu_background, self.menu_background_position)

    def loop(self):
        """The bit of code called at each iteration"""
        super().loop()

        self.draw()
        self.screen.flip()

        self.handleEvent()

    def handleEvent(self):
        for event in super().handleEvent():  # skipcq PTC-W0047
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False

    def resume(self):
        self.running = False

    def options_menu(self):
        GameOptionsMenu(self.screen, background=self.backgroundCallback)()

    def quit_game(self):
        from models.game import Game
        Game.getInstance().running = False
        self.running = False
