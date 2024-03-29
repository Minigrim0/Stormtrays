import json

import pygame as pg

from models.screen import Screen
from src.runnable import Runnable
from UI.components.animated_element import Animated


class Animation(Runnable):
    """Represents a blocking animation"""

    def __init__(
        self, animation: str, screen: Screen,
        pickFrom: dict = None, background: callable = None, **background_kwargs
    ):
        super().__init__()
        self.screen: Screen = screen
        self.elements: list(Animated) = []
        self.totalTime = 1

        self.background = None  # Either a pg.Surface or a callable
        self.background_kwargs = background_kwargs

        with open(animation) as animation_file:
            data = json.load(animation_file)
            self.load(data, pickFrom=pickFrom, background=background)

    def load(self, data: dict, pickFrom: dict = None, background: callable = None):
        """Loads the animation from the given dict"""
        self.duration = data["duration"]
        if "background" in data.keys():
            self.background = pg.image.load(data["background"])
        else:
            self.background = background

        for elem in data["elements"]:
            key = elem["image"]
            self.elements.append(
                Animated(
                    pickFrom[key]
                    if pickFrom is not None and key in pickFrom.keys()
                    else pg.image.load(key).convert_alpha(),
                    tuple(elem["from"]),
                    tuple(elem["to"]),
                    style=elem["style"],
                    duration=self.totalTime,
                )
            )

    def loop(self):
        """Method called at each code loop"""
        self.draw()
        for animated in self.elements:
            animated.update(self.screen.elapsed_time)
            animated.draw(self.screen)
        self.totalTime -= self.screen.elapsed_time
        self.handleEvent()

        if self.totalTime <= 0:
            self.running = False

        self.screen.flip()

    def invert(self):
        """Inverts the animation of all the elements"""
        for elem in self.elements:
            elem.invert()

    def handleEvent(self):
        """Handles the user's events"""
        self.screen.getEvent()

    def draw(self):
        """Draws the animation on the screen"""
        if self.background is not None:
            if callable(self.background):
                self.background(**self.background_kwargs)
            else:
                self.screen.blit(self.background, (0, 0))
