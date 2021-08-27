import pygame as pg

from models.game_options import GameOptions


class Box:
    """Represents a box of the power bar"""

    def __init__(self, icon: pg.Surface, size: int, cooldown: int, callback: callable, **ckwargs):
        self.icon = icon
        self.size = size

        self.initial_cooldown = cooldown
        self.current_cooldown = 0
        self.cooldown_text: pg.Surface = None

        self.callback: callable = callback
        self.ckwargs = ckwargs

    @property
    def available(self) -> bool:
        return self.current_cooldown == 0

    @property
    def _cooldownText(self) -> pg.Surface:
        options = GameOptions.getInstance()
        return options.fonts["MedievalSharp-xOZ5"]["14"].render(
            str(round(self.current_cooldown, 1)), 0, (255, 255, 255)
        )

    def trigger(self):
        if self.available:
            if self.callback(**self.ckwargs):
                self.current_cooldown = self.initial_cooldown

    def update(self, elapsed_time: float):
        if not self.available:
            self.current_cooldown = max(self.current_cooldown - elapsed_time, 0)

    def draw(self, screen, position: tuple):
        screen.blit(self.icon, position)
        if not self.available:
            screen.blit(
                self._cooldownText,
                (
                    position[0] + 2,
                    position[1] + self.size - 15
                )
            )
