import pygame as pg

from models.screen import Screen


class LoadingBar:
    """A loading bar"""

    def __init__(
        self, pos: tuple, size: tuple, max_val: int = 100, initial_val: int = 0,
        fg_color: tuple = (76, 187, 23), bg_color: tuple = (138, 7, 7)
    ):
        self.position = pos
        self.size = size

        self.current_advancement = initial_val
        self.advancement = initial_val
        self.max_advancement = max_val

        self.fg_color = fg_color
        self.bg_color = bg_color

        self.fg_image: pg.Surface = None

        if self.bg_color == (-1, -1, -1):
            self.bg_image = None
        else:
            self.bg_image = pg.Surface(self.size)
            self.bg_image.fill(self.bg_color)

        self._buildImage(force=True)

    def _buildImage(self, force: bool = False):
        """Builds the foreground image if the moving_speed is not null"""
        if self.moving_speed != 0 or (force and self._percentAdvanced > 0):
            self.fg_image = pg.Surface((int(self._percentAdvanced * self.size[0]), self.size[1]))
            self.fg_image.fill(self.fg_color)

    @property
    def _percentAdvanced(self) -> float:
        return self.current_advancement / self.max_advancement

    def set_advancement(self, advancement: int):
        """Sets the advancement of the loading"""
        self.advancement = advancement

    @property
    def moving_speed(self) -> int:
        return self.advancement - self.current_advancement

    def update(self, timeElapsed: int):
        """Updates the bar according to its advancement"""
        if abs(self.moving_speed) > 2:
            self.current_advancement += self.moving_speed * timeElapsed
            self._buildImage()
        else:
            self.current_advancement = self.advancement

    def draw(self, screen: Screen, position: tuple = None):
        """Draws the bar on the screen"""
        position = position if position is not None else self.position
        if self.bg_image is not None:
            screen.blit(self.bg_image, position)
        if self.advancement > 0 and self.fg_image is not None:
            screen.blit(self.fg_image, position)

    def move(self, new_pos: tuple):
        self.position = new_pos
