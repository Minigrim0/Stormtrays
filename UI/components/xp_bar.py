import pygame as pg

from models.screen import Screen
from models.character import Character
from models.gameOptions import GameOptions

from UI.components.loading_bar import LoadingBar


class XPBar(LoadingBar):
    def __init__(self, position: tuple, size: tuple, fg_color: tuple = (76, 187, 23), bg_color: tuple = (138, 7, 7)):
        self.setObjective(20)

        super().__init__(
            position,
            size,
            max_val=self.objective,
            fg_color=fg_color,
            bg_color=bg_color
        )

        self.font = GameOptions.getInstance().fonts["MedievalSharp-xOZ5"]["14"]
        self.xp_text: pg.Surface = None
        self.text_position: tuple = (0, 0)

        self.stashed = 0
        self.add_xp(0)

    @property
    def objective(self) -> int:
        """Hides the real variable behind objective"""
        return self.max_advancement

    def setObjective(self, amount: int):
        """Sets the value of the hidden max_advancement variable"""
        self.max_advancement = amount

    def update(self, timeElapsed: float):
        """Updates the bar"""
        super().update(timeElapsed)
        if self._percentAdvanced == 1:
            character = Character.getInstance()
            character.level_up()
            self.setObjective((character.level ** 2) * 20)
            self.set_advancement(0)

            if self.bg_color != (-1, -1, -1):
                self.bg_image = pg.Surface(self.size)
                self.bg_image.fill(self.bg_color)

    def draw(self, screen: Screen):
        """Displays the bar and its text on the screen"""
        super().draw(screen)
        screen.blit(self.xp_text, self.text_position)

    def add_xp(self, amount: int):
        """Adds a certain amount of xp and update the text/bar in accordance"""
        if self.advancement + amount > self.objective:
            self.stashed += self.advancement - self.objective
            self.set_advancement(self.objective)
        else:
            self.set_advancement(self.advancement + amount)
        self.xp_text = self.font.render(
            f"{self.advancement}/{self.max_advancement}",
            1, (0, 0, 0)
        )

        text_size = self.xp_text.get_size()
        self.text_position = (
            self.position[0] + ((self.size[0] - text_size[0]) // 2),
            self.position[1] + ((self.size[1] - text_size[1]) // 2)
        )
