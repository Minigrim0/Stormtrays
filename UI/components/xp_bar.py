import pygame as pg

from models.screen import Screen
from models.character import Character
from models.gameOptions import GameOptions

from UI.components.loading_bar import LoadingBar
from UI.components.imageAnimation import ImageAnimation


class XPBar(LoadingBar):
    def __init__(
        self, position: tuple, size: tuple,
        fg_color: tuple = (76, 187, 23), bg_color: tuple = (138, 7, 7),
        overlay: str = None
    ):
        self.setObjective(20)

        super().__init__(
            position,
            size,
            max_val=self.objective,
            fg_color=fg_color,
            bg_color=bg_color
        )

        self.overlay: pg.Surface = None if overlay is None else pg.image.load(overlay).convert_alpha()

        self.overlay_position: tuple = (0, 0)
        if self.overlay is not None:
            overlay_size = self.overlay.get_size()
            self.overlay_position = (
                self.position[0] + ((self.size[0] - overlay_size[0]) // 2),
                self.position[1] + ((self.size[1] - overlay_size[1]) // 2)
            )

        self.font: pg.Font = GameOptions.getInstance().fonts["MedievalSharp-xOZ5"]["14"]
        self.xp_text: pg.Surface = None
        self.text_position: tuple = (0, 0)

        self.level_up_animation: ImageAnimation = ImageAnimation("assets/images/animations/level_up", loop=1, speed=10)
        self.level_up_animation.pause()

        self.stashed: int = 0
        self.add_xp(0)

    def _levelUp(self):
        """Updates the bar's objective"""
        character = Character.getInstance()
        character.level_up()
        self.setObjective((character.level ** 2) * 20)
        self.reset()

        if self.bg_color != (-1, -1, -1):
            self.bg_image = pg.Surface(self.size)
            self.bg_image.fill(self.bg_color)

        stashed = self.stashed
        self.stashed = 0
        self.add_xp(stashed)

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
        self.level_up_animation.update(timeElapsed)
        if self.current_advancement != self.advancement:
            self.xp_text = self.font.render(
                f"{int(self.current_advancement) + 1}/{self.max_advancement}",
                1, (0, 0, 0)
            )

        if self._percentAdvanced >= 1:
            self._levelUp()
            self.level_up_animation.play()

    def draw(self, screen: Screen):
        """Displays the bar and its text on the screen"""
        super().draw(screen)
        screen.blit(self.xp_text, self.text_position)
        if self.overlay is not None:
            screen.blit(self.overlay, self.overlay_position)

        if self.level_up_animation.playing:
            self.level_up_animation.draw(screen, (1152 // 2, 768 // 2), centered=True)

    def add_xp(self, amount: int):
        """Adds a certain amount of xp and update the text/bar in accordance"""
        if self.advancement + amount > self.objective:
            self.stashed += self.advancement + amount - self.objective
            self.set_advancement(self.objective)
        else:
            self.set_advancement(self.advancement + amount)

        text_size = self.xp_text.get_size()
        self.text_position = (
            self.position[0] + ((self.size[0] - text_size[0]) // 2),
            self.position[1] + ((self.size[1] - text_size[1]) // 2)
        )
