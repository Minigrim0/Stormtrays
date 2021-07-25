import pygame as pg

from models.screen import Screen


class LoadingBar:
    """A loading bar"""

    def __init__(
        self, pos: tuple, size: tuple, initial_adv: int = 0,
        fg_color: tuple = (76, 187, 23), bg_color: tuple = (138, 7, 7)
    ):
        self.position = pos
        self.size = size

        self.current_advancement = initial_adv
        self.advancement = initial_adv

        self.fg_color = fg_color
        self.bg_color = bg_color

        self.moving_speed = 0

        self.bg_image = pg.Surface(self.size)
        self.bg_image.fill(self.bg_color)

        self._buildImage()

    def _buildImage(self):
        """Builds the foreground image if the moving_speed is not null"""
        if self.moving_speed != 0:
            self.fg_image = pg.Surface((int(self.current_advancement * self.size[0]), self.size[1]))
            self.fg_image.fill(self.fg_color)

    def set_advancement(self, advancement: int):
        """Sets the advancement of the loading"""
        self.advancement = advancement
        self.moving_speed = (self.advancement - self.current_advancement) // 2

    def update(self, timeElapsed: int):
        """Updates the bar according to its advancement"""
        if abs(self.moving_speed) > 2:
            self.current_advancement += self.moving_speed * timeElapsed
        else:
            self.current_advancement = self.advancement
            self.moving_speed = 0

    def draw(self, screen: Screen):
        """Draws the bar on the screen"""
        screen.blit(self.bg_image, self.position)
        if self.advancement > 0:
            screen.blit(self.fg_image, self.position)

    def move(self, new_pos: tuple):
        self.position = new_pos
