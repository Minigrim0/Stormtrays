import pygame as pg

from models.game_options import GameOptions
from models.screen import Screen
from src.runnable import Runnable
from UI.components.button import Button
from UI.menus.menu import Menu


class GameOptionsMenu(Menu, Runnable):
    """Represents the in game option menu"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu_background: pg.Surface = None
        self.menu_background_position: tuple = None

        self.volume_text: pg.Surface = None
        self.difficulty_text: pg.Surface = None

        self.background: pg.Surface = None

        self._build()

    def _build(self):
        """Builds the menu's buttons and texts"""
        options = GameOptions.getInstance()
        _ = options.get_lang()

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
            _("menuOptions_options"), 1, (0, 0, 0)
        )

        title_pos = (self.menu_background.get_size()[0] - title.get_size()[0]) / 2

        self.menu_background.blit(
            title,
            (title_pos, 15)
        )

        less = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "-", 1, (0, 0, 0)
        )
        plus = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "+", 1, (0, 0, 0)
        )

        self.buttons["lessVolume"] = Button((655, 302), (40, 40), image=less, callback=self.updateVolume, value=-1)
        self.buttons["moreVolume"] = Button((705, 302), (40, 40), image=plus, callback=self.updateVolume, value=1)
        self.buttons["lessDifficulty"] = Button(
            (655, 347), (40, 40), image=less, callback=self.updateDifficulty, value=-1)
        self.buttons["moreDifficulty"] = Button(
            (705, 347), (40, 40), image=plus, callback=self.updateDifficulty, value=1)
        self.buttons["quitOptions"] = Button(
            (516, 407), (120, 50),
            image=pg.image.load(options.fullPath("images", "buttons/small_button.png")).convert_alpha(),
            callback=self.quitMenu
        )
        self.buttons["quitOptions"].build(
            _("menuOptions_back"), options.fonts["MedievalSharp-xOZ5"]["25"],
            text_position=("CENTER", "CENTER")
        )

        self._buildVolumeText()
        self._buildDifficultyText()

    def _buildVolumeText(self):
        """Builds the text for the volume option"""
        options = GameOptions.getInstance()
        self.volume_text = options.fonts["MedievalSharp-xOZ5"]["25"].render(
            _("menuOptions_volume").format(int(options.volume * 10)),
            1, (0, 0, 0)
        )

    def _buildDifficultyText(self):
        """Builds the text for the difficulty option"""
        options = GameOptions.getInstance()
        self.difficulty_text = options.fonts["MedievalSharp-xOZ5"]["25"].render(
            _("menuOptions_difficulty").format(options.difficulty),
            1, (0, 0, 0)
        )

    def loop(self):
        """Method called at each code's loop"""
        super().loop()

        self.draw()
        self.screen.flip()

        self.handleEvent()

    def _draw(self):
        """Draws the menu's background"""
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.menu_background, self.menu_background_position)
        self.screen.blit(self.volume_text, (410, 302))
        self.screen.blit(self.difficulty_text, (410, 347))

    def handleEvent(self):
        """Handles the user's events"""
        for event in super().handleEvent():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False

    def updateVolume(self, value: int):
        """Updates the volume of the music"""
        GameOptions.getInstance().changeVolume(value)
        self._buildVolumeText()

    def updateDifficulty(self, value: int):
        """Updates the difficulty of the game"""
        GameOptions.getInstance().changeDifficulty(value)
        self._buildDifficultyText()

    def quitMenu(self):
        """Callback for the quit button"""
        self.running = False
