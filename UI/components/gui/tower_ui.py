import pygame as pg

from models.game_options import GameOptions
from src.tower import TowerDO
from UI.components.button import Button


class TowerUI:
    """Represents the small UI appearing when a tower is selected"""

    instance = None

    @staticmethod
    def getInstance():
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
            "Vendre", self.font,
            text_position=("CENTER", "CENTER"), text_color=(0, 0, 0)
        )

    def _buildText(self):
        """Builds the text of the tower stats"""
        self.damage_text = self.font.render(f"dégâts: {self.tower.damage}", 1, (0, 0, 0))
        self.kills_text = self.font.render(f"Victimes: {self.tower.kills}", 1, (0, 0, 0))
        self.total_damage_text = self.font.render(f"Dégâts totaux: {self.tower.damage_dealt}", 1, (0, 0, 0))

    def _sell(self):
        """Sells the currently selected tower"""
        if self.tower is not None:
            self.tower.sell()
            self.opened = False
            self.tower = None

    def open(self):
        self.opened = True

    def close(self):
        self.opened = False

    def setTower(self, tower: TowerDO):
        self.tower = tower
        self._buildText()

    def update(self, elapsed_time: float):
        if self.opened and self.tower is not None:
            self._buildText()

    def draw(self, screen):
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
                self.tower.position, self.tower.range * options.tile_size,
                width=2
            )

    def handleEvent(self, event):
        self.button.click(event.pos)
