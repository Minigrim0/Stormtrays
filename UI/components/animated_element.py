import math as m

import pygame as pg


class Animated:
    """An animable object"""

    def __init__(self, image: pg.Surface, start: tuple, end: tuple, style: str, duration: float, offset: float = 0):
        self.image = image
        self.start_pos = start
        self.end_pos = end
        self.current_position = start
        self.time = 0
        self.initTime = duration

        available_styles = ("linear", "sine")
        if style not in available_styles:
            raise RuntimeError(f"incorrect value for style: {style} not in {available_styles}")
        self.style = style

    def getSpeeds(self):
        if self.style == "linear":
            delta_x = self.end_pos[0] - self.current_position[0]
            delta_y = self.end_pos[1] - self.current_position[1]
            speed_x = delta_x * self.time
            speed_y = delta_y * self.time
        elif self.style == "sine":
            A_x = self.end_pos[0] - self.start_pos[0]
            A_y = self.end_pos[1] - self.start_pos[1]

            wt = (self.time * 2 / self.initTime) * m.pi

            # First derivative of the position A(x - sin(pi * x) / pi)
            speed_x = A_x * (1 - m.cos(wt))
            speed_y = A_y * (1 - m.cos(wt))

        return speed_x, speed_y

    def update(self, timeElapsed):
        """Updates the position of the object depending on time"""
        self.time += timeElapsed
        speed_x, speed_y = self.getSpeeds()

        self.current_position = (
            self.current_position[0] + speed_x * timeElapsed,
            self.current_position[1] + speed_y * timeElapsed,
        )

    def draw(self, screen):
        """Draws the object on the screen"""
        screen.blit(self.image, (int(self.current_position[0]), int(self.current_position[1])))

    def invert(self):
        self.start_pos, self.end_pos = self.end_pos, self.start_pos
        self.current_position = self.start_pos
