import math as m

import pygame as pg

from models.screen import Screen


class LoadingBar:
    """A loading bar"""

    def __init__(
        self, pos: tuple, size: tuple, max_val: int = 100, initial_val: int = 0,
        fg_color: tuple = (76, 187, 23), bg_color: tuple = (138, 7, 7),
        animation_type="sine", speed=1
    ):
        self.position = pos
        self.size = size

        self.current_advancement: int = initial_val
        self.old_advancement: int = initial_val
        self.advancement: int = initial_val
        self.max_advancement: int = max_val
        self.time: int = 0

        self.fg_color = fg_color
        self.bg_color = bg_color

        self.fg_image: pg.Surface = None

        if self.bg_color == (-1, -1, -1):
            self.bg_image = None
        else:
            self.bg_image = pg.Surface(self.size)
            self.bg_image.fill(self.bg_color)

        self.animation_type = animation_type  # Either sine, linear or none
        self.speed = speed  # When animation = sine represents the time the animation will take (Otherwise the speed)

        self._buildImage(force=True)

    @property
    def _percentAdvanced(self) -> float:
        """Returns the filling rate of the bar"""
        return self.current_advancement / self.max_advancement

    @property
    def moving_speed(self) -> float:
        """Returns the in/decrease speed of the bar"""
        if self.animation_type == "sine":
            A_x = self.advancement - self.old_advancement

            wt = (self.time * 2) * m.pi

            # First derivative of the position A(x - sin(pi * x) / pi)
            return A_x * (1 - m.cos(wt))
        elif self.animation_type == "linear":
            return self.speed * (-1) ** (self.advancement < self.current_advancement)
        else:
            return 0

    def _buildImage(self, force: bool = False):
        """Builds the foreground image if the moving_speed is not null"""
        if self.size[0] > 0 or (force and int(self._percentAdvanced) > 0):
            self.fg_image = pg.Surface((int(self._percentAdvanced * self.size[0]) + 1, self.size[1]))
            self.fg_image.fill(self.fg_color)

    def reset(self):
        """Resets the advancement of the bar"""
        self.current_advancement = 0
        self.advancement = 0
        self.old_advancement = 0
        self.time = 0

    def set_advancement(self, advancement: int):
        """Sets the advancement of the loading"""
        self.old_advancement = self.advancement
        self.advancement = advancement
        self.time = 0
        if self.animation_type == "none":
            self.current_advancement = advancement
            self.old_advancement = advancement

    def update(self, elapsed_time: int):
        """Updates the bar according to its advancement"""
        if self.old_advancement != self.advancement:
            self.time += elapsed_time

            speed = self.moving_speed
            if (
                abs(speed) > 1e-3 and
                abs(self.current_advancement - self.advancement) > abs(
                    (self.current_advancement + speed * elapsed_time) - self.advancement
                )
            ):
                self.current_advancement += speed * elapsed_time
                self._buildImage()
            else:
                self.current_advancement = self.advancement
                self.old_advancement = self.advancement
                self.time = 0

    def draw(self, screen: Screen, position: tuple = None):
        """Draws the bar on the screen"""
        position = position if position is not None else self.position
        if self.bg_image is not None:
            screen.blit(self.bg_image, position)
        if self.advancement > 0 and self.fg_image is not None:
            screen.blit(self.fg_image, position)

    def move(self, new_pos: tuple):
        """Moves the bar to a new location"""
        self.position = new_pos
