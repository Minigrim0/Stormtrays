import pygame as pg

from models.game_options import GameOptions
from models.screen import Screen
from src.runnable import Runnable

from UI.components.button import Button
from UI.menus.menu import Menu


class EndScreen(Menu, Runnable):
    """Represents the screen at the end of the game"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background: pg.Surface = None
        self.menu_background: pg.Surface = None
        self.menu_background_position: tuple = None

        self._build()

    def _build(self):
        """Builds the backgrounds and buttons of the end screen"""
        options: GameOptions = GameOptions.getInstance()

        self.background = pg.Surface((1152, 704), pg.SRCALPHA)
        self.background.fill((0, 0, 0, 128))

        self.menu_background = pg.image.load(
            options.fullPath("images", "backgrounds/submenu_background.png")
        ).convert_alpha()
        self.menu_background_position = (
            (Screen.getInstance().get_size()[0] - self.menu_background.get_size()[0]) / 2,
            (Screen.getInstance().get_size()[1] - self.menu_background.get_size()[1]) / 2
        )

        title = options.fonts["MedievalSharp-xOZ5"]["60"].render(
            "Défaite", 1, (0, 0, 0)
        )

        title_pos = (self.menu_background.get_size()[0] - title.get_size()[0]) / 2

        self.menu_background.blit(
            title,
            (title_pos, 15)
        )

        button_image = pg.image.load(options.fullPath("images", "buttons/small_button.png")).convert_alpha()

        self.buttons["quit"] = Button(
            (516, 387), button_image.get_size(),
            image=button_image,
            callback=self.quitMenu
        )
        self.buttons["quit"].build(
            "Retour", options.fonts["MedievalSharp-xOZ5"]["25"],
            ("CENTER", "CENTER")
        )

    def loop(self):
        """Method called at each code loop"""
        super().loop()

        self.draw()
        self.screen.flip()

        self.handleEvent()

    def _draw(self):
        """Draws the background of the end screen"""
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.menu_background, self.menu_background_position)

    def handleEvent(self):
        """Handles the user's events"""
        for _ in super().handleEvent():  # skipcq PTC-W0047
            pass

    def quitMenu(self):
        """Callback for the quit button"""
        self.running = False
