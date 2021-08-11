import pygame as pg

from models.character import Character
from models.game_options import GameOptions
from models.screen import Screen
from UI.components.image_animation import ImageAnimation
from UI.components.loading_bar import LoadingBar


class XPBar(LoadingBar):
    """Represents the user's XP bar, with an objective update on level up"""

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

    @property
    def objective(self) -> int:
        """Hides the real variable behind objective"""
        return self.max_advancement

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

    def _genText(self):
        """Generates the text in the XP bar"""
        self.xp_text = self.font.render(
            f"{int(self.current_advancement)}/{self.max_advancement}",
            1, (0, 0, 0)
        )

        text_size = self.xp_text.get_size()
        self.text_position = (
            self.position[0] + ((self.size[0] - text_size[0]) // 2),
            self.position[1] + ((self.size[1] - text_size[1]) // 2)
        )

    def setObjective(self, amount: int):
        """Sets the value of the hidden max_advancement variable"""
        self.max_advancement = amount

    def update(self, elapsed_time: float):
        """Updates the bar"""
        super().update(elapsed_time)
        self.level_up_animation.update(elapsed_time)
        if self.current_advancement != self.advancement:
            self._genText()

        if self._percentAdvanced >= 1:
            self._levelUp()
            self.level_up_animation.play()

    def draw(self, screen: Screen):  # skipcq PYL-W0221
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
        self._genText()

    def resetBar(self):
        """Resets the bar to its default values"""
        self.setObjective(20)
        self.stashed = 0
        self.current_advancement = 0
        self.advancement = 0
        self.old_advancement = 0
        self._genText()
