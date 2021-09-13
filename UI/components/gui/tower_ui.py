from gettext import gettext as _

import pygame as pg

from models.game_options import GameOptions
from src.tower import TowerDO
from UI.components.button import Button


class TowerUI:
    """Represents the small UI appearing when a tower is selected"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the one and only instance of the TowerUI"""
        if TowerUI.instance is None:
            TowerUI()
        return TowerUI.instance

    def __init__(self):
        if TowerUI.instance is not None:
            raise RuntimeError("Trying to instanciate second class from singleton")
        TowerUI.instance = self

        self.tower: TowerDO = None
        self.opened: bool = False

        self.background: pg.Surface = None
        self.button: Button = None
        self.position: tuple = (0, 0)

        self.font: pg.Font = None
        self.damage_text: pg.Surface = None
        self.total_damage_text: pg.Surface = None
        self.kills_text: pg.Surface = None

        self._build()

    def _build(self):
        """Loads the background image and build the selling button"""
        options = GameOptions.getInstance()
        self.background = pg.image.load(options.fullPath("images", "overlays/stats_background.png"))
        self.position = tuple(map(lambda i, j: i - j, options.window_size, self.background.get_size()))

        button_image = pg.image.load(options.fullPath("images", "buttons/small_button.png")).convert_alpha()
        self.button = Button(
            tuple(map(lambda i, j, k: i + j - k, self.position, self.background.get_size(), button_image.get_size())),
            button_image.get_size(),
            image=button_image,
            callback=self._sell
        )
        self.font = options.fonts["MedievalSharp-xOZ5"]["20"]
        self.button.build(
            -("tower_sell"), self.font,
            text_position=("CENTER", "CENTER"), text_color=(0, 0, 0)
        )

    def _buildText(self):
        """Builds the text of the tower stats"""
        self.damage_text = self.font.render(_("tower_damage").format(self.tower.damage), 1, (0, 0, 0))
        self.kills_text = self.font.render(_("tower_victims").format(self.tower.kills), 1, (0, 0, 0))
        self.total_damage_text = self.font.render(_("tower_totalDamage").format(self.tower.damage_dealt), 1, (0, 0, 0))

    def _sell(self):
        """Sells the currently selected tower"""
        if self.tower is not None:
            self.tower.sell()
            self.opened = False
            self.tower = None

    def open(self):
        """Opens the UI"""
        self.opened = True

    def close(self):
        """Closes the UI"""
        self.opened = False

    def setTower(self, tower: TowerDO):
        """Sets the selected tower"""
        if self.tower is not None:
            self.tower.unselect()
        self.tower = tower
        self._buildText()

    def unsetTower(self, tower: TowerDO):
        """Closes and unset the tower if the given tower is the selected one"""
        if self.tower == tower:
            self.tower = None
            self.opened = False

    def update(self, _elapsed_time: float):
        """Rebuilds the UI text"""
        if self.opened and self.tower is not None:
            self._buildText()

    def draw(self, screen):
        """Draws the tower UI on screen"""
        if self.opened and self.tower is not None:
            options = GameOptions.getInstance()

            screen.blit(self.background, self.position)
            self.button.draw(screen)
            screen.blit(self.kills_text, (self.position[0] + 2, self.position[1] + 2))
            screen.blit(self.damage_text, (self.position[0] + 2, self.position[1] + 30))
            screen.blit(self.total_damage_text, (self.position[0] + 2, self.position[1] + 60))

            pg.draw.circle(
                screen.fenetre,
                (128, 0, 0),
                self.tower.centered_position, self.tower.range * options.tile_size,
                width=2
            )

    def handleEvent(self, event):
        """Handles click on the UI's button"""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.button.click(event.pos)
